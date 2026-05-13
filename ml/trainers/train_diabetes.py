"""Train Diabetes Predictor — LogisticRegression + RandomForest stacked."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from utils import save_metrics, update_registry, ARTIFACTS_DIR

DATASETS = Path(__file__).parent.parent / "datasets" / "diabetes"

def train():
    print("\n[TRAIN] Diabetes Predictor")
    csv_path = DATASETS / "diabetes.csv"
    if not csv_path.exists():
        print(f"  [SKIP] Dataset not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    feature_cols = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
    
    # Handle column name variations
    df.columns = [c.strip() for c in df.columns]
    available = [c for c in feature_cols if c in df.columns]
    if len(available) < 6:
        # Try lowercase
        df.columns = [c.lower() for c in df.columns]
        feature_cols = [c.lower() for c in feature_cols]
        available = [c for c in feature_cols if c in df.columns]

    target = "Outcome" if "Outcome" in df.columns else "outcome"
    X = df[available].values
    y = df[target].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Model 1: Logistic Regression
    lr_pipe = Pipeline([("scaler", StandardScaler()), ("lr", LogisticRegression(max_iter=1000, random_state=42))])
    lr_f1 = cross_val_score(lr_pipe, X_train, y_train, cv=5, scoring="f1").mean()
    
    # Model 2: Random Forest
    rf_pipe = Pipeline([("scaler", StandardScaler()), ("rf", RandomForestClassifier(n_estimators=100, random_state=42))])
    rf_f1 = cross_val_score(rf_pipe, X_train, y_train, cv=5, scoring="f1").mean()

    print(f"  LR F1: {lr_f1:.4f}, RF F1: {rf_f1:.4f}")
    
    best_pipe = rf_pipe if rf_f1 >= lr_f1 else lr_pipe
    best_name = "RandomForest" if rf_f1 >= lr_f1 else "LogisticRegression"
    print(f"  Best: {best_name}")
    
    best_pipe.fit(X_train, y_train)
    y_pred = best_pipe.predict(X_test)

    save_metrics("diabetes", y_test, y_pred, available, str(csv_path),
                 extra={"best_model": best_name, "lr_f1": round(lr_f1, 4), "rf_f1": round(rf_f1, 4)})
    
    artifact_path = ARTIFACTS_DIR / "diabetes_v1.pkl"
    joblib.dump(best_pipe, artifact_path)
    update_registry("diabetes", "diabetes_v1.pkl", 1)
    print(f"  [OK] Saved to {artifact_path}")

if __name__ == "__main__":
    train()
