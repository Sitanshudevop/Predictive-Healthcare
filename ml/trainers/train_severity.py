"""Train Severity Scorer — GradientBoostingRegressor."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import json, time
from utils import update_registry, ARTIFACTS_DIR

DATASETS = Path(__file__).parent.parent / "datasets" / "severity"

def train():
    print("\n[TRAIN] Severity Scorer")
    csv_path = DATASETS / "severity.csv"
    if not csv_path.exists():
        sys.path.insert(0, str(Path(__file__).parent.parent / "data_loaders"))
        from severity_generator import generate_severity_data
        DATASETS.mkdir(parents=True, exist_ok=True)
        df = generate_severity_data()
        df.to_csv(csv_path, index=False)
        print("  Generated severity dataset")

    df = pd.read_csv(csv_path)
    feature_cols = [c for c in df.columns if c != "severity_score"]
    X = df[feature_cols].values
    y = df["severity_score"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"  MAE: {mae:.4f}, R2: {r2:.4f}")

    # Save regression metrics
    metrics = {
        "model_name": "severity",
        "mae": round(float(mae), 4),
        "r2": round(float(r2), 4),
        "training_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "feature_list": feature_cols,
    }
    with open(ARTIFACTS_DIR / "severity_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    artifact_path = ARTIFACTS_DIR / "severity_v1.pkl"
    joblib.dump(model, artifact_path)
    update_registry("severity", "severity_v1.pkl", 1)
    print(f"  [OK] Saved to {artifact_path}")

if __name__ == "__main__":
    train()
