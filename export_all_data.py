#!/usr/bin/env python3
"""
Export All Data to CSV
"""

import sqlite3
import pandas as pd
from datetime import datetime

def export_data():
    """Export all patient data to CSV files"""
    print("📄 EXPORTING ALL DATA TO CSV")
    print("="*50)
    
    try:
        conn = sqlite3.connect('risk_data.db')
        
        # 1. Export all patient data
        print("📊 Exporting all patient data...")
        all_data_query = """
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
            CHOLESTEROL as Cholesterol,
            RENAL_DISEASE as Renal_Disease,
            ALZHEIMER as Alzheimer,
            HEARTFAILURE as Heart_Failure,
            CANCER as Cancer,
            PULMONARY as Pulmonary,
            OSTEOPOROSIS as Osteoporosis,
            RHEUMATOID as Rheumatoid,
            STROKE as Stroke
        FROM risk_training 
        WHERE RISK_30D IS NOT NULL
        ORDER BY RISK_30D DESC
        """
        
        all_data = pd.read_sql_query(all_data_query, conn)
        all_data_filename = f"all_patient_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        all_data.to_csv(all_data_filename, index=False)
        print(f"✅ Exported {len(all_data):,} patients to: {all_data_filename}")
        
        # 2. Export high-risk patients only
        print("🏆 Exporting high-risk patients...")
        high_risk_query = """
        SELECT 
            DESYNPUF_ID as Patient_ID,
            AGE as Age,
            CASE WHEN GENDER = 1 THEN 'Male' ELSE 'Female' END as Gender,
            RISK_30D as Risk_30D,
            RISK_LABEL as Risk_Level,
            TOP_3_FEATURES as Top_Features,
            AI_RECOMMENDATIONS as AI_Recommendations,
            EMAIL as Email
        FROM risk_training 
        WHERE RISK_30D >= 70 AND RISK_30D IS NOT NULL
        ORDER BY RISK_30D DESC
        """
        
        high_risk_data = pd.read_sql_query(high_risk_query, conn)
        high_risk_filename = f"high_risk_patients_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        high_risk_data.to_csv(high_risk_filename, index=False)
        print(f"✅ Exported {len(high_risk_data):,} high-risk patients to: {high_risk_filename}")
        
        # 3. Export patients with emails
        print("📧 Exporting patients with emails...")
        email_query = """
        SELECT 
            DESYNPUF_ID as Patient_ID,
            AGE as Age,
            CASE WHEN GENDER = 1 THEN 'Male' ELSE 'Female' END as Gender,
            RISK_30D as Risk_30D,
            RISK_LABEL as Risk_Level,
            TOP_3_FEATURES as Top_Features,
            AI_RECOMMENDATIONS as AI_Recommendations,
            EMAIL as Email
        FROM risk_training 
        WHERE EMAIL IS NOT NULL AND EMAIL != ''
        ORDER BY RISK_30D DESC
        """
        
        email_data = pd.read_sql_query(email_query, conn)
        email_filename = f"patients_with_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        email_data.to_csv(email_filename, index=False)
        print(f"✅ Exported {len(email_data):,} patients with emails to: {email_filename}")
        
        # 4. Export summary statistics
        print("📈 Exporting summary statistics...")
        summary_query = """
        SELECT 
            RISK_LABEL as Risk_Level,
            COUNT(*) as Count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM risk_training WHERE RISK_30D IS NOT NULL), 2) as Percentage,
            AVG(RISK_30D) as Avg_Risk_30D,
            AVG(AGE) as Avg_Age
        FROM risk_training 
        WHERE RISK_30D IS NOT NULL
        GROUP BY RISK_LABEL
        ORDER BY Count DESC
        """
        
        summary_data = pd.read_sql_query(summary_query, conn)
        summary_filename = f"risk_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        summary_data.to_csv(summary_filename, index=False)
        print(f"✅ Exported summary statistics to: {summary_filename}")
        
        print("\n" + "="*50)
        print("📁 EXPORTED FILES:")
        print("="*50)
        print(f"1. 📊 All Patient Data: {all_data_filename}")
        print(f"2. 🏆 High-Risk Patients: {high_risk_filename}")
        print(f"3. 📧 Patients with Emails: {email_filename}")
        print(f"4. 📈 Risk Summary: {summary_filename}")
        
        print("\n💡 TIP: Open these CSV files in Excel or Google Sheets for easy viewing!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    export_data()
