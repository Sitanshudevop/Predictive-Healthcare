"""
Dataset Downloader — Downloads all required datasets using kagglehub and ucimlrepo.

Usage: python ml/data_loaders/download_datasets.py
"""

import os
import sys
import shutil
from pathlib import Path

DATASETS_DIR = Path(__file__).resolve().parent.parent.parent / "datasets"


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def download_general_symptoms():
    """Kaggle: Disease Prediction Using Machine Learning."""
    dest = DATASETS_DIR / "general_symptoms"
    ensure_dir(dest)
    if (dest / "Training.csv").exists():
        print("[SKIP] General symptoms already downloaded")
        return True
    try:
        import kagglehub
        path = kagglehub.dataset_download("kaushil268/disease-prediction-using-machine-learning")
        print(f"[INFO] Downloaded to: {path}")
        # Copy CSVs to dest
        src = Path(path)
        for f in src.rglob("*.csv"):
            shutil.copy2(f, dest / f.name)
            print(f"  -> Copied {f.name}")
        return True
    except Exception as e:
        print(f"[FAIL] General symptoms: {e}")
        print("  Manual: https://www.kaggle.com/datasets/kaushil268/disease-prediction-using-machine-learning")
        print(f"  Place Training.csv, Testing.csv into {dest}")
        return False


def download_diabetes():
    """Kaggle: Pima Indians Diabetes."""
    dest = DATASETS_DIR / "diabetes"
    ensure_dir(dest)
    if (dest / "diabetes.csv").exists():
        print("[SKIP] Diabetes already downloaded")
        return True
    try:
        import kagglehub
        path = kagglehub.dataset_download("uciml/pima-indians-diabetes-database")
        src = Path(path)
        for f in src.rglob("*.csv"):
            shutil.copy2(f, dest / "diabetes.csv")
            print(f"  -> Copied as diabetes.csv")
            return True
        return False
    except Exception as e:
        print(f"[FAIL] Diabetes: {e}")
        print("  Manual: https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database")
        print(f"  Place diabetes.csv into {dest}")
        return False


def download_heart():
    """UCI: Heart Disease (Cleveland)."""
    dest = DATASETS_DIR / "heart"
    ensure_dir(dest)
    if (dest / "heart.csv").exists():
        print("[SKIP] Heart already downloaded")
        return True
    try:
        from ucimlrepo import fetch_ucirepo
        heart = fetch_ucirepo(id=45)
        df = heart.data.original
        df.to_csv(dest / "heart.csv", index=False)
        print("  -> Saved heart.csv")
        return True
    except Exception as e:
        print(f"[FAIL] Heart: {e}")
        print("  Manual: https://archive.ics.uci.edu/dataset/45/heart+disease")
        print(f"  Place processed.cleveland.data into {dest}")
        return False


def download_liver():
    """UCI: Indian Liver Patient Dataset."""
    dest = DATASETS_DIR / "liver"
    ensure_dir(dest)
    if (dest / "indian_liver_patient.csv").exists():
        print("[SKIP] Liver already downloaded")
        return True
    try:
        from ucimlrepo import fetch_ucirepo
        liver = fetch_ucirepo(id=225)
        df = liver.data.original
        df.to_csv(dest / "indian_liver_patient.csv", index=False)
        print("  -> Saved indian_liver_patient.csv")
        return True
    except Exception as e:
        print(f"[FAIL] Liver: {e}")
        print("  Manual: https://archive.ics.uci.edu/dataset/225/ilpd+indian+liver+patient+dataset")
        print(f"  Place indian_liver_patient.csv into {dest}")
        return False


def download_kidney():
    """UCI: Chronic Kidney Disease."""
    dest = DATASETS_DIR / "kidney"
    ensure_dir(dest)
    if (dest / "kidney_disease.csv").exists():
        print("[SKIP] Kidney already downloaded")
        return True
    try:
        from ucimlrepo import fetch_ucirepo
        kidney = fetch_ucirepo(id=336)
        df = kidney.data.original
        df.to_csv(dest / "kidney_disease.csv", index=False)
        print("  -> Saved kidney_disease.csv")
        return True
    except Exception as e:
        print(f"[FAIL] Kidney: {e}")
        print("  Manual: https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease")
        print(f"  Place kidney_disease.csv into {dest}")
        return False


