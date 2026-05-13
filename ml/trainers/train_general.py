"""Train General Disease Predictor — Calibrated VotingClassifier (RF + XGBoost).

Improvements over v1:
- Hyperparameter regularization to prevent memorization
- CalibratedClassifierCV for realistic probability outputs
- Stratified K-Fold cross-validation for robust evaluation
- SMOTE for synthetic boundary samples (improves generalization)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.calibration import CalibratedClassifierCV
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from utils import save_metrics, update_registry, ARTIFACTS_DIR

DATASETS = Path(__file__).parent.parent / "datasets" / "general_symptoms"

def train():
    print("\n[TRAIN] General Disease Predictor (Calibrated v2)")
    train_path = DATASETS / "Training.csv"
    test_path = DATASETS / "Testing.csv"
    if not train_path.exists():
        print(f"  [SKIP] Dataset not found: {train_path}")
        return

    df_train = pd.read_csv(train_path)
    # Clean column names
    df_train.columns = [c.strip().lower().replace(" ", "_") for c in df_train.columns]
    
    target_col = "prognosis"
    if target_col not in df_train.columns:
        # Try last column
        target_col = df_train.columns[-1]
    
    # Drop unnamed/empty columns
    feature_cols = [c for c in df_train.columns if c != target_col and not c.startswith("unnamed")]
    X = df_train[feature_cols].values
    
    le = LabelEncoder()
    y = le.fit_transform(df_train[target_col].str.strip())

    # Apply SMOTE for synthetic boundary samples (improves generalization
    # even on balanced data by creating new decision boundary examples)
    print("  Applying SMOTE...")
    smote = SMOTE(random_state=42, k_neighbors=min(5, min(np.bincount(y)) - 1))
    X_resampled, y_resampled = smote.fit_resample(X, y)
    print(f"  Resampled: {X.shape[0]} -> {X_resampled.shape[0]} samples")

    # Regularized estimators to prevent memorization
    rf = RandomForestClassifier(
        n_estimators=80,
        max_depth=12,           # Prevent deep memorization trees
        min_samples_split=5,    # Require minimum samples to split
        min_samples_leaf=3,     # Require minimum samples in leaf
        max_features="sqrt",    # Feature subsampling for diversity
        random_state=42,
        n_jobs=-1,
    )
    xgb = XGBClassifier(
        n_estimators=80,
        max_depth=8,            # Prevent deep memorization
        learning_rate=0.1,
        subsample=0.8,          # Row subsampling
        colsample_bytree=0.8,   # Feature subsampling
        reg_alpha=0.1,          # L1 regularization
        reg_lambda=1.0,         # L2 regularization
        random_state=42,
        use_label_encoder=False,
        eval_metric="mlogloss",
        verbosity=0,
    )
    
    voting = VotingClassifier(
        estimators=[("rf", rf), ("xgb", xgb)],
        voting="soft"
    )
    
    # Wrap with CalibratedClassifierCV for realistic probability calibration
    print("  Training Calibrated VotingClassifier (RF + XGBoost)...")
    calibrated = CalibratedClassifierCV(voting, cv=3, method="sigmoid")
    calibrated.fit(X_resampled, y_resampled)

    # Evaluate BEFORE overriding classes_ (model outputs integer labels during eval)
    if test_path.exists():
        print("  Evaluating on holdout test set...")
        df_test = pd.read_csv(test_path)
        df_test.columns = [c.strip().lower().replace(" ", "_") for c in df_test.columns]
        test_feature_cols = [c for c in df_test.columns if c != target_col and not c.startswith("unnamed")]
        X_test = df_test[test_feature_cols].values
        y_test = le.transform(df_test[target_col].str.strip())
        y_pred = calibrated.predict(X_test)
    else:
        print("  Evaluating with 5-fold cross-validation...")
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        y_pred = cross_val_predict(calibrated, X_resampled, y_resampled, cv=skf)
        y_test = y_resampled

    y_pred_labels = le.inverse_transform(y_pred)
    y_test_labels = le.inverse_transform(y_test)

    save_metrics("general", y_test_labels, y_pred_labels, feature_cols, str(train_path))
    
    # NOW override classes_ with disease names for deployment-time readable predictions
    calibrated.classes_ = le.classes_
    
    # Save standalone model (what ml_loader expects)
    artifact_path = ARTIFACTS_DIR / "general_model_v1.pkl"
    joblib.dump(calibrated, artifact_path)
    
    # Also save bundled artifact with label encoder for reference
    bundle = {"model": calibrated, "label_encoder": le, "feature_cols": feature_cols}
    joblib.dump(bundle, ARTIFACTS_DIR / "general_v1.pkl")
    
    update_registry("general", "general_model_v1.pkl", 2)
    
    print(f"  [OK] Saved to {artifact_path}")

if __name__ == "__main__":
    train()
