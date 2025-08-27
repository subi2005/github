#!/usr/bin/env python3
"""
Database Setup Script for Risk Stratification Project
This script helps set up the SQLite database from CSV data.
"""

import os
import pandas as pd
from sqlalchemy import text
from risk.db import create_table_from_csv, get_engine
from risk.logger import logger

def setup_database():
    """Set up the SQLite database with training data"""
    logger.info("Setting up SQLite database...")
    
    # Check if data directory exists
    if not os.path.exists("data"):
        logger.error("Data directory not found. Please ensure you have a 'data' folder with your CSV files.")
        return False
    
    # Look for CSV files in the data directory
    csv_files = [f for f in os.listdir("data") if f.endswith('.csv')]
    
    if not csv_files:
        logger.error("No CSV files found in the data directory.")
        return False
    
    logger.info(f"Found CSV files: {csv_files}")
    
    # Create database tables from CSV files
    success_count = 0
    for csv_file in csv_files:
        table_name = csv_file.replace('.csv', '').lower()
        csv_path = os.path.join("data", csv_file)
        
        logger.info(f"Creating table '{table_name}' from '{csv_file}'...")
        if create_table_from_csv(csv_path, table_name):
            success_count += 1
    
    logger.success(f"Database setup completed. {success_count}/{len(csv_files)} tables created successfully.")
    
    # List all tables in the database
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result.fetchall()]
            logger.info(f"Tables in database: {tables}")
    except Exception as e:
        logger.warning(f"Could not list tables: {e}")
    
    return success_count > 0

def check_database():
    """Check the current state of the database"""
    logger.info("Checking database status...")
    
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                logger.success(f"Database is ready with {len(tables)} tables: {tables}")
                
                # Show sample data from each table
                for table in tables:
                    try:
                        df = pd.read_sql(f"SELECT * FROM {table} LIMIT 5", engine)
                        logger.info(f"Table '{table}' has {len(df)} sample rows")
                    except Exception as e:
                        logger.warning(f"Could not read from table '{table}': {e}")
            else:
                logger.warning("Database exists but has no tables. Run setup_database() to create tables.")
                
    except Exception as e:
        logger.error(f"Database check failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Risk Stratification Database Setup")
    print("=" * 40)
    
    # Check current database status
    check_database()
    
    # Ask user if they want to set up the database
    response = input("\nDo you want to set up the database from CSV files? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        setup_database()
        print("\nDatabase setup completed!")
    else:
        print("Database setup skipped.")
    
    print("\nYou can now run:")
    print("- train.py to train your models")
    print("- predict.py to make predictions")
