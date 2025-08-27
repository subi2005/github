#!/usr/bin/env python3
"""
Force create EMAIL column and add test data
"""

import sqlite3
from risk.db import ensure_prediction_columns

def force_create_email_column():
    """Force create EMAIL column in database"""
    print("🔧 Force creating EMAIL column...")
    
    try:
        # This will create the EMAIL column if it doesn't exist
        ensure_prediction_columns("risk_training")
        print("✅ EMAIL column created/verified successfully")
        
        # Add some test email data
        add_test_emails()
        
    except Exception as e:
        print(f"❌ Error creating EMAIL column: {e}")

def add_test_emails():
    """Add test email addresses to some patients"""
    print("\n📧 Adding test email addresses...")
    
    try:
        conn = sqlite3.connect('risk_data.db')
        cursor = conn.cursor()
        
        # Get first 5 patients
        cursor.execute("SELECT DESYNPUF_ID FROM risk_training LIMIT 5")
        patients = cursor.fetchall()
        
        # Test email addresses
        test_emails = [
            'patient1@example.com',
            'patient2@example.com', 
            'patient3@example.com',
            'patient4@example.com',
            'patient5@example.com'
        ]
        
        for i, (patient_id,) in enumerate(patients):
            if i < len(test_emails):
                cursor.execute("""
                    UPDATE risk_training 
                    SET EMAIL = ? 
                    WHERE DESYNPUF_ID = ?
                """, (test_emails[i], patient_id))
                print(f"   ✅ Added email for patient {patient_id}: {test_emails[i]}")
        
        conn.commit()
        print(f"   📧 Added {len(patients)} test email addresses")
        
        # Verify the emails were added
        cursor.execute("SELECT COUNT(*) FROM risk_training WHERE EMAIL IS NOT NULL AND EMAIL != ''")
        email_count = cursor.fetchone()[0]
        print(f"   📊 Total patients with emails: {email_count}")
        
    except Exception as e:
        print(f"❌ Error adding test emails: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    force_create_email_column()
    print("\n🎉 Email column setup complete!")
    print("   Refresh your dashboard to see the email input fields populated with test data.")

