"""
import pandas as pd
from sklearn.model_selection import train_test_split
from risk.preprocess import preprocess_features, feature_cols, target_cols
from risk.model import train_model, save_model
from sklearn.metrics import mean_absolute_error, r2_score

DATA_PATH = "data/risk_training.csv"

def main():
    df = pd.read_csv(DATA_PATH)
    df = preprocess_features(df)

    X = df[feature_cols]
    y = df[target_cols]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    regressors = train_model(X_train, y_train)

    # Quick evaluation
    for col in target_cols:
        preds = regressors[col].predict(X_test)
        mae = mean_absolute_error(y_test[col], preds)
        r2 = r2_score(y_test[col], preds)
        print(f"--- {col} --- MAE={mae:.3f}, R²={r2:.3f}")

    save_model(regressors)
    print("Model trained and saved.")

if __name__ == "__main__":
    main()
"""
"""
import mlflow
import mlflow.sklearn
import pickle
from risk.preprocess import preprocess_features
from risk.model import build_regressors
from risk.db import load_patient_data
from loguru import logger

def train_and_log(model_path="models/risk_model.pkl"):
    logger.info("Loading data from DB...")
    df = load_patient_data()

    df_proc = preprocess_features(df)
    X, y, feature_cols, target_cols = build_regressors.prepare_data(df_proc)

    regressors = build_regressors.train(X, y, target_cols)

    # Save pickle
    with open(model_path, "wb") as f:
        pickle.dump({"regressors": regressors, "feature_cols": feature_cols}, f)
    logger.info(f"Model saved at {model_path}")

    # Log to MLflow
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("risk_modeling")

    with mlflow.start_run():
        for col in target_cols:
            model = regressors[col]
            mlflow.sklearn.log_model(model, artifact_path=f"regressor_{col}")
        mlflow.log_param("features", feature_cols)
        mlflow.log_artifact(model_path, artifact_path="pickles")
        logger.info(" Model logged to MLflow")

    return regressors
"""
"""
import os
import pandas as pd
from dotenv import load_dotenv
from risk.logger import logger
from risk.model import train_model
from risk.db import load_data_from_db

if __name__ == "__main__":
    load_dotenv()
    table_name = "beneficiary5"

    try:
        df = load_data_from_db(table_name)
        logger.info(f"Loaded {len(df)} rows from DB.")
    except Exception as e:
        logger.warning(f"DB load failed: {e}. Falling back to CSV.")
        df = pd.read_csv("data/risk_training.csv")
        logger.info(f"Loaded {len(df)} rows from CSV.")

    os.makedirs("models", exist_ok=True)
    train_model(df)
"""

import pandas as pd
from risk.model import train_models, save_model
from risk.db import load_data_from_db
from risk.logger import logger

if __name__ == "__main__":
    table_name = "risk_training"
    logger.info("Loading data for training...")
    df = load_data_from_db(table_name)
    regressors = train_models(df)
    save_model(regressors, "models/risk_model.pkl")
    logger.success("Model trained & saved")
