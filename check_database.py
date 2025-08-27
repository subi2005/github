#!/usr/bin/env python3
"""
Check Database Status
"""

import sqlite3
import pandas as pd

def check_database():
    """Check database status and email column"""
    print("🔍 Checking Database Status")
    print("="*40)
    
    try:
        conn = sqlite3.connect('risk_data.db')
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='risk_training'")
        if cursor.fetchone():
            print("✅ risk_training table exists")
        else:
            print("❌ risk_training table not found")
            return
        
        # Check table structure
        cursor.execute("PRAGMA table_info(risk_training)")
        columns = cursor.fetchall()
        print(f"\n📋 Table columns ({len(columns)} total):")
        
        email_column_exists = False
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            print(f"   - {col_name} ({col_type})")
            if col_name == 'EMAIL':
                email_column_exists = True
        
        if email_column_exists:
            print("\n✅ EMAIL column exists")
        else:
            print("\n❌ EMAIL column not found")
        
        # Check total records
        cursor.execute("SELECT COUNT(*) FROM risk_training")
        total_records = cursor.fetchone()[0]
        print(f"\n📊 Total records: {total_records}")
        
        # Check records with emails
        if email_column_exists:
            cursor.execute("SELECT COUNT(*) FROM risk_training WHERE EMAIL IS NOT NULL AND EMAIL != ''")
            email_records = cursor.fetchone()[0]
            print(f"📧 Records with emails: {email_records}")
            
            # Show sample emails
            cursor.execute("SELECT DESYNPUF_ID, EMAIL FROM risk_training WHERE EMAIL IS NOT NULL AND EMAIL != '' LIMIT 5")
            sample_emails = cursor.fetchall()
            if sample_emails:
                print("\n📧 Sample email addresses:")
                for patient_id, email in sample_emails:
                    print(f"   - {patient_id}: {email}")
        
        # Check if there are any records with predictions
        cursor.execute("SELECT COUNT(*) FROM risk_training WHERE RISK_30D IS NOT NULL")
        prediction_records = cursor.fetchone()[0]
        print(f"\n🎯 Records with predictions: {prediction_records}")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_database()
