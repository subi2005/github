#!/usr/bin/env python3
"""
Email System Setup Script
Helps configure and test the enhanced PDF email system
"""

import os
import sqlite3
from datetime import datetime

def check_email_config():
    """Check if email configuration is properly set up"""
    print("🔍 Checking Email Configuration...")
    
    try:
        import email_config
        
        # Check if default values are still being used
        if (email_config.MAIL_USERNAME == 'your-email@gmail.com' or 
            email_config.MAIL_PASSWORD == 'your-app-password'):
            print("❌ Email configuration needs to be updated!")
            print("   Please edit email_config.py with your actual email credentials")
            return False
        else:
            print("✅ Email configuration looks good!")
            return True
            
    except ImportError:
        print("❌ email_config.py not found!")
        print("   Please create email_config.py with your email settings")
        return False

def check_database_email_column():
    """Check if EMAIL column exists in database"""
    print("\n🗄️ Checking Database Email Column...")
    
    try:
        conn = sqlite3.connect('risk_data.db')
        cursor = conn.cursor()
        
        # Check if EMAIL column exists
        cursor.execute("PRAGMA table_info(risk_training)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'EMAIL' in columns:
            print("✅ EMAIL column exists in database")
            
            # Check how many patients have emails
            cursor.execute("SELECT COUNT(*) FROM risk_training WHERE EMAIL IS NOT NULL AND EMAIL != ''")
            email_count = cursor.fetchone()[0]
            print(f"   📧 {email_count} patients have email addresses")
            
            return True
        else:
            print("❌ EMAIL column not found in database")
            print("   The system will create it automatically when needed")
            return False
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def add_sample_emails():
    """Add sample email addresses to some patients for testing"""
    print("\n📧 Adding Sample Email Addresses...")
    
    try:
        conn = sqlite3.connect('risk_data.db')
        cursor = conn.cursor()
        
        # Get first few patients without emails
        cursor.execute("""
            SELECT DESYNPUF_ID FROM risk_training 
            WHERE EMAIL IS NULL OR EMAIL = '' 
            LIMIT 5
        """)
        patients = cursor.fetchall()
        
        if not patients:
            print("   All patients already have email addresses")
            return
        
        # Add sample emails
        sample_emails = [
            'patient1@example.com',
            'patient2@example.com', 
            'patient3@example.com',
            'patient4@example.com',
            'patient5@example.com'
        ]
        
        for i, (patient_id,) in enumerate(patients):
            if i < len(sample_emails):
                cursor.execute("""
                    UPDATE risk_training 
                    SET EMAIL = ? 
                    WHERE DESYNPUF_ID = ?
                """, (sample_emails[i], patient_id))
                print(f"   ✅ Added email for patient {patient_id}: {sample_emails[i]}")
        
        conn.commit()
        print(f"   📧 Added {len(patients)} sample email addresses")
        
    except Exception as e:
        print(f"❌ Error adding sample emails: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def test_email_system():
    """Test the email system functionality"""
    print("\n🧪 Testing Email System...")
    
    # Check if Flask app is running
    try:
        import requests
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Flask application is running")
            print("   🌐 Dashboard available at: http://localhost:5000")
        else:
            print("❌ Flask application not responding properly")
            return False
    except:
        print("❌ Flask application not running")
        print("   Please start the application with: python app.py")
        return False
    
    return True

def print_setup_instructions():
    """Print setup instructions"""
    print("\n" + "="*60)
    print("📋 EMAIL SYSTEM SETUP INSTRUCTIONS")
    print("="*60)
    
    print("\n1️⃣ CONFIGURE EMAIL SETTINGS:")
    print("   Edit email_config.py with your email provider details")
    print("   For Gmail: Enable 2FA and create an App Password")
    
    print("\n2️⃣ START THE APPLICATION:")
    print("   python app.py")
    print("   Access dashboard at: http://localhost:5000")
    
    print("\n3️⃣ ADD PATIENT EMAIL ADDRESSES:")
    print("   - Find patients in the dashboard table")
    print("   - Enter email addresses in the input fields")
    print("   - Click save button (💾) to update database")
    
    print("\n4️⃣ SEND PDF REPORTS:")
    print("   - Individual: Click '📄📧' button next to patient")
    print("   - Bulk: Click 'Send Bulk Emails' button")
    
    print("\n5️⃣ TEST THE SYSTEM:")
    print("   - Add test email addresses")
    print("   - Send test PDF emails")
    print("   - Check inbox for received reports")
    
    print("\n📚 DOCUMENTATION:")
    print("   - README_PDF_EMAIL_SYSTEM.md - Complete guide")
    print("   - README_EMAIL_SETUP.md - Email configuration")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🚀 Enhanced PDF Email System Setup")
    print("="*50)
    
    # Check email configuration
    email_config_ok = check_email_config()
    
    # Check database
    db_ok = check_database_email_column()
    
    # Test system
    system_ok = test_email_system()
    
    # Add sample emails if needed
    if db_ok and system_ok:
        add_sample_emails()
    
    # Print instructions
    print_setup_instructions()
    
    # Summary
    print("\n📊 SETUP SUMMARY:")
    print(f"   Email Configuration: {'✅' if email_config_ok else '❌'}")
    print(f"   Database Setup: {'✅' if db_ok else '❌'}")
    print(f"   System Running: {'✅' if system_ok else '❌'}")
    
    if email_config_ok and db_ok and system_ok:
        print("\n🎉 Setup Complete! Your email system is ready to use!")
    else:
        print("\n⚠️  Some setup steps need attention. Please review the instructions above.")

if __name__ == "__main__":
    main()

