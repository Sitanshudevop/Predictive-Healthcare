"""
ML Training Orchestrator — runs all trainers sequentially.

Usage:
    python ml/train_all.py                  # Train all models
    python ml/train_all.py --only diabetes,heart  # Train specific models
"""

import sys
import time
import argparse
from pathlib import Path

# Add ml/ to path
sys.path.insert(0, str(Path(__file__).parent))

TRAINERS = {
    "general": "trainers.train_general",
    "diabetes": "trainers.train_diabetes",
    "heart": "trainers.train_heart",
    "breast_cancer": "trainers.train_breast_cancer",
    "liver": "trainers.train_liver",
    "kidney": "trainers.train_kidney",
    "pneumonia": "trainers.train_pneumonia_cnn",
    "skin": "trainers.train_skin_mobilenet",
    "mental_health": "trainers.train_mental_health",
    "severity": "trainers.train_severity",
    "nlp_extractor": "trainers.train_nlp_extractor",
}


def main():
    parser = argparse.ArgumentParser(description="PHS ML Training Orchestrator")
    parser.add_argument("--only", type=str, default="", help="Comma-separated list of models to train")
    args = parser.parse_args()

    # Create artifacts directory
    artifacts_dir = Path(__file__).parent / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    if args.only:
        selected = [s.strip() for s in args.only.split(",")]
    else:
        selected = list(TRAINERS.keys())

    print("=" * 60)
    print("Predictive Healthcare System — ML Training Pipeline")
    print("=" * 60)
    print(f"Models to train: {', '.join(selected)}\n")

    results = {}
    total_start = time.time()

    for name in selected:
        if name not in TRAINERS:
            print(f"[WARN] Unknown model: {name}")
            results[name] = "UNKNOWN"
            continue

        start = time.time()
        try:
            module = __import__(TRAINERS[name], fromlist=["train"])
            module.train()
            elapsed = time.time() - start
            results[name] = f"OK ({elapsed:.1f}s)"
        except Exception as e:
            elapsed = time.time() - start
            results[name] = f"FAIL: {e}"
            print(f"  [ERROR] {name}: {e}")

    total_elapsed = time.time() - total_start

    print("\n" + "=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)
    for name, status in results.items():
        print(f"  {name:20s} : {status}")
    print(f"\nTotal time: {total_elapsed:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
