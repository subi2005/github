#!/usr/bin/env python3
"""
Email Service for Risk Stratification
Handles sending AI recommendations to high-risk patients
"""

import os
from datetime import datetime
from flask import current_app
from flask_mail import Mail, Message
from risk.logger import logger

# Initialize Flask-Mail
mail = Mail()

def init_email_service(app):
    """Initialize email service with Flask app"""
    try:
        # Import email configuration
        import email_config
        
        # Email configuration from config file
        app.config['MAIL_SERVER'] = email_config.MAIL_SERVER
        app.config['MAIL_PORT'] = email_config.MAIL_PORT
        app.config['MAIL_USE_TLS'] = email_config.MAIL_USE_TLS
        app.config['MAIL_USE_SSL'] = email_config.MAIL_USE_SSL
        app.config['MAIL_USERNAME'] = email_config.MAIL_USERNAME
        app.config['MAIL_PASSWORD'] = email_config.MAIL_PASSWORD
        app.config['MAIL_DEFAULT_SENDER'] = email_config.MAIL_DEFAULT_SENDER
        
        mail.init_app(app)
        logger.info("Email service initialized with custom configuration")
        
    except ImportError:
        # Fallback to environment variables if config file not found
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
        app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your-app-password')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'your-email@gmail.com')
        
        mail.init_app(app)
        logger.warning("Email service initialized with default settings. Please configure email_config.py")

def is_high_risk(risk_label):
    """Check if patient is high risk based on risk label"""
    high_risk_labels = ['Very High Risk', 'High Risk']
    return risk_label in high_risk_labels

def send_recommendations_email(patient_data, recommendations, pdf_attachment=None):
    """Send AI recommendations email to patient with optional PDF attachment"""
    try:
        if not patient_data.get('EMAIL'):
            logger.warning(f"No email address for patient {patient_data.get('DESYNPUF_ID')}")
            return False
            
        if not is_high_risk(patient_data.get('RISK_LABEL', '')):
            logger.info(f"Patient {patient_data.get('DESYNPUF_ID')} is not high risk, skipping email")
            return False
        
        # Create email message
        subject = f"Your Health Risk Assessment Report - Patient ID: {patient_data.get('DESYNPUF_ID')}"
        
        # Format email body
        body = f"""
Dear Patient,

We are sending you your personalized Health Risk Assessment Report based on your recent medical evaluation.

Your Risk Assessment Summary:
- 30-Day Risk: {patient_data.get('RISK_30D', 'N/A')}%
- 60-Day Risk: {patient_data.get('RISK_60D', 'N/A')}%
- 90-Day Risk: {patient_data.get('RISK_90D', 'N/A')}%
- Risk Level: {patient_data.get('RISK_LABEL', 'N/A')}

Top Risk Factors: {patient_data.get('TOP_3_FEATURES', 'N/A')}

AI-Generated Recommendations:
{recommendations}

Your detailed report is attached to this email as a PDF document. Please review it carefully and discuss the findings with your healthcare provider.

Important Next Steps:
1. Schedule an appointment with your primary care physician
2. Review your current medications with your pharmacist
3. Implement the lifestyle changes recommended in the report
4. Monitor your symptoms and report any changes

If you have any questions or concerns, please contact your healthcare provider immediately.

Best regards,
Your Healthcare Team

---
This is an automated message. Please do not reply to this email.
For medical emergencies, call 911 or your local emergency number.
        """
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[patient_data['EMAIL']],
            body=body
        )
        
        # Attach PDF if provided
        if pdf_attachment:
            msg.attach(
                filename=f"patient_report_{patient_data.get('DESYNPUF_ID')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                content_type="application/pdf",
                data=pdf_attachment
            )
        
        mail.send(msg)
        logger.info(f"Recommendations email with PDF sent to {patient_data['EMAIL']} for patient {patient_data.get('DESYNPUF_ID')}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email to {patient_data.get('EMAIL', 'unknown')}: {e}")
        return False

def send_bulk_recommendations_emails(patients_data):
    """Send recommendations emails to multiple high-risk patients"""
    success_count = 0
    total_high_risk = 0
    
    for patient_data in patients_data:
        if is_high_risk(patient_data.get('RISK_LABEL', '')):
            total_high_risk += 1
            if patient_data.get('EMAIL') and patient_data.get('AI_RECOMMENDATIONS'):
                if send_recommendations_email(patient_data, patient_data['AI_RECOMMENDATIONS']):
                    success_count += 1
    
    logger.info(f"Bulk email sending completed: {success_count}/{total_high_risk} high-risk patients")
    return success_count, total_high_risk
