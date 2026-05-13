"""Train Kidney Disease Predictor — DecisionTree + RandomForest, serve RF."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from utils import save_metrics, update_registry, ARTIFACTS_DIR

DATASETS = Path(__file__).parent.parent / "datasets" / "kidney"

def train():
    print("\n[TRAIN] Kidney Disease Predictor")
    csv_path = DATASETS / "kidney_disease.csv"
    if not csv_path.exists():
        print(f"  [SKIP] Dataset not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    # Remove id column if present
    if "id" in df.columns:
        df.drop("id", axis=1, inplace=True)
    
    # Identify target
    target_col = None
    for c in ["classification", "class", "target", "ckd"]:
        if c in df.columns:
            target_col = c
            break
    if target_col is None:
        target_col = df.columns[-1]
    
    # Encode categorical columns
    le_dict = {}
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le
    
    # Fill NaN with median
    df.fillna(df.median(numeric_only=True), inplace=True)
    
    feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols].values.astype(float)
    y = df[target_col].values.astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Train both, report both, serve RF
    dt = Pipeline([("scaler", StandardScaler()), ("dt", DecisionTreeClassifier(random_state=42))])
    rf = Pipeline([("scaler", StandardScaler()), ("rf", RandomForestClassifier(n_estimators=100, random_state=42))])
    
    dt_f1 = cross_val_score(dt, X_train, y_train, cv=5, scoring="f1").mean()
    rf_f1 = cross_val_score(rf, X_train, y_train, cv=5, scoring="f1").mean()
    print(f"  DT F1: {dt_f1:.4f}, RF F1: {rf_f1:.4f}")
    
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    save_metrics("kidney", y_test, y_pred, feature_cols, str(csv_path),
                 extra={"dt_f1": round(dt_f1, 4), "rf_f1": round(rf_f1, 4)})
    
    artifact_path = ARTIFACTS_DIR / "kidney_v1.pkl"
    joblib.dump(rf, artifact_path)
    update_registry("kidney", "kidney_v1.pkl", 1)
    print(f"  [OK] Saved to {artifact_path}")

if __name__ == "__main__":
    train()
