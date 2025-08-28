#!/usr/bin/env python3
"""
Risk Stratification Web Application
Flask app to display risk stratification results on localhost
"""

from flask import Flask, render_template, jsonify, request, send_file
import pandas as pd
import sqlite3
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime
from risk.db import get_engine
from risk.model import load_model, predict_batch
from risk.logger import logger
from risk.email_service import init_email_service, send_recommendations_email, send_bulk_recommendations_emails

app = Flask(__name__)

def get_database_data(limit=100):
    """Get data from SQLite database"""
    try:
        engine = get_engine()
        query = f"""
        SELECT DESYNPUF_ID, AGE, GENDER, TOTAL_CLAIMS_COST, 
               RISK_30D, RISK_60D, RISK_90D, RISK_LABEL, TOP_3_FEATURES, AI_RECOMMENDATIONS, EMAIL
        FROM risk_training 
        ORDER BY RISK_30D DESC 
        LIMIT {limit}
        """
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return pd.DataFrame()

def get_summary_stats():
    """Get summary statistics"""
    try:
        engine = get_engine()
        query = """
        SELECT 
            COUNT(*) as total_patients,
            AVG(RISK_30D) as avg_risk_30d,
            AVG(RISK_60D) as avg_risk_60d,
            AVG(RISK_90D) as avg_risk_90d,
            COUNT(CASE WHEN RISK_LABEL = 'Very High Risk' THEN 1 END) as very_high_risk,
            COUNT(CASE WHEN RISK_LABEL = 'High Risk' THEN 1 END) as high_risk,
            COUNT(CASE WHEN RISK_LABEL = 'Moderate Risk' THEN 1 END) as moderate_risk,
            COUNT(CASE WHEN RISK_LABEL = 'Low Risk' THEN 1 END) as low_risk,
            COUNT(CASE WHEN RISK_LABEL = 'Very Low Risk' THEN 1 END) as very_low_risk
        FROM risk_training
        """
        df = pd.read_sql(query, engine)
        return df.iloc[0].to_dict()
    except Exception as e:
        logger.error(f"Error loading summary stats: {e}")
        return {}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get patient data"""
    limit = request.args.get('limit', 100, type=int)
    df = get_database_data(limit)
    
    if df.empty:
        return jsonify({'error': 'No data available'})
    
    # Convert to JSON-friendly format
    data = []
    for _, row in df.iterrows():
        data.append({
            'patient_id': str(row['DESYNPUF_ID']),
            'age': int(row['AGE']) if pd.notna(row['AGE']) else 0,
            'gender': 'Male' if row['GENDER'] == 1 else 'Female',
            'claims_cost': float(row['TOTAL_CLAIMS_COST']) if pd.notna(row['TOTAL_CLAIMS_COST']) else 0,
            'risk_30d': int(row['RISK_30D']) if pd.notna(row['RISK_30D']) else 0,
            'risk_60d': int(row['RISK_60D']) if pd.notna(row['RISK_60D']) else 0,
            'risk_90d': int(row['RISK_90D']) if pd.notna(row['RISK_90D']) else 0,
            'risk_label': str(row['RISK_LABEL']) if pd.notna(row['RISK_LABEL']) else 'Unknown',
            'top_features': str(row['TOP_3_FEATURES']) if pd.notna(row['TOP_3_FEATURES']) else 'N/A',
            'ai_recommendations': str(row['AI_RECOMMENDATIONS']) if pd.notna(row['AI_RECOMMENDATIONS']) else 'Continue current care plan',
            'email': str(row['EMAIL']) if pd.notna(row['EMAIL']) else ''
        })
    
    return jsonify({'data': data})

@app.route('/api/summary')
def get_summary():
    """API endpoint to get summary statistics"""
    stats = get_summary_stats()
    return jsonify(stats)

@app.route('/api/predict', methods=['POST'])
def predict_single():
    """API endpoint to predict risk for a single patient"""
    try:
        data = request.json
        
        # Check if this is a new patient or existing patient
        if 'DESYNPUF_ID' in data and data['DESYNPUF_ID'].startswith('NEW_'):
            # New patient prediction - save to database first
            try:
                # Ensure all necessary columns exist in database
                from risk.db import ensure_prediction_columns
                ensure_prediction_columns("risk_training")
                
                # Create DataFrame with new patient data
                patient_data = pd.DataFrame([data])
                
                # Save new patient data to database first
                engine = get_engine()
                patient_data.to_sql('risk_training', engine, if_exists='append', index=False)
                
                logger.info(f"New patient data saved to database: {data['DESYNPUF_ID']}")
                
                # Now make prediction
                model = load_model("models/risk_model.pkl")
                predictions = predict_batch(patient_data, model)
                prediction_result = predictions.iloc[0].to_dict()
                
                # Update the database with predictions
                from risk.db import update_predictions_in_db
                update_predictions_in_db(predictions, "risk_training")
                
                logger.info(f"Prediction completed and saved for new patient: {prediction_result}")
                
                return jsonify({
                    'success': True,
                    'predictions': prediction_result,
                    'message': f'New patient {data["DESYNPUF_ID"]} saved to database with predictions'
                })
                
            except Exception as save_error:
                logger.error(f"Error saving new patient to database: {save_error}")
                return jsonify({'error': f'Failed to save patient data: {str(save_error)}'}), 500
        else:
            # Existing patient prediction from database
            desynpuf_id = data.get('DESYNPUF_ID')
            if not desynpuf_id:
                return jsonify({'error': 'DESYNPUF_ID is required for existing patient prediction'}), 400
            
            # Load patient data from database
            engine = get_engine()
            query = f"""
            SELECT * FROM risk_training 
            WHERE DESYNPUF_ID = '{desynpuf_id}'
            """
            patient_df = pd.read_sql(query, engine)
            
            if patient_df.empty:
                return jsonify({'error': f'Patient with DESYNPUF_ID {desynpuf_id} not found'}), 404
            
            # Load model and predict
            model = load_model("models/risk_model.pkl")
            predictions = predict_batch(patient_df, model)
            
            # Update database with predictions
            from risk.db import update_predictions_in_db
            update_predictions_in_db(predictions, "risk_training")
            
            # Get the updated prediction results
            prediction_result = predictions.iloc[0].to_dict()
            
            logger.info(f"Prediction completed and database updated for patient {desynpuf_id}: {prediction_result}")
            
            return jsonify({
                'success': True,
                'predictions': prediction_result,
                'message': f'Database updated for patient {desynpuf_id}'
            })
            
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'database': 'connected'})

@app.route('/api/predict-all', methods=['POST'])
def predict_all_patients():
    """API endpoint to predict risk for all patients in database"""
    try:
        # Load all patient data from database
        engine = get_engine()
        query = """
        SELECT * FROM risk_training 
        WHERE RISK_30D IS NULL OR RISK_60D IS NULL OR RISK_90D IS NULL 
        OR RISK_LABEL IS NULL OR TOP_3_FEATURES IS NULL
        """
        patients_df = pd.read_sql(query, engine)
        
        if patients_df.empty:
            return jsonify({'message': 'All patients already have predictions'})
        
        # Load model and predict
        model = load_model("models/risk_model.pkl")
        predictions = predict_batch(patients_df, model)
        
        # Update database with predictions
        from risk.db import update_predictions_in_db_bulk
        update_predictions_in_db_bulk(predictions, "risk_training")
        
        logger.info(f"Predictions completed and database updated for {len(predictions)} patients")
        
        return jsonify({
            'success': True,
            'message': f'Database updated for {len(predictions)} patients',
            'patients_processed': len(predictions)
        })
        
    except Exception as e:
        logger.error(f"Bulk prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-recommendations-email', methods=['POST'])
def send_recommendations_email_endpoint():
    """API endpoint to send recommendations email to a specific patient"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        
        if not patient_id:
            return jsonify({'error': 'Patient ID is required'}), 400
        
        # Get patient data from database
        engine = get_engine()
        query = f"""
        SELECT * FROM risk_training 
        WHERE DESYNPUF_ID = '{patient_id}'
        """
        patient_df = pd.read_sql(query, engine)
        
        if patient_df.empty:
            return jsonify({'error': f'Patient {patient_id} not found'}), 404
        
        patient_data = patient_df.iloc[0].to_dict()
        
        # Send email
        success = send_recommendations_email(patient_data, patient_data.get('AI_RECOMMENDATIONS', ''))
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Recommendations email sent to {patient_data.get("EMAIL", "patient")}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send email. Check if patient has email address and is high risk.'
            })
            
    except Exception as e:
        logger.error(f"Email sending error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-bulk-emails', methods=['POST'])
def send_bulk_emails_endpoint():
    """API endpoint to send recommendations emails to all high-risk patients"""
    try:
        # Get all high-risk patients with predictions
        engine = get_engine()
        query = """
        SELECT * FROM risk_training 
        WHERE RISK_LABEL IN ('Very High Risk', 'High Risk')
        AND AI_RECOMMENDATIONS IS NOT NULL
        AND EMAIL IS NOT NULL
        """
        patients_df = pd.read_sql(query, engine)
        
        if patients_df.empty:
            return jsonify({'message': 'No high-risk patients with email addresses found'})
        
        # Convert to list of dictionaries
        patients_data = patients_df.to_dict('records')
        
        # Send bulk emails
        success_count, total_count = send_bulk_recommendations_emails(patients_data)
        
        return jsonify({
            'success': True,
            'message': f'Emails sent to {success_count}/{total_count} high-risk patients',
            'emails_sent': success_count,
            'total_high_risk': total_count
        })
        
    except Exception as e:
        logger.error(f"Bulk email sending error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-patient-pdf/<patient_id>')
def export_patient_pdf(patient_id):
    """Export individual patient recommendations as PDF"""
    try:
        # Get patient data
        engine = get_engine()
        query = f"""
        SELECT * FROM risk_training 
        WHERE DESYNPUF_ID = '{patient_id}'
        """
        patient_df = pd.read_sql(query, engine)
        
        if patient_df.empty:
            return jsonify({'error': f'Patient {patient_id} not found'}), 404
        
        patient_data = patient_df.iloc[0]
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Title
        title = Paragraph(f"Patient Risk Assessment Report", title_style)
        elements.append(title)
        
        # Patient Information
        patient_info = f"""
        <b>Patient Information:</b><br/>
        Patient ID: {patient_data['DESYNPUF_ID']}<br/>
        Age: {patient_data['AGE']}<br/>
        Gender: {'Male' if patient_data['GENDER'] == 1 else 'Female'}<br/>
        Email: {patient_data.get('EMAIL', 'Not provided')}<br/>
        Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        patient_para = Paragraph(patient_info, styles['Normal'])
        elements.append(patient_para)
        elements.append(Spacer(1, 20))
        
        # Risk Assessment
        risk_info = f"""
        <b>Risk Assessment:</b><br/>
        30-Day Risk: {patient_data.get('RISK_30D', 'N/A')}%<br/>
        60-Day Risk: {patient_data.get('RISK_60D', 'N/A')}%<br/>
        90-Day Risk: {patient_data.get('RISK_90D', 'N/A')}%<br/>
        Risk Level: {patient_data.get('RISK_LABEL', 'N/A')}<br/>
        Top Risk Factors: {patient_data.get('TOP_3_FEATURES', 'N/A')}
        """
        risk_para = Paragraph(risk_info, styles['Normal'])
        elements.append(risk_para)
        elements.append(Spacer(1, 20))
        
        # AI Recommendations
        recommendations = patient_data.get('AI_RECOMMENDATIONS', 'No recommendations available')
        rec_info = f"""
        <b>AI-Generated Recommendations:</b><br/>
        {recommendations}
        """
        rec_para = Paragraph(rec_info, styles['Normal'])
        elements.append(rec_para)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'patient_recommendations_{patient_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"Patient PDF export error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-patient-email', methods=['POST'])
def update_patient_email_endpoint():
    """API endpoint to update patient email address"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        email = data.get('email')
        
        if not patient_id or not email:
            return jsonify({'error': 'Patient ID and email are required'}), 400
        
        # Validate email format
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Update email in database
        from risk.db import update_patient_email
        success = update_patient_email(patient_id, email)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Email updated successfully for patient {patient_id}'
            })
        else:
            return jsonify({'error': 'Failed to update email'}), 500
            
    except Exception as e:
        logger.error(f"Email update error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/send-pdf-email', methods=['POST'])
def send_pdf_email_endpoint():
    """API endpoint to send PDF report via email"""
    try:
        data = request.json
        patient_id = data.get('patient_id')
        
        if not patient_id:
            return jsonify({'error': 'Patient ID is required'}), 400
        
        # Get patient data
        from risk.db import get_patient_by_id
        patient_data = get_patient_by_id(patient_id)
        
        if not patient_data:
            return jsonify({'error': f'Patient {patient_id} not found'}), 404
        
        if not patient_data.get('EMAIL'):
            return jsonify({'error': 'Patient has no email address'}), 400
        
        # Generate PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Title
        title = Paragraph(f"Patient Risk Assessment Report", title_style)
        elements.append(title)
        
        # Patient Information
        patient_info = f"""
        <b>Patient Information:</b><br/>
        Patient ID: {patient_data['DESYNPUF_ID']}<br/>
        Age: {patient_data['AGE']}<br/>
        Gender: {'Male' if patient_data['GENDER'] == 1 else 'Female'}<br/>
        Email: {patient_data.get('EMAIL', 'Not provided')}<br/>
        Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        patient_para = Paragraph(patient_info, styles['Normal'])
        elements.append(patient_para)
        elements.append(Spacer(1, 20))
        
        # Risk Assessment
        risk_info = f"""
        <b>Risk Assessment:</b><br/>
        30-Day Risk: {patient_data.get('RISK_30D', 'N/A')}%<br/>
        60-Day Risk: {patient_data.get('RISK_60D', 'N/A')}%<br/>
        90-Day Risk: {patient_data.get('RISK_90D', 'N/A')}%<br/>
        Risk Level: {patient_data.get('RISK_LABEL', 'N/A')}<br/>
        Top Risk Factors: {patient_data.get('TOP_3_FEATURES', 'N/A')}
        """
        risk_para = Paragraph(risk_info, styles['Normal'])
        elements.append(risk_para)
        elements.append(Spacer(1, 20))
        
        # AI Recommendations
        recommendations = patient_data.get('AI_RECOMMENDATIONS', 'No recommendations available')
        rec_info = f"""
        <b>AI-Generated Recommendations:</b><br/>
        {recommendations}
        """
        rec_para = Paragraph(rec_info, styles['Normal'])
        elements.append(rec_para)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        
        # Send email with PDF attachment
        from risk.email_service import send_recommendations_email
        success = send_recommendations_email(patient_data, recommendations, pdf_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'PDF report sent to {patient_data.get("EMAIL")}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send email. Check if patient is high risk and has valid email.'
            })
            
    except Exception as e:
        logger.error(f"PDF email sending error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Initialize email service
    init_email_service(app)
    
    print("🚀 Starting Risk Stratification Web App...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🔗 API endpoints:")
    print("   - Main Dashboard: http://localhost:5000")
    print("   - Patient Data: http://localhost:5000/api/data")
    print("   - Summary Stats: http://localhost:5000/api/summary")
    print("   - Health Check: http://localhost:5000/api/health")
    print("   - Send Email: http://localhost:5000/api/send-recommendations-email")
    print("   - Send PDF Email: http://localhost:5000/api/send-pdf-email")
    print("   - Update Email: http://localhost:5000/api/update-patient-email")
    print("   - Bulk Emails: http://localhost:5000/api/send-bulk-emails")
    print("   - Patient PDF: http://localhost:5000/api/export-patient-pdf/<patient_id>")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
