#!/usr/bin/env python3
"""
Test Email Input Functionality
"""

import requests
import json

def test_email_api():
    """Test the email API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Email Input Functionality")
    print("="*50)
    
    # Test 1: Get patient data with emails
    print("\n1️⃣ Testing GET /api/data endpoint...")
    try:
        response = requests.get(f"{base_url}/api/data?limit=10")
        if response.status_code == 200:
            data = response.json()
            patients_with_emails = 0
            for patient in data['data']:
                if patient.get('email') and patient['email'].strip():
                    patients_with_emails += 1
                    print(f"   ✅ Patient {patient['patient_id']}: {patient['email']}")
            
            print(f"   📊 Found {patients_with_emails} patients with email addresses")
        else:
            print(f"   ❌ API returned status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing API: {e}")
    
    # Test 2: Update a patient email
    print("\n2️⃣ Testing POST /api/update-patient-email endpoint...")
    try:
        # Get first patient
        response = requests.get(f"{base_url}/api/data?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                patient_id = data['data'][0]['patient_id']
                test_email = "test@example.com"
                
                update_data = {
                    "patient_id": patient_id,
                    "email": test_email
                }
                
                response = requests.post(
                    f"{base_url}/api/update-patient-email",
                    json=update_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"   ✅ Successfully updated email for patient {patient_id}")
                    else:
                        print(f"   ❌ Update failed: {result.get('message')}")
                else:
                    print(f"   ❌ API returned status {response.status_code}")
            else:
                print("   ❌ No patients found")
    except Exception as e:
        print(f"   ❌ Error testing email update: {e}")
    
    # Test 3: Verify email was updated
    print("\n3️⃣ Verifying email update...")
    try:
        response = requests.get(f"{base_url}/api/data?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                patient = data['data'][0]
                if patient.get('email') == "test@example.com":
                    print(f"   ✅ Email update verified: {patient['email']}")
                else:
                    print(f"   ❌ Email not updated correctly: {patient.get('email')}")
    except Exception as e:
        print(f"   ❌ Error verifying update: {e}")
    
    print("\n🎉 Email input functionality test complete!")
    print("   Check your dashboard at http://localhost:5000 to see the email input fields.")

if __name__ == "__main__":
    test_email_api()

