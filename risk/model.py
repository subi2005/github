"""
import numpy as np
import pandas as pd
import shap
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from .preprocess import preprocess_features, feature_cols, target_cols

# Risk label assignment
def assign_label(score):
    if score >= 85:
        return "Very High Risk"
    elif score >= 60:
        return "High Risk"
    elif score >= 40:
        return "Moderate Risk"
    elif score >= 20:
        return "Low Risk"
    else:
        return "Very Low Risk"

# Train model
def train_model(X_train, y_train):
    regressors = {}
    for col in target_cols:
        reg = Pipeline([
            ("scaler", StandardScaler()),
            ("rf", RandomForestRegressor(
                n_estimators=50,
                max_depth=4,
                min_samples_leaf=50,
                min_samples_split=20,
                max_features="log2",
                random_state=42
            ))
        ])
        reg.fit(X_train, y_train[col])
        regressors[col] = reg
    return regressors

# Predict batch
def predict_batch(df_in, regressors):
    df_proc = preprocess_features(df_in.copy())
    preds = pd.DataFrame({"DESYNPUF_ID": df_proc["DESYNPUF_ID"]})

    for col in target_cols:
        p = regressors[col].predict(df_proc[feature_cols])
        preds[col] = np.clip(np.round(p), 0, 100).astype(int)

    # SHAP on 30D risk
    model_30d = regressors["RISK_30D"].named_steps["rf"]
    X_transformed = regressors["RISK_30D"].named_steps["scaler"].transform(df_proc[feature_cols])

    explainer = shap.TreeExplainer(model_30d)
    shap_values = explainer.shap_values(X_transformed)

    top_features = []
    for i in range(len(df_proc)):
        contribs = dict(zip(feature_cols, shap_values[i]))
        sorted_feats = sorted(contribs.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
        formatted = ", ".join([f for f, _ in sorted_feats])
        top_features.append(formatted)

    preds["RISK_LABEL"] = preds["RISK_30D"].apply(assign_label)
    preds["TOP_3_FEATURES"] = top_features
    return preds

# Save / Load model
def save_model(regressors, path="models/risk_model.pkl"):
    bundle = {
        "regressors": regressors,
        "feature_cols": feature_cols,
        "target_cols": target_cols,
        "assign_label": assign_label,
        "preprocess_features": preprocess_features
    }
    with open(path, "wb") as f:
        pickle.dump(bundle, f)

def load_model(path="models/risk_model.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)
"""
import numpy as np
import pandas as pd
import shap
import pickle
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from risk.preprocess import preprocess_features, feature_cols, target_cols

regressors = {}

def train_models(df: pd.DataFrame):
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, r2_score

    df = preprocess_features(df)
    X = df[feature_cols]
    y = df[target_cols]
    
    # Convert to numpy arrays to avoid column name issues with sklearn
    X = X.values
    y = y.values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    for i, col in enumerate(target_cols):
        reg = Pipeline([
            ("scaler", StandardScaler()),
            ("rf", RandomForestRegressor(
                n_estimators=50, max_depth=4, min_samples_leaf=50,
                min_samples_split=20, max_features="log2", random_state=42
            ))
        ])
        reg.fit(X_train, y_train[:, i])
        regressors[col] = reg

        preds = reg.predict(X_test)
        mae = mean_absolute_error(y_test[:, i], preds)
        r2 = r2_score(y_test[:, i], preds)
        print(f"{col} → MAE={mae:.3f}, R²={r2:.3f}")

    return regressors

def save_model(regressors, path="models/risk_model.pkl"):
    with open(path, "wb") as f:
        pickle.dump(regressors, f)

def load_model(path="models/risk_model.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)

def assign_label(score):
    if score >= 85:
        return "Very High Risk"
    elif score >= 60:
        return "High Risk"
    elif score >= 40:
        return "Moderate Risk"
    elif score >= 20:
        return "Low Risk"
    else:
        return "Very Low Risk"

def predict_batch(df_in, regressors):
    df_proc = preprocess_features(df_in.copy())
    preds = pd.DataFrame({"DESYNPUF_ID": df_proc["DESYNPUF_ID"]})

    # Convert feature columns to numpy array to avoid column name issues
    X = df_proc[feature_cols].values

    for col in target_cols:
        p = regressors[col].predict(X)
        preds[col] = np.clip(np.round(p), 0, 100).astype(int)

    # For SHAP analysis, we need to use the feature names
    model_30d = regressors["RISK_30D"].named_steps["rf"]
    X_transformed = regressors["RISK_30D"].named_steps["scaler"].transform(X)
    explainer = shap.TreeExplainer(model_30d)
    shap_values = explainer.shap_values(X_transformed)

    top_features = []
    for i in range(len(df_proc)):
        contribs = dict(zip(feature_cols, shap_values[i]))
        sorted_feats = sorted(contribs.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
        formatted = ", ".join([f for f, _ in sorted_feats])
        top_features.append(formatted)

    preds["RISK_LABEL"] = preds["RISK_30D"].apply(assign_label)
    preds["TOP_3_FEATURES"] = top_features

    # Add AI recommendations
    from risk.recommendations import get_ai_recommendations
    
    ai_recommendations = []
    for i, row in preds.iterrows():
        # Create patient data dictionary for recommendations
        patient_data = {
            'RISK_30D': row['RISK_30D'],
            'RISK_60D': row['RISK_60D'],
            'RISK_90D': row['RISK_90D']
        }
        
        # Add original patient data if available
        if i < len(df_proc):
            for col in df_proc.columns:
                if col not in patient_data:
                    patient_data[col] = df_proc.iloc[i][col]
        
        recommendations = get_ai_recommendations(patient_data, row['TOP_3_FEATURES'])
        ai_recommendations.append(recommendations)
    
    preds["AI_RECOMMENDATIONS"] = ai_recommendations

    return preds
