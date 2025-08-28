#!/usr/bin/env python3
"""
Check which patients have emails
"""

import sqlite3

def check_email_patients():
    """Check which patients have emails and their risk scores"""
    print("🔍 Checking Patients with Emails")
    print("="*40)
    
    try:
        conn = sqlite3.connect('risk_data.db')
        cursor = conn.cursor()
        
        # Get patients with emails and their risk scores
        cursor.execute("""
            SELECT DESYNPUF_ID, EMAIL, RISK_30D, RISK_LABEL 
            FROM risk_training 
            WHERE EMAIL IS NOT NULL AND EMAIL != ''
            ORDER BY RISK_30D DESC
        """)
        
        patients = cursor.fetchall()
        print(f"📧 Found {len(patients)} patients with emails:")
        
        for patient_id, email, risk_30d, risk_label in patients:
            print(f"   - {patient_id}: {email} (Risk: {risk_30d}%, {risk_label})")
        
        # Check if any of these patients would appear in top 100 by risk
        cursor.execute("""
            SELECT DESYNPUF_ID, EMAIL, RISK_30D, RISK_LABEL 
            FROM risk_training 
            WHERE EMAIL IS NOT NULL AND EMAIL != ''
            ORDER BY RISK_30D DESC
            LIMIT 10
        """)
        
        top_email_patients = cursor.fetchall()
        print(f"\n🏆 Top 10 patients with emails (by risk):")
        
        for patient_id, email, risk_30d, risk_label in top_email_patients:
            print(f"   - {patient_id}: {email} (Risk: {risk_30d}%, {risk_label})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_email_patients()
