import pandas as pd
"""
chronic_cols = [
    "ALZHEIMER","HEARTFAILURE","CANCER","PULMONARY",
    "OSTEOPOROSIS","RHEUMATOID","STROKE","RENAL_DISEASE"
]

def preprocess_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Claims flag
    df["CLAIMS_FLAG"] = (df["TOTAL_CLAIMS_COST"].fillna(0) > 0).astype(int)
    # Comorbidity count
    df["COMOR_COUNT"] = df[chronic_cols].sum(axis=1)
    return df

feature_cols = [
    "AGE", "TOTAL_CLAIMS_COST", "IN_ADM", "OUT_VISITS", "RX_ADH",
    "CLAIMS_FLAG", "COMOR_COUNT"
] + chronic_cols + [
    "BP_S", "GLUCOSE", "HbA1c","CHOLESTEROL"
]

target_cols = ["RISK_30D", "RISK_60D", "RISK_90D"]

"""


chronic_cols = [
    "ALZHEIMER","HEARTFAILURE","CANCER","PULMONARY",
    "OSTEOPOROSIS","RHEUMATOID","STROKE","RENAL_DISEASE"
]

feature_cols = [
    "AGE", "TOTAL_CLAIMS_COST", "IN_ADM", "OUT_VISITS", "RX_ADH",
    "CLAIMS_FLAG", "COMOR_COUNT"
] + chronic_cols + ["BP_S", "GLUCOSE", "HbA1c","CHOLESTEROL"]

# Targets
target_cols = ["RISK_30D", "RISK_60D", "RISK_90D"]

def preprocess_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Ensure all column names are strings (fix for sklearn compatibility)
    df.columns = df.columns.astype(str)

    # Ensure needed columns exist (fill missing with 0 where appropriate)
    for c in chronic_cols:
        if c not in df: df[c] = 0

    for c in ["TOTAL_CLAIMS_COST","IN_ADM","OUT_VISITS","RX_ADH","BP_S","GLUCOSE","HbA1c","CHOLESTEROL","AGE"]:
        if c not in df: df[c] = 0

    # Claims flag
    df["TOTAL_CLAIMS_COST"] = pd.to_numeric(df["TOTAL_CLAIMS_COST"], errors="coerce").fillna(0)
    df["CLAIMS_FLAG"] = (df["TOTAL_CLAIMS_COST"] > 0).astype(int)

    # Comorbidity count
    df["COMOR_COUNT"] = df[chronic_cols].sum(axis=1)

    return df

