#!/usr/bin/env python3
"""
Test Email Update Endpoint
"""

import requests
import json

def test_email_update():
    """Test the email update endpoint"""
    print("🧪 Testing Email Update Endpoint")
    print("="*40)
    
    try:
        # Get a patient ID first
        response = requests.get("http://localhost:5000/api/data?limit=1")
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                patient_id = data['data'][0]['patient_id']
                current_email = data['data'][0]['email']
                
                print(f"📋 Testing with patient: {patient_id}")
                print(f"📧 Current email: {current_email}")
                
                # Test email update
                update_data = {
                    "patient_id": patient_id,
                    "email": "test-update@example.com"
                }
                
                print(f"\n📤 Sending update request...")
                print(f"   Data: {json.dumps(update_data, indent=2)}")
                
                response = requests.post(
                    "http://localhost:5000/api/update-patient-email",
                    json=update_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                print(f"\n📥 Response Status: {response.status_code}")
                print(f"📥 Response Headers: {dict(response.headers)}")
                
                try:
                    result = response.json()
                    print(f"📥 Response JSON: {json.dumps(result, indent=2)}")
                except:
                    print(f"📥 Response Text: {response.text}")
                
                if response.status_code == 200:
                    print("✅ Email update successful!")
                else:
                    print("❌ Email update failed!")
                    
            else:
                print("❌ No patients found")
        else:
            print(f"❌ Failed to get patient data: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_email_update()
