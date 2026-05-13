"""Train Mental Health Risk Screener — GradientBoosting."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from utils import save_metrics, update_registry, ARTIFACTS_DIR

DATASETS = Path(__file__).parent.parent / "datasets" / "mental_health"

def train():
    print("\n[TRAIN] Mental Health Risk Screener")
    csv_path = DATASETS / "mental_health.csv"
    if not csv_path.exists():
        # Generate it
        sys.path.insert(0, str(Path(__file__).parent.parent / "data_loaders"))
        from mental_health_synth import generate_mental_health_data
        DATASETS.mkdir(parents=True, exist_ok=True)
        df = generate_mental_health_data()
        df.to_csv(csv_path, index=False)
        print("  Generated synthetic dataset")
    
    df = pd.read_csv(csv_path)
    feature_cols = [c for c in df.columns if c != "risk_label"]
    X = df[feature_cols].values
    y = df["risk_label"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("gb", GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42))
    ])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    save_metrics("mental_health", y_test, y_pred, feature_cols, str(csv_path),
                 extra={"note": "Synthetic dataset for academic purposes only"})
    
    artifact_path = ARTIFACTS_DIR / "mental_health_v1.pkl"
    joblib.dump(pipe, artifact_path)
    update_registry("mental_health", "mental_health_v1.pkl", 1)
    print(f"  [OK] Saved to {artifact_path}")

if __name__ == "__main__":
    train()