def download_pneumonia():
    """Kaggle: Chest X-Ray Pneumonia (large — ~1.2GB)."""
    dest = DATASETS_DIR / "pneumonia"
    ensure_dir(dest)
    if (dest / "train").exists():
        print("[SKIP] Pneumonia already downloaded")
        return True
    try:
        import kagglehub
        path = kagglehub.dataset_download("paultimothymooney/chest-xray-pneumonia")
        src = Path(path)
        # Find the chest_xray folder
        for d in src.rglob("chest_xray"):
            if d.is_dir():
                for split in ["train", "val", "test"]:
                    split_src = d / split
                    if split_src.exists():
                        shutil.copytree(split_src, dest / split, dirs_exist_ok=True)
                print("  -> Copied train/val/test splits")
                return True
        # If flat structure
        for split in ["train", "val", "test"]:
            split_src = src / split
            if split_src.exists():
                shutil.copytree(split_src, dest / split, dirs_exist_ok=True)
        print("  -> Copied pneumonia dataset")
        return True
    except Exception as e:
        print(f"[FAIL] Pneumonia: {e}")
        print("  Manual: https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia")
        print(f"  Place train/val/test folders into {dest}")
        return False


def download_skin():
    """Kaggle: HAM10000 Skin Cancer."""
    dest = DATASETS_DIR / "skin_ham10000"
    ensure_dir(dest)
    existing_imgs = list(dest.glob("*.jpg")) + list(dest.glob("*.png"))
    if len(existing_imgs) > 100:
        print(f"[SKIP] Skin already has {len(existing_imgs)} images")
        return True
    try:
        import kagglehub
        path = kagglehub.dataset_download("kmader/skin-cancer-mnist-ham10000")
        src = Path(path)
        # Copy metadata CSV
        for f in src.rglob("*.csv"):
            shutil.copy2(f, dest / f.name)
        # Copy images (limit to 2000)
        count = 0
        for f in src.rglob("*.jpg"):
            if count >= 2000:
                break
            shutil.copy2(f, dest / f.name)
            count += 1
        print(f"  -> Copied {count} images + metadata")
        return True
    except Exception as e:
        print(f"[FAIL] Skin: {e}")
        print("  Manual: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000")
        print(f"  Place images + HAM10000_metadata.csv into {dest}")
        return False


def setup_breast_cancer():
    """sklearn built-in — no download needed."""
    print("[OK] Breast cancer: uses sklearn.datasets (no download needed)")
    return True


def setup_mental_health():
    """Auto-generated synthetic dataset."""
    dest = DATASETS_DIR / "mental_health"
    ensure_dir(dest)
    print("[OK] Mental health: will be auto-generated during training")
    return True


def setup_severity():
    """Auto-generated curated severity CSV."""
    dest = DATASETS_DIR / "severity"
    ensure_dir(dest)
    print("[OK] Severity: will be auto-generated during training")
    return True


def main():
    print("=" * 60)
    print("PHS Dataset Downloader")
    print("=" * 60)
    print(f"Target directory: {DATASETS_DIR}\n")

    results = {}
    results["General Symptoms"] = download_general_symptoms()
    results["Diabetes"] = download_diabetes()
    results["Heart Disease"] = download_heart()
    results["Liver Disease"] = download_liver()
    results["Kidney Disease"] = download_kidney()
    results["Pneumonia X-Ray"] = download_pneumonia()
    results["Skin HAM10000"] = download_skin()
    results["Breast Cancer"] = setup_breast_cancer()
    results["Mental Health"] = setup_mental_health()
    results["Severity"] = setup_severity()

    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    for name, ok in results.items():
        status = "✓" if ok else "✗ MANUAL DOWNLOAD NEEDED"
        print(f"  {name}: {status}")

    failed = [k for k, v in results.items() if not v]
    if failed:
        print(f"\n[WARN] {len(failed)} dataset(s) need manual download.")
        print("Install kagglehub: pip install kagglehub")
        print("Install ucimlrepo: pip install ucimlrepo")
    else:
        print("\n[OK] All datasets ready!")


if __name__ == "__main__":
    main()
