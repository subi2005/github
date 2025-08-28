#!/usr/bin/env python3
"""
Debug API Response
"""

import requests
import json

def debug_api():
    """Debug the API response"""
    print("🔍 Debugging API Response")
    print("="*40)
    
    try:
        # Test the data API
        response = requests.get("http://localhost:5000/api/data?limit=5")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            if 'data' in data:
                patients = data['data']
                print(f"Number of patients returned: {len(patients)}")
                
                if patients:
                    print("\n📋 First patient data:")
                    first_patient = patients[0]
                    for key, value in first_patient.items():
                        print(f"   {key}: {value} (type: {type(value)})")
                    
                    print(f"\n📧 Email field: '{first_patient.get('email')}'")
                    print(f"📧 Email field type: {type(first_patient.get('email'))}")
                    
                    # Check all patients for emails
                    emails_found = 0
                    for i, patient in enumerate(patients):
                        email = patient.get('email', '')
                        if email and email.strip():
                            emails_found += 1
                            print(f"   Patient {i+1}: {patient['patient_id']} -> '{email}'")
                    
                    print(f"\n📊 Total patients with emails: {emails_found}")
                else:
                    print("❌ No patients returned")
            else:
                print("❌ No 'data' key in response")
                print(f"Response: {data}")
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_api()
