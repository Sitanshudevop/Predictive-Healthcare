"""
ML utility functions shared across trainers.
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Any

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
)


ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def save_metrics(
    model_name: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    feature_list: list[str],
    dataset_path: str = "",
    extra: dict = None,
) -> dict:
    """Compute and save metrics JSON + confusion matrix PNG."""
    labels = sorted(list(set(y_true) | set(y_pred)))
    
    avg = "binary" if len(labels) == 2 else "weighted"
    metrics = {
        "model_name": model_name,
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, average=avg, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, average=avg, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, average=avg, zero_division=0)), 4),
        "training_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "dataset_checksum": _file_hash(dataset_path) if dataset_path else "",
        "feature_list": feature_list,
        "num_classes": len(labels),
        "confusion_matrix_path": f"{model_name}_confusion.png",
    }
    if extra:
        metrics.update(extra)

    # Save metrics JSON
    metrics_path = ARTIFACTS_DIR / f"{model_name}_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    # Save confusion matrix plot
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(max(6, len(labels)), max(5, len(labels) * 0.8)))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"{model_name} — Confusion Matrix")
    plt.tight_layout()
    fig.savefig(str(ARTIFACTS_DIR / f"{model_name}_confusion.png"), dpi=100)
    plt.close(fig)

    print(f"  [METRICS] {model_name}: Acc={metrics['accuracy']}, F1={metrics['f1']}")
    return metrics


def update_registry(model_name: str, filename: str, version: int = 1):
    """Add or update an entry in registry.json."""
    registry_path = ARTIFACTS_DIR / "registry.json"
    if registry_path.exists():
        with open(registry_path, "r") as f:
            registry = json.load(f)
    else:
        registry = {}

    registry[model_name] = {
        "filename": filename,
        "version": version,
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)


def _file_hash(path: str) -> str:
    """Compute MD5 hash of a file for dataset versioning."""
    if not path or not Path(path).exists():
        return ""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
