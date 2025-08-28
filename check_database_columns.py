#!/usr/bin/env python3
"""
Check Database Columns
"""

import sqlite3

def check_columns():
    """Check what columns exist in the database"""
    print("🔍 Checking Database Columns")
    print("="*40)
    
    try:
        conn = sqlite3.connect('risk_data.db')
        cursor = conn.cursor()
        
        # Get table structure
        cursor.execute("PRAGMA table_info(risk_training)")
        columns = cursor.fetchall()
        
        print(f"📋 Table 'risk_training' has {len(columns)} columns:")
        print("-" * 40)
        
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            print(f"{col_id:2d}. {col_name:<20} ({col_type})")
        
        print("\n" + "="*40)
        print("📊 SAMPLE DATA (First 3 records)")
        print("="*40)
        
        # Get sample data
        cursor.execute("SELECT * FROM risk_training LIMIT 3")
        rows = cursor.fetchall()
        
        if rows:
            # Get column names
            column_names = [description[0] for description in cursor.description]
            print("Columns:", column_names)
            print()
            
            for i, row in enumerate(rows, 1):
                print(f"Record {i}:")
                for j, value in enumerate(row):
                    print(f"  {column_names[j]}: {value}")
                print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_columns()
