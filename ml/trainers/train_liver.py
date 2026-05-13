"""Train Liver Disease Predictor — RandomForest with SMOTE."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from utils import save_metrics, update_registry, ARTIFACTS_DIR

DATASETS = Path(__file__).parent.parent / "datasets" / "liver"

def train():
    print("\n[TRAIN] Liver Disease Predictor")
    csv_path = DATASETS / "indian_liver_patient.csv"
    if not csv_path.exists():
        print(f"  [SKIP] Dataset not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    
    # Identify gender column and encode
    gender_col = None
    for c in df.columns:
        if "gender" in c or "sex" in c:
            gender_col = c
            break
    if gender_col:
        df[gender_col] = LabelEncoder().fit_transform(df[gender_col].astype(str))
    
    # Identify target (usually last column or 'dataset' or 'selector')
    target_col = df.columns[-1]
    
    # Drop NaN
    df.dropna(inplace=True)
    
    feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols].values.astype(float)
    y = df[target_col].values.astype(int)
    
    # Convert to binary if needed (1=liver disease, 2=no disease -> 1=disease, 0=no)
    if set(np.unique(y)) == {1, 2}:
        y = (y == 1).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipe = ImbPipeline([
        ("scaler", StandardScaler()),
        ("smote", SMOTE(random_state=42)),
        ("rf", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
    ])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    save_metrics("liver", y_test, y_pred, feature_cols, str(csv_path))
    
    artifact_path = ARTIFACTS_DIR / "liver_v1.pkl"
    joblib.dump(pipe, artifact_path)
    update_registry("liver", "liver_v1.pkl", 1)
    print(f"  [OK] Saved to {artifact_path}")

if __name__ == "__main__":
    train()
