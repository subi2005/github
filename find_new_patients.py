#!/usr/bin/env python3
"""
Find New Patients - Search for recently added patients
"""

import sqlite3
import pandas as pd

def find_new_patients():
    """Find recently added patients"""
    print("🔍 FINDING NEW PATIENTS")
    print("="*50)
    
    try:
        conn = sqlite3.connect('risk_data.db')
        
        # Search for patients with NEW_ prefix
        query = """
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
        """
        
        df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            print(f"✅ Found {len(df)} new patients:")
            print("-" * 50)
            print(df.to_string(index=False))
        else:
            print("❌ No new patients found with 'NEW_' prefix")
            
            # Check if there are any patients without the standard ID format
            print("\n🔍 Checking for other recently added patients...")
            
            # Get the most recent patients by checking the last few records
            recent_query = """
            SELECT 
                DESYNPUF_ID as Patient_ID,
                AGE as Age,
                CASE WHEN GENDER = 1 THEN 'Male' ELSE 'Female' END as Gender,
                RISK_30D as Risk_30D,
                RISK_LABEL as Risk_Level,
                TOP_3_FEATURES as Top_Features
            FROM risk_training 
            WHERE RISK_30D IS NOT NULL
            ORDER BY DESYNPUF_ID DESC
            LIMIT 10
            """
            
            recent_df = pd.read_sql_query(recent_query, conn)
            print("📋 Most recent 10 patients:")
            print(recent_df.to_string(index=False))
        
        # Check total count again
        total_count = pd.read_sql_query("SELECT COUNT(*) as total FROM risk_training", conn)
        print(f"\n📊 Total patients in database: {total_count['total'].iloc[0]:,}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    find_new_patients()
