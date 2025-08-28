#!/usr/bin/env python3
"""
Check if test patient was saved to database
"""

import sqlite3
import pandas as pd

def check_saved_patient():
    """Check if the test patient was saved"""
    print("🔍 Checking if test patient was saved to database")
    print("="*50)
    
    try:
        conn = sqlite3.connect('risk_data.db')
        
        # Check for any NEW_ patients
        query = """
        SELECT 
            DESYNPUF_ID as Patient_ID,
            AGE as Age,
            CASE WHEN GENDER = 1 THEN 'Male' ELSE 'Female' END as Gender,
            RISK_30D as Risk_30D,
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
            print(f"✅ Found {len(df)} new patients in database:")
            print("-" * 50)
            print(df.to_string(index=False))
        else:
            print("❌ No NEW_ patients found in database")
            
            # Check total count
            total_count = pd.read_sql_query("SELECT COUNT(*) as total FROM risk_training", conn)
            print(f"\n📊 Total patients in database: {total_count['total'].iloc[0]:,}")
            
            # Check recent additions
            print("\n🔍 Checking most recent patients...")
            recent_query = """
            SELECT 
                DESYNPUF_ID as Patient_ID,
                AGE as Age,
                CASE WHEN GENDER = 1 THEN 'Male' ELSE 'Female' END as Gender,
                RISK_30D as Risk_30D,
                RISK_LABEL as Risk_Level
            FROM risk_training 
            ORDER BY DESYNPUF_ID DESC
            LIMIT 10
            """
            
            recent_df = pd.read_sql_query(recent_query, conn)
            print("📋 Most recent 10 patients:")
            print(recent_df.to_string(index=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_saved_patient()
