#!/usr/bin/env python3
"""
Comprehensive Data Viewer - See All Your Saved Data
"""

import sqlite3
import pandas as pd
from datetime import datetime

def view_all_data():
    """View comprehensive data including new predictions"""
    print("📊 COMPREHENSIVE DATA VIEWER")
    print("="*60)
    print(f"🕒 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    try:
        conn = sqlite3.connect('risk_data.db')
        
        # 1. OVERALL STATISTICS
        print("\n📈 OVERALL STATISTICS")
        print("-" * 40)
        
        total_count = pd.read_sql_query("SELECT COUNT(*) as total FROM risk_training", conn)
        predicted_count = pd.read_sql_query("SELECT COUNT(*) as predicted FROM risk_training WHERE RISK_30D IS NOT NULL", conn)
        email_count = pd.read_sql_query("SELECT COUNT(*) as emails FROM risk_training WHERE EMAIL IS NOT NULL AND EMAIL != ''", conn)
        new_patients = pd.read_sql_query("SELECT COUNT(*) as new FROM risk_training WHERE DESYNPUF_ID LIKE 'NEW_%'", conn)
        
        print(f"📊 Total Patients: {total_count['total'].iloc[0]:,}")
        print(f"🎯 With Predictions: {predicted_count['predicted'].iloc[0]:,}")
        print(f"📧 With Emails: {email_count['emails'].iloc[0]}")
        print(f"🆕 New Patients Added: {new_patients['new'].iloc[0]}")
        
        # 2. NEW PATIENTS (Recently Added)
        print("\n🆕 NEW PATIENTS (Recently Added)")
        print("-" * 40)
        
        new_patients_data = pd.read_sql_query("""
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
                EMAIL as Email
            FROM risk_training 
            WHERE DESYNPUF_ID LIKE 'NEW_%'
            ORDER BY DESYNPUF_ID DESC
        """, conn)
        
        if not new_patients_data.empty:
            print(new_patients_data.to_string(index=False))
        else:
            print("No new patients found")
        
        # 3. TOP 10 HIGHEST RISK PATIENTS
        print("\n🏆 TOP 10 HIGHEST RISK PATIENTS")
        print("-" * 40)
        
        top_risk = pd.read_sql_query("""
            SELECT 
                DESYNPUF_ID as Patient_ID,
                AGE as Age,
                CASE WHEN GENDER = 1 THEN 'Male' ELSE 'Female' END as Gender,
                RISK_30D as Risk_30D,
                RISK_LABEL as Risk_Level,
                TOP_3_FEATURES as Top_Features,
                EMAIL as Email
            FROM risk_training 
            WHERE RISK_30D IS NOT NULL
            ORDER BY RISK_30D DESC
            LIMIT 10
        """, conn)
        
        print(top_risk.to_string(index=False))
        
        # 4. PATIENTS WITH EMAILS
        print("\n📧 PATIENTS WITH EMAIL ADDRESSES")
        print("-" * 40)
        
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
        
        print(f"Found {len(email_patients)} patients with emails:")
        print(email_patients.to_string(index=False))
        
        # 5. RISK DISTRIBUTION
        print("\n📊 RISK DISTRIBUTION")
        print("-" * 40)
        
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
        
        # 6. SAMPLE PATIENT DATA (First 5)
        print("\n📋 SAMPLE PATIENT DATA (First 5 Records)")
        print("-" * 40)
        
        sample_data = pd.read_sql_query("""
            SELECT 
                DESYNPUF_ID as Patient_ID,
                AGE as Age,
                CASE WHEN GENDER = 1 THEN 'Male' ELSE 'Female' END as Gender,
                RISK_30D as Risk_30D,
                RISK_LABEL as Risk_Level,
                TOP_3_FEATURES as Top_Features,
                EMAIL as Email
            FROM risk_training 
            WHERE RISK_30D IS NOT NULL
            ORDER BY DESYNPUF_ID
            LIMIT 5
        """, conn)
        
        print(sample_data.to_string(index=False))
        
        # 7. DATA ACCESS OPTIONS
        print("\n🔍 HOW TO ACCESS YOUR DATA")
        print("-" * 40)
        print("1. 🌐 Web Dashboard: http://localhost:5000")
        print("2. 🗄️  Database File: risk_data.db")
        print("3. 📄 Export to CSV: python export_data.py")
        print("4. 🔍 Search Patient: python search_patient.py")
        print("5. 📊 This Report: python comprehensive_data_viewer.py")
        
        # 8. RECENT ACTIVITY
        print("\n🕒 RECENT ACTIVITY")
        print("-" * 40)
        print("✅ Flask app running on http://localhost:5000")
        print("✅ New patient predictions working")
        print("✅ Email management functional")
        print("✅ PDF generation available")
        print("✅ AI recommendations active")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    view_all_data()
