#!/usr/bin/env python3
"""
Add emails to top risk patients
"""

import sqlite3

def add_emails_to_top_patients():
    """Add email addresses to the highest risk patients"""
    print("📧 Adding emails to top risk patients")
    print("="*40)
    
    try:
        conn = sqlite3.connect('risk_data.db')
        cursor = conn.cursor()
        
        # Get the top 10 highest risk patients
        cursor.execute("""
            SELECT DESYNPUF_ID, RISK_30D, RISK_LABEL 
            FROM risk_training 
            ORDER BY RISK_30D DESC 
            LIMIT 10
        """)
        
        top_patients = cursor.fetchall()
        print(f"🏆 Top 10 highest risk patients:")
        
        # Test email addresses
        test_emails = [
            'highrisk1@example.com',
            'highrisk2@example.com', 
            'highrisk3@example.com',
            'highrisk4@example.com',
            'highrisk5@example.com',
            'highrisk6@example.com',
            'highrisk7@example.com',
            'highrisk8@example.com',
            'highrisk9@example.com',
            'highrisk10@example.com'
        ]
        
        for i, (patient_id, risk_30d, risk_label) in enumerate(top_patients):
            print(f"   {i+1}. {patient_id}: {risk_30d}% ({risk_label})")
            
            # Add email if patient doesn't already have one
            cursor.execute("SELECT EMAIL FROM risk_training WHERE DESYNPUF_ID = ?", (patient_id,))
            existing_email = cursor.fetchone()[0]
            
            if not existing_email or existing_email.strip() == '':
                email = test_emails[i] if i < len(test_emails) else f'patient{i+1}@example.com'
                cursor.execute("""
                    UPDATE risk_training 
                    SET EMAIL = ? 
                    WHERE DESYNPUF_ID = ?
                """, (email, patient_id))
                print(f"      ✅ Added email: {email}")
            else:
                print(f"      ℹ️  Already has email: {existing_email}")
        
        conn.commit()
        
        # Verify the changes
        cursor.execute("SELECT COUNT(*) FROM risk_training WHERE EMAIL IS NOT NULL AND EMAIL != ''")
        total_emails = cursor.fetchone()[0]
        print(f"\n📊 Total patients with emails: {total_emails}")
        
        # Show top 5 patients with emails
        cursor.execute("""
            SELECT DESYNPUF_ID, EMAIL, RISK_30D, RISK_LABEL 
            FROM risk_training 
            WHERE EMAIL IS NOT NULL AND EMAIL != ''
            ORDER BY RISK_30D DESC 
            LIMIT 5
        """)
        
        top_email_patients = cursor.fetchall()
        print(f"\n📧 Top 5 patients with emails:")
        for patient_id, email, risk_30d, risk_label in top_email_patients:
            print(f"   - {patient_id}: {email} (Risk: {risk_30d}%, {risk_label})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    add_emails_to_top_patients()
