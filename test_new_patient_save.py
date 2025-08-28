#!/usr/bin/env python3
"""
Test New Patient Save Functionality
"""

import requests
import json
import time

def test_new_patient_save():
    """Test saving new patient data to database"""
    print("🧪 Testing New Patient Save Functionality")
    print("="*50)
    
    # Test data for a new patient
    test_patient = {
        "DESYNPUF_ID": f"NEW_TEST_{int(time.time())}",
        "AGE": 75,
        "GENDER": 1,  # Male
        "RENAL_DISEASE": 0,
        "PARTA": 12,
        "PARTB": 12,
        "HMO": 0,
        "PARTD": 12,
        "ALZHEIMER": 1,
        "HEARTFAILURE": 0,
        "CANCER": 0,
        "PULMONARY": 0,
        "OSTEOPOROSIS": 0,
        "RHEUMATOID": 0,
        "STROKE": 0,
        "TOTAL_CLAIMS_COST": 2500.0,
        "IN_ADM": 0.0,
        "OUT_VISITS": 8,
        "BMI": 28,
        "BP_S": 140,
        "GLUCOSE": 180,
        "HbA1c": 8.5,
        "CHOLESTEROL": 200,
        "ED_VISITS": 1,
        "RX_ADH": 0.85
    }
    
    print(f"📋 Test Patient ID: {test_patient['DESYNPUF_ID']}")
    print(f"📊 Age: {test_patient['AGE']}, Gender: {'Male' if test_patient['GENDER'] == 1 else 'Female'}")
    print(f"🏥 Conditions: Alzheimer's: {test_patient['ALZHEIMER']}, Heart Failure: {test_patient['HEARTFAILURE']}")
    
    try:
        # Send prediction request
        print("\n📤 Sending prediction request...")
        response = requests.post(
            "http://localhost:5000/api/predict",
            json=test_patient,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction successful!")
            print(f"📊 Risk Score: {result['predictions']['RISK_30D']}%")
            print(f"🏷️ Risk Label: {result['predictions']['RISK_LABEL']}")
            print(f"📝 Message: {result.get('message', 'No message')}")
            
            # Wait a moment for database to update
            print("\n⏳ Waiting for database update...")
            time.sleep(2)
            
            # Check if patient was saved in database
            print("\n🔍 Checking if patient was saved in database...")
            check_response = requests.get("http://localhost:5000/api/data?limit=1000")
            
            if check_response.status_code == 200:
                data = check_response.json()
                patients = data['data']
                
                # Look for our test patient
                found_patient = None
                for patient in patients:
                    if patient['patient_id'] == test_patient['DESYNPUF_ID']:
                        found_patient = patient
                        break
                
                if found_patient:
                    print("✅ Patient found in database!")
                    print(f"📊 Saved Risk Score: {found_patient['risk_30d']}%")
                    print(f"🏷️ Saved Risk Label: {found_patient['risk_label']}")
                    print(f"🤖 AI Recommendations: {found_patient.get('ai_recommendations', 'None')}")
                else:
                    print("❌ Patient not found in database")
                    
            else:
                print(f"❌ Failed to check database: {check_response.status_code}")
                
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            try:
                error_result = response.json()
                print(f"📝 Error: {error_result.get('error', 'Unknown error')}")
            except:
                print(f"📝 Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_new_patient_save()
