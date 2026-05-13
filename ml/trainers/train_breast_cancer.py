"""Train Breast Cancer Predictor — SVM (RBF) with StandardScaler."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from utils import save_metrics, update_registry, ARTIFACTS_DIR

def train():
    print("\n[TRAIN] Breast Cancer Predictor")
    data = load_breast_cancer()
    X, y = data.data, data.target
    feature_names = list(data.feature_names)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(kernel="rbf", C=1.0, gamma="scale", probability=True, random_state=42))
    ])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    save_metrics("breast_cancer", y_test, y_pred, feature_names, "sklearn.datasets")
    
    artifact_path = ARTIFACTS_DIR / "breast_cancer_v1.pkl"
    joblib.dump(pipe, artifact_path)
    update_registry("breast_cancer", "breast_cancer_v1.pkl", 1)
    print(f"  [OK] Saved to {artifact_path}")

if __name__ == "__main__":
    train()
