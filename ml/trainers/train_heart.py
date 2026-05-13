"""Train Heart Disease Predictor — XGBoost with GridSearchCV."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from utils import save_metrics, update_registry, ARTIFACTS_DIR

DATASETS = Path(__file__).parent.parent / "datasets" / "heart"

def train():
    print("\n[TRAIN] Heart Disease Predictor")
    csv_path = DATASETS / "heart.csv"
    dat_path = DATASETS / "processed.cleveland.data"
    
    if csv_path.exists():
        df = pd.read_csv(csv_path)
    elif dat_path.exists():
        cols = ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal","target"]
        df = pd.read_csv(dat_path, names=cols, na_values="?")
        df.dropna(inplace=True)
    else:
        print(f"  [SKIP] Dataset not found")
        return

    df.columns = [c.strip().lower() for c in df.columns]
    
    # Identify target column
    target_col = None
    for candidate in ["target", "num", "condition", "goal"]:
        if candidate in df.columns:
            target_col = candidate
            break
    if target_col is None:
        target_col = df.columns[-1]
    
    feature_cols = [c for c in df.columns if c != target_col][:13]
    X = df[feature_cols].values.astype(float)
    y = (df[target_col].values > 0).astype(int)  # Binary: 0 = no disease, 1 = disease

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("xgb", XGBClassifier(use_label_encoder=False, eval_metric="logloss", verbosity=0, random_state=42))
    ])
    
    param_grid = {
        "xgb__n_estimators": [50, 100],
        "xgb__max_depth": [3, 5],
        "xgb__learning_rate": [0.1, 0.2],
    }
    
    grid = GridSearchCV(pipe, param_grid, cv=3, scoring="f1", n_jobs=-1, verbose=0)
    grid.fit(X_train, y_train)
    
    print(f"  Best params: {grid.best_params_}")
    y_pred = grid.best_estimator_.predict(X_test)

    save_metrics("heart", y_test, y_pred, feature_cols, str(csv_path if csv_path.exists() else dat_path))
    
    artifact_path = ARTIFACTS_DIR / "heart_v1.pkl"
    joblib.dump(grid.best_estimator_, artifact_path)
    update_registry("heart", "heart_v1.pkl", 1)
    print(f"  [OK] Saved to {artifact_path}")

if __name__ == "__main__":
    train()
