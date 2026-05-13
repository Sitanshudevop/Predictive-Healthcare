"""
Dataset checker — verifies all required datasets are in place.
Usage: python ml/data_loaders/check_datasets.py
"""

from pathlib import Path

DATASETS_DIR = Path(__file__).resolve().parent.parent.parent / "datasets"

CHECKS = [
    ("general_symptoms", ["Training.csv", "Testing.csv"]),
    ("diabetes", ["diabetes.csv"]),
    ("heart", ["heart.csv"]),
    ("liver", ["indian_liver_patient.csv"]),
    ("kidney", ["kidney_disease.csv"]),
]

IMAGE_CHECKS = [
    ("pneumonia", "train", 100),
    ("skin_ham10000", None, 100),
]


def main():
    print("=" * 50)
    print("PHS Dataset Checker")
    print("=" * 50)
    all_ok = True

    for folder, files in CHECKS:
        for f in files:
            p = DATASETS_DIR / folder / f
            if p.exists():
                print(f"  [OK] {folder}/{f}")
            else:
                print(f"  [MISSING] {folder}/{f}")
                all_ok = False

    for folder, subfolder, min_count in IMAGE_CHECKS:
        base = DATASETS_DIR / folder
        if subfolder:
            base = base / subfolder
        imgs = list(base.rglob("*.jpg")) + list(base.rglob("*.png")) + list(base.rglob("*.jpeg"))
        if len(imgs) >= min_count:
            print(f"  [OK] {folder}: {len(imgs)} images found")
        else:
            print(f"  [MISSING] {folder}: only {len(imgs)} images (need {min_count}+)")
            all_ok = False

    print(f"\n{'ALL DATASETS READY' if all_ok else 'SOME DATASETS MISSING — run download_datasets.py'}")
    return all_ok


if __name__ == "__main__":
    main()
