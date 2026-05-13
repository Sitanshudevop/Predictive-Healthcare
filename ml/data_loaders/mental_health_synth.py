"""
Mental Health Synthetic Dataset Generator.

Generates 5000 rows of realistic PHQ-9 + GAD-7 + lifestyle data.
This is SYNTHETIC data for ACADEMIC purposes — not clinical data.

Rules:
- PHQ-9: 9 items scored 0-3 (depression screening)
- GAD-7: 7 items scored 0-3 (anxiety screening)
- Age: 18-65
- Sleep hours: 3-12
- Stress level: 1-10
- Labels: 0=low risk, 1=moderate risk, 2=high risk

Labeling rules with noise:
- PHQ-9 total < 10 AND GAD-7 total < 8 AND stress < 5 => low
- PHQ-9 total 10-19 OR GAD-7 8-14 OR stress 5-7 => moderate
- PHQ-9 total >= 20 OR GAD-7 >= 15 OR stress >= 8 => high
- 10% label noise added for realism
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_mental_health_data(n=5000, seed=42):
    rng = np.random.RandomState(seed)
    rows = []

    for _ in range(n):
        # Generate base risk profile
        profile = rng.choice(["low", "moderate", "high"], p=[0.4, 0.35, 0.25])

        if profile == "low":
            phq9 = [rng.randint(0, 2) for _ in range(9)]
            gad7 = [rng.randint(0, 1) for _ in range(7)]
            age = rng.randint(18, 65)
            sleep = round(rng.uniform(6, 9), 1)
            stress = rng.randint(1, 5)
        elif profile == "moderate":
            phq9 = [rng.randint(0, 3) for _ in range(9)]
            gad7 = [rng.randint(0, 3) for _ in range(7)]
            age = rng.randint(18, 65)
            sleep = round(rng.uniform(4, 8), 1)
            stress = rng.randint(4, 8)
        else:
            phq9 = [rng.randint(1, 3) for _ in range(9)]
            gad7 = [rng.randint(1, 3) for _ in range(7)]
            age = rng.randint(18, 65)
            sleep = round(rng.uniform(3, 6), 1)
            stress = rng.randint(7, 10)

        phq9_total = sum(phq9)
        gad7_total = sum(gad7)

        # Determine label with rules
        if phq9_total >= 20 or gad7_total >= 15 or stress >= 8:
            label = 2
        elif phq9_total >= 10 or gad7_total >= 8 or stress >= 5:
            label = 1
        else:
            label = 0

        # Add 10% noise
        if rng.random() < 0.10:
            label = rng.randint(0, 3)

        row = phq9 + gad7 + [age, sleep, stress, phq9_total, gad7_total, label]
        rows.append(row)

    cols = [f"phq9_{i+1}" for i in range(9)] + [f"gad7_{i+1}" for i in range(7)]
    cols += ["age", "sleep_hours", "stress_level", "phq9_total", "gad7_total", "risk_label"]

    df = pd.DataFrame(rows, columns=cols)
    return df


def main():
    dest = Path(__file__).resolve().parent.parent.parent / "datasets" / "mental_health"
    dest.mkdir(parents=True, exist_ok=True)
    df = generate_mental_health_data()
    df.to_csv(dest / "mental_health.csv", index=False)
    print(f"[OK] Generated {len(df)} rows -> {dest / 'mental_health.csv'}")
    print(f"  Label distribution: {df['risk_label'].value_counts().to_dict()}")


if __name__ == "__main__":
    main()
