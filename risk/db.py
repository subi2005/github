import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from risk.logger import logger
DATABASE_URL = "sqlite:///risk_data.db"


def get_engine():
    return create_engine(DATABASE_URL)

def load_data_from_db(table_name: str) -> pd.DataFrame:
    logger.info(f"Loading data from {table_name}")
    engine = get_engine()
    return pd.read_sql_table(table_name, con=engine)

def load_patient_data() -> pd.DataFrame:
    """Load patient data from the database"""
    logger.info("Loading patient data from database")
    engine = get_engine()
    try:
        # Try to load from beneficiary table first
        df = pd.read_sql_table("beneficiary", con=engine)
        logger.info(f"Loaded {len(df)} rows from beneficiary table")
        return df
    except Exception as e:
        logger.warning(f"Could not load from beneficiary table: {e}")
        # Fallback to CSV if database table doesn't exist
        df = pd.read_csv("data/risk_training.csv")
        logger.info(f"Loaded {len(df)} rows from CSV fallback")
        return df

def ensure_prediction_columns(table_name):
    """Ensure prediction-related columns exist in the table"""
    try:
        engine = get_engine()
        
        # Columns to add if they don't exist
        columns_to_add = [
            "RISK_30D INTEGER",
            "RISK_60D INTEGER", 
            "RISK_90D INTEGER",
            "RISK_LABEL TEXT",
            "TOP_3_FEATURES TEXT",
            "AI_RECOMMENDATIONS TEXT",
            "EMAIL TEXT"
        ]
        
        with engine.connect() as conn:
            for column_def in columns_to_add:
                column_name = column_def.split()[0]
                try:
                    # Check if column exists
                    query = text(f"SELECT {column_name} FROM {table_name} LIMIT 1")
                    conn.execute(query)
                except:
                    # Column doesn't exist, add it
                    alter_query = text(f"ALTER TABLE {table_name} ADD COLUMN {column_def}")
                    conn.execute(alter_query)
                    conn.commit()
                    logger.info(f"Added column {column_name} to {table_name}")
                
    except Exception as e:
        logger.error(f"Error ensuring prediction columns: {e}")
        raise

def update_predictions_in_db(df: pd.DataFrame, table_name: str):
    engine = get_engine()
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(
                text(f"""
                    UPDATE {table_name}
                    SET RISK_30D = :r30,
                        RISK_60D = :r60,
                        RISK_90D = :r90,
                        RISK_LABEL = :rlabel,
                        TOP_3_FEATURES = :features
                    WHERE DESYNPUF_ID = :pid
                """),
                {
                    "r30": int(row["RISK_30D"]),
                    "r60": int(row["RISK_60D"]),
                    "r90": int(row["RISK_90D"]),
                    "rlabel": row["RISK_LABEL"],
                    "features": row["TOP_3_FEATURES"],
                    "pid": row["DESYNPUF_ID"]
                }
            )
    logger.success("Predictions updated successfully in DB")

def update_predictions_in_db_bulk(df: pd.DataFrame, table_name: str):
    """Bulk update predictions in the database"""
    logger.info(f"Bulk updating predictions for {len(df)} records in {table_name}")
    engine = get_engine()
    
    # Ensure prediction columns exist
    ensure_prediction_columns(table_name)
    
    with engine.begin() as conn:
        for _, row in df.iterrows():
            try:
                conn.execute(
                    text(f"""
                        UPDATE {table_name}
                        SET RISK_30D = :r30,
                            RISK_60D = :r60,
                            RISK_90D = :r90,
                            RISK_LABEL = :rlabel,
                            TOP_3_FEATURES = :features
                        WHERE DESYNPUF_ID = :pid
                    """),
                    {
                        "r30": int(row["RISK_30D"]),
                        "r60": int(row["RISK_60D"]),
                        "r90": int(row["RISK_90D"]),
                        "rlabel": row["RISK_LABEL"],
                        "features": row["TOP_3_FEATURES"],
                        "pid": row["DESYNPUF_ID"]
                    }
                )
            except Exception as e:
                logger.warning(f"Failed to update row {row['DESYNPUF_ID']}: {e}")
                continue
    
    logger.success(f"Bulk update completed for {len(df)} records")

def create_table_from_csv(csv_path: str, table_name: str):
    """Create a SQLite table from CSV data"""
    logger.info(f"Creating table {table_name} from {csv_path}")
    engine = get_engine()
    
    try:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logger.success(f"Table {table_name} created with {len(df)} rows")
        return True
    except Exception as e:
        logger.error(f"Failed to create table {table_name}: {e}")
        return False

def update_patient_email(patient_id, email):
    """Update patient email address in the database"""
    try:
        engine = get_engine()
        
        # Update email for the patient
        update_query = text(f"""
            UPDATE risk_training 
            SET EMAIL = :email
            WHERE DESYNPUF_ID = :patient_id
        """)
        
        engine.execute(update_query, {
            "email": email,
            "patient_id": patient_id
        })
        
        logger.info(f"Email updated for patient {patient_id}: {email}")
        return True
        
    except Exception as e:
        logger.error(f"Error updating email for patient {patient_id}: {e}")
        return False

def get_patient_by_id(patient_id):
    """Get patient data by ID"""
    try:
        engine = get_engine()
        query = text(f"""
            SELECT * FROM risk_training 
            WHERE DESYNPUF_ID = :patient_id
        """)
        
        result = engine.execute(query, {"patient_id": patient_id})
        row = result.fetchone()
        
        if row:
            return dict(row)
        else:
            return None
            
    except Exception as e:
        logger.error(f"Error getting patient {patient_id}: {e}")
        return None
