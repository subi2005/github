#!/usr/bin/env python3
"""
View Saved Patient Data
"""

import sqlite3
import pandas as pd

def view_saved_data():
    """View all saved patient data from the database"""
    print("📊 Viewing Saved Patient Data")
    print("="*50)
    
    try:
        conn = sqlite3.connect('risk_data.db')
        
        # Get total count
        total_count = pd.read_sql_query("SELECT COUNT(*) as total FROM risk_training", conn)
        print(f"📈 Total patients in database: {total_count['total'].iloc[0]:,}")
        
        # Get patients with predictions
        predicted_count = pd.read_sql_query("SELECT COUNT(*) as predicted FROM risk_training WHERE RISK_30D IS NOT NULL", conn)
        print(f"🎯 Patients with predictions: {predicted_count['predicted'].iloc[0]:,}")
        
        # Get patients with emails
        email_count = pd.read_sql_query("SELECT COUNT(*) as emails FROM risk_training WHERE EMAIL IS NOT NULL AND EMAIL != ''", conn)
        print(f"📧 Patients with emails: {email_count['emails'].iloc[0]:,}")
        
        print("\n" + "="*50)
        print("📋 SAMPLE PATIENT DATA (First 10 records)")
        print("="*50)
        
        # Get sample data with all important columns
        query = """
        SELECT 
            DESYNPUF_ID as Patient_ID,
            AGE as Age,
            CASE WHEN GENDER = 1 THEN 'Male' ELSE 'Female' END as Gender,
            RISK_30D as Risk_30D,
            RISK_60D as Risk_60D,
            RISK_90D as Risk_90D,
            RISK_LABEL as Risk_Level,
            TOP_3_FEATURES as Top_Features,
            AI_RECOMMENDATIONS as AI_Recommendations,
            EMAIL as Email,
            TOTAL_CLAIMS_COST as Claims_Cost,
            BMI as BMI,
            GLUCOSE as Glucose,
            HbA1c as HbA1c,
            CHOLESTEROL as Cholesterol
        FROM risk_training 
        WHERE RISK_30D IS NOT NULL
        ORDER BY RISK_30D DESC
        LIMIT 10
        """
        
        df = pd.read_sql_query(query, conn)
        
        # Display the data
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 30)
        
        print(df.to_string(index=False))
        
        print("\n" + "="*50)
        print("🔍 DETAILED VIEW OPTIONS")
        print("="*50)
        
        print("1. 📊 Web Dashboard: http://localhost:5000")
        print("2. 🗄️  Database File: risk_data.db")
        print("3. 📄 Export to CSV: Run 'export_data.py'")
        print("4. 🔍 Search specific patient: Run 'search_patient.py'")
        
        # Show risk distribution
        print("\n" + "="*50)
        print("📊 RISK DISTRIBUTION")
        print("="*50)
        
        risk_dist = pd.read_sql_query("""
            SELECT 
                RISK_LABEL as Risk_Level,
                COUNT(*) as Count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM risk_training WHERE RISK_30D IS NOT NULL), 2) as Percentage
            FROM risk_training 
            WHERE RISK_30D IS NOT NULL
            GROUP BY RISK_LABEL
            ORDER BY Count DESC
        """, conn)
        
        print(risk_dist.to_string(index=False))
        
        # Show patients with emails
        print("\n" + "="*50)
        print("📧 PATIENTS WITH EMAILS")
        print("="*50)
        
        email_patients = pd.read_sql_query("""
            SELECT 
                DESYNPUF_ID as Patient_ID,
                AGE as Age,
                CASE WHEN GENDER = 1 THEN 'Male' ELSE 'Female' END as Gender,
                RISK_30D as Risk_30D,
                RISK_LABEL as Risk_Level,
                EMAIL as Email
            FROM risk_training 
            WHERE EMAIL IS NOT NULL AND EMAIL != ''
            ORDER BY RISK_30D DESC
        """, conn)
        
        print(email_patients.to_string(index=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    view_saved_data()
