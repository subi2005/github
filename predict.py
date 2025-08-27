"""
import pandas as pd
from risk.model import load_model, predict_batch

MODEL_PATH = "models/risk_model.pkl"

def main():
    bundle = load_model(MODEL_PATH)
    regressors = bundle["regressors"]

    df_new = pd.DataFrame([{
        "DESYNPUF_ID": "00070B63745BE497",
    "AGE": 65,
    "GENDER": 1,
    "RENAL_DISEASE":0,
    'PARTA':12,
    'PARTB':0,
    'HMO':0,
    'PARTD':0,
    "ALZHEIMER":0,
    "HEARTFAILURE":0,
    "CANCER":0,
    "PULMONARY":0,
    "OSTEOPOROSIS":0,
    "RHEUMATOID":0,
    "STROKE":0,
    "TOTAL_CLAIMS_COST":0,
    "IN_ADM":2,
    "OUT_VISITS":1,
    'BMI':23,
    'BP_S':120,
    'GLUCOSE':100,
    'HbA1c':4.2,
    'CHOLESTEROL':180,
    'ED_VISITS':0,
    'RX_ADH':0.6
    }])

    preds = predict_batch(df_new, regressors)
    print(preds)

if __name__ == "__main__":
    main()
"""
"""
import pandas as pd
from dotenv import load_dotenv
from risk.logger import logger
from risk.db import load_data_from_db, ensure_prediction_columns, update_predictions_in_db_bulk
from risk.model import predict_batch

if __name__ == "__main__":
    load_dotenv()
    table_name = "beneficiary5"

    # 1) Load data
    df = load_data_from_db(table_name)
    logger.info(f"Loaded {len(df)} rows from '{table_name}'")

    # 2) Predict in batch
    preds = predict_batch(df)  # DESYNPUF_ID, RISK_30D, RISK_60D, RISK_90D, RISK_LABEL, TOP_3_FEATURES

    # 3) Ensure target columns exist
    ensure_prediction_columns(table_name)

    # 4) Bulk update into the SAME table by DESYNPUF_ID
    update_predictions_in_db_bulk(preds, table_name)

    logger.info("Done.")
"""

from risk.model import load_model, predict_batch
from risk.db import load_data_from_db, update_predictions_in_db
from risk.logger import logger

if __name__ == "__main__":
    table_name = "risk_training"
    logger.info("Loading trained model...")
    regressors = load_model("models/risk_model.pkl")

    logger.info("Loading new data...")
    df = load_data_from_db(table_name)

    # Ensure prediction columns exist in the database
    from risk.db import ensure_prediction_columns
    ensure_prediction_columns(table_name)

    preds = predict_batch(df, regressors)

    update_predictions_in_db(preds, table_name)
