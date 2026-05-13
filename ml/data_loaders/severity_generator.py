"""
Severity Dataset Generator — curated symptom-set to urgency score mapping.
Generates ~1500 rows of symptom combinations with urgency scores 0-10.
"""

import numpy as np
import pandas as pd
from pathlib import Path

SYMPTOM_COLS = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing",
    "shivering", "chills", "joint_pain", "stomach_pain", "acidity",
    "ulcers_on_tongue", "muscle_wasting", "vomiting", "burning_micturition",
    "fatigue", "weight_gain", "anxiety", "cold_hands_and_feets",
    "mood_swings", "weight_loss", "restlessness", "lethargy",
    "patches_in_throat", "irregular_sugar_level", "cough",
    "high_fever", "sunken_eyes", "breathlessness", "sweating",
    "dehydration", "indigestion", "headache", "yellowish_skin",
    "dark_urine", "nausea", "loss_of_appetite", "pain_behind_the_eyes",
    "back_pain", "constipation", "abdominal_pain", "diarrhoea",
    "mild_fever", "yellow_urine", "yellowing_of_eyes", "acute_liver_failure",
    "fluid_overload", "swelling_of_stomach", "swelled_lymph_nodes",
    "malaise", "blurred_and_distorted_vision", "phlegm",
    "throat_irritation", "redness_of_eyes", "sinus_pressure",
    "runny_nose", "congestion", "chest_pain", "weakness_in_limbs",
    "fast_heart_rate", "pain_during_bowel_movements", "pain_in_anal_region",
    "bloody_stool", "irritation_in_anus", "neck_pain", "dizziness",
    "cramps", "bruising", "obesity", "swollen_legs",
    "swollen_blood_vessels", "puffy_face_and_eyes", "enlarged_thyroid",
    "brittle_nails", "swollen_extremeties", "excessive_hunger",
    "extra_marital_contacts", "drying_and_tingling_lips",
    "slurred_speech", "knee_pain", "hip_joint_pain",
    "muscle_weakness", "stiff_neck", "swelling_joints",
    "movement_stiffness", "spinning_movements", "loss_of_balance",
    "unsteadiness", "weakness_of_one_body_side", "loss_of_smell",
    "bladder_discomfort", "foul_smell_of_urine",
    "continuous_feel_of_urine", "passage_of_gases", "internal_itching",
    "toxic_look_(typhos)", "depression", "irritability",
    "muscle_pain", "altered_sensorium", "red_spots_over_body",
    "belly_pain", "abnormal_menstruation", "dischromic_patches",
    "watering_from_eyes", "increased_appetite", "polyuria",
    "family_history", "mucoid_sputum", "rusty_sputum",
    "lack_of_concentration", "visual_disturbances",
    "receiving_blood_transfusion", "receiving_unsterile_injections",
    "coma", "stomach_bleeding", "distention_of_abdomen",
    "history_of_alcohol_consumption", "blood_in_sputum",
    "prominent_veins_on_calf", "palpitations", "painful_walking",
    "pus_filled_pimples", "blackheads", "scurring",
    "skin_peeling", "silver_like_dusting", "small_dents_in_nails",
    "inflammatory_nails", "blister", "red_sore_around_nose",
    "yellow_crust_ooze"
]


def generate_severity_data(n=1500, seed=42):
    rng = np.random.RandomState(seed)
    rows = []

    # Emergency symptoms (score 8-10)
    emergency = ["chest_pain", "breathlessness", "coma", "slurred_speech",
                  "acute_liver_failure", "stomach_bleeding", "weakness_of_one_body_side"]
    # High symptoms (score 5-8)
    high = ["high_fever", "bloody_stool", "blood_in_sputum", "fast_heart_rate",
            "altered_sensorium", "fluid_overload", "yellowish_skin"]
    # Moderate (3-5)
    moderate = ["vomiting", "diarrhoea", "abdominal_pain", "joint_pain",
                "muscle_pain", "weight_loss", "dehydration"]
    # Mild (0-3)
    mild = ["itching", "skin_rash", "headache", "cough", "mild_fever",
            "runny_nose", "congestion", "acidity"]

    for _ in range(n):
        vec = np.zeros(len(SYMPTOM_COLS))
        num_symptoms = rng.randint(1, 8)
        base_score = 0

        # Pick symptom mix
        profile = rng.choice(["mild", "moderate", "high", "emergency"], p=[0.35, 0.30, 0.25, 0.10])

        if profile == "emergency":
            picks = rng.choice(emergency, size=min(2, len(emergency)), replace=False).tolist()
            extra = max(0, min(num_symptoms - 2, 3, len(high + moderate)))
            if extra > 0:
                picks += rng.choice(high + moderate, size=extra, replace=False).tolist()
            base_score = rng.uniform(8, 10)
        elif profile == "high":
            picks = rng.choice(high, size=min(2, len(high)), replace=False).tolist()
            extra = max(0, min(num_symptoms - 2, 4, len(moderate + mild)))
            if extra > 0:
                picks += rng.choice(moderate + mild, size=extra, replace=False).tolist()
            base_score = rng.uniform(5, 8)
        elif profile == "moderate":
            picks = rng.choice(moderate, size=min(2, len(moderate)), replace=False).tolist()
            extra = max(0, min(num_symptoms - 2, 4, len(mild)))
            if extra > 0:
                picks += rng.choice(mild, size=extra, replace=False).tolist()
            base_score = rng.uniform(3, 5)
        else:
            picks = rng.choice(mild, size=min(num_symptoms, len(mild)), replace=False).tolist()
            base_score = rng.uniform(0, 3)

        for s in picks:
            if s in SYMPTOM_COLS:
                vec[SYMPTOM_COLS.index(s)] = 1

        # Add noise
        score = np.clip(base_score + rng.normal(0, 0.5), 0, 10)
        rows.append(list(vec) + [round(score, 2)])

    cols = SYMPTOM_COLS + ["severity_score"]
    return pd.DataFrame(rows, columns=cols)


def main():
    dest = Path(__file__).resolve().parent.parent.parent / "datasets" / "severity"
    dest.mkdir(parents=True, exist_ok=True)
    df = generate_severity_data()
    df.to_csv(dest / "severity.csv", index=False)
    print(f"[OK] Generated {len(df)} rows -> {dest / 'severity.csv'}")


if __name__ == "__main__":
    main()
