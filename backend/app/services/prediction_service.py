"""
Prediction service — handles model inference for all prediction types.
No auth required — predictions are stored with optional session_id.
"""

import json
import logging
from pathlib import Path
from typing import Optional

import numpy as np
from sqlalchemy.orm import Session

from app.ml_loader import model_registry
from app.core.config import get_settings
from app.models.prediction import PredictionHistory

logger = logging.getLogger(__name__)
settings = get_settings()

# ─── Synonym mapping: NLP-extracted symptom → model feature column name ───
# The general model was trained on Kaggle's symptom dataset which uses
# specific column naming conventions. The NLP extractor uses natural-
# language names. This map bridges the two.
SYMPTOM_SYNONYM_MAP = {
    # Spelling variants (US vs UK / Kaggle conventions)
    "diarrhea": "diarrhoea",
    "yellowish_skin": "yellowish_skin",  # identity (already correct)
    "yellow_skin": "yellowish_skin",
    "jaundice": "yellowish_skin",

    # Natural language → Kaggle column
    "shortness_of_breath": "breathlessness",
    "difficulty_breathing": "breathlessness",
    "fever": "high_fever",
    "low_grade_fever": "mild_fever",
    "continuous_fever": "high_fever",
    "intermittent_fever": "mild_fever",
    "night_fever": "mild_fever",
    "tiredness": "fatigue",
    "exhaustion": "fatigue",
    "weakness": "muscle_weakness",
    "body_aches": "muscle_pain",
    "stomach_ache": "stomach_pain",
    "belly_ache": "belly_pain",
    "tummy_pain": "stomach_pain",
    "throwing_up": "vomiting",
    "puking": "vomiting",
    "feeling_sick": "nausea",
    "queasy": "nausea",
    "loose_stools": "diarrhoea",
    "runny_stool": "diarrhoea",
    "rash": "skin_rash",
    "skin_rash": "skin_rash",
    "itchy": "itching",
    "scratching": "itching",
    "blurry_vision": "blurred_and_distorted_vision",
    "blurred_vision": "blurred_and_distorted_vision",
    "vision_problems": "visual_disturbances",
    "rapid_heartbeat": "fast_heart_rate",
    "palpitations": "palpitations",
    "irregular_heartbeat": "palpitations",
    "increased_thirst": "excessive_hunger",
    "thirst": "dehydration",
    "frequent_urination": "polyuria",
    "painful_urination": "burning_micturition",
    "burning_urination": "burning_micturition",
    "blood_in_urine": "spotting__urination",
    "dark_urine": "dark_urine",
    "sore_throat": "throat_irritation",
    "throat_pain": "throat_irritation",
    "runny_nose": "runny_nose",
    "nasal_congestion": "congestion",
    "stuffy_nose": "congestion",
    "sneezing": "continuous_sneezing",
    "cold": "chills",
    "chills": "chills",
    "shivering": "shivering",
    "sweating": "sweating",
    "excessive_sweating": "sweating",
    "night_sweats": "sweating",
    "weight_loss": "weight_loss",
    "weight_gain": "weight_gain",
    "loss_of_appetite": "loss_of_appetite",
    "increased_appetite": "increased_appetite",
    "swelling": "swollen_extremeties",
    "swollen_legs": "swollen_legs",
    "edema": "swollen_extremeties",
    "fluid_retention": "fluid_overload",
    "bloating": "swelling_of_stomach",
    "abdominal_bloating": "distention_of_abdomen",
    "abdominal_pain": "abdominal_pain",
    "chest_pain": "chest_pain",
    "chest_tightness": "chest_pain",
    "back_pain": "back_pain",
    "lower_back_pain": "back_pain",
    "upper_back_pain": "back_pain",
    "neck_pain": "neck_pain",
    "stiff_neck": "stiff_neck",
    "joint_pain": "joint_pain",
    "knee_pain": "knee_pain",
    "hip_pain": "hip_joint_pain",
    "muscle_pain": "muscle_pain",
    "headache": "headache",
    "migraine": "headache",
    "dizziness": "dizziness",
    "lightheadedness": "dizziness",
    "fainting": "dizziness",
    "confusion": "altered_sensorium",
    "disorientation": "altered_sensorium",
    "slurred_speech": "slurred_speech",
    "numbness": "weakness_of_one_body_side",
    "tingling": "drying_and_tingling_lips",
    "pins_and_needles": "drying_and_tingling_lips",
    "seizures": "coma",
    "anxiety": "anxiety",
    "depression": "depression",
    "mood_swings": "mood_swings",
    "irritability": "irritability",
    "restlessness": "restlessness",
    "insomnia": "restlessness",
    "lethargy": "lethargy",
    "malaise": "malaise",
    "cough": "cough",
    "dry_cough": "cough",
    "phlegm": "phlegm",
    "mucus": "mucoid_sputum",
    "coughing_blood": "blood_in_sputum",
    "wheezing": "breathlessness",
    "constipation": "constipation",
    "gas": "passage_of_gases",
    "flatulence": "passage_of_gases",
    "heartburn": "acidity",
    "acid_reflux": "acidity",
    "indigestion": "indigestion",
    "hemorrhoids": "pain_in_anal_region",
    "rectal_pain": "pain_in_anal_region",
    "anal_itching": "irritation_in_anus",
    "blood_in_stool": "bloody_stool",
    "black_stool": "bloody_stool",
    "rectal_bleeding": "bloody_stool",
    "hair_loss": "brittle_nails",
    "brittle_nails": "brittle_nails",
    "acne": "pus_filled_pimples",
    "pimples": "pus_filled_pimples",
    "blisters": "blister",
    "skin_peeling": "skin_peeling",
    "dry_skin": "skin_peeling",
    "skin_lesions": "red_spots_over_body",
    "red_eyes": "redness_of_eyes",
    "watery_eyes": "watering_from_eyes",
    "eye_pain": "pain_behind_the_eyes",
    "sensitivity_to_light": "visual_disturbances",
    "balance_problems": "loss_of_balance",
    "coordination_problems": "unsteadiness",
    "difficulty_walking": "painful_walking",
    "muscle_wasting": "muscle_wasting",
    "muscle_twitching": "muscle_weakness",
    "burning_sensation": "internal_itching",
    "lump": "swelled_lymph_nodes",
    "swollen_lymph_nodes": "swelled_lymph_nodes",
    "cold_hands": "cold_hands_and_feets",
    "cold_feet": "cold_hands_and_feets",
    "cold_hands_and_feet": "cold_hands_and_feets",
    "hot_flashes": "sweating",
    "concentration_difficulty": "lack_of_concentration",
    "brain_fog": "lack_of_concentration",
    "memory_loss": "lack_of_concentration",
    "chronic_fatigue": "fatigue",
    "obesity": "obesity",
    "sunken_eyes": "sunken_eyes",
    "dehydration": "dehydration",
    "high_blood_pressure": "swollen_blood_vessels",
    "nosebleed": "stomach_bleeding",
    "cramps": "cramps",
    "bruising": "bruising",
    "irregular_periods": "abnormal_menstruation",
    "menstrual_cramps": "abnormal_menstruation",
    "loss_of_smell": "loss_of_smell",
    "loss_of_taste": "loss_of_smell",
}


class PredictionService:
    """Centralized prediction service that interacts with the model registry."""

    def __init__(self):
        self.artifacts_dir = settings.ML_ARTIFACTS_DIR

    def _save_history(
        self,
        db: Session,
        model_name: str,
        input_data: dict,
        prediction: str,
        confidence: float = 0.0,
        top_k: list = None,
        severity_score: float = 0.0,
        recommendation: dict = None,
        image_filename: str = None,
        user_id: int = None,
    ) -> int:
        """Save prediction result to history."""
        record = PredictionHistory(
            user_id=user_id,
            model_name=model_name,
            input_data=input_data,
            prediction=prediction,
            confidence=confidence,
            top_k=top_k or [],
            severity_score=severity_score,
            recommendation=recommendation,
            image_filename=image_filename,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record.id

    def predict_general(self, symptoms: list[str], db: Session = None, user_id: int = None) -> dict:
        """General disease prediction using VotingClassifier."""
        model = model_registry.get_model("general", self.artifacts_dir)
        if model is None:
            return {"error": "General disease model not loaded"}

        # Load symptom columns
        meta = model_registry.get_metadata("general", self.artifacts_dir)
        feature_names = meta.get("feature_list", [])

        # Create binary feature vector with synonym resolution
        feature_vector = np.zeros(len(feature_names))
        matched_symptoms = []
        for symptom in symptoms:
            symptom_clean = symptom.strip().lower().replace(" ", "_")
            # Apply synonym mapping to resolve NLP names → model feature names
            mapped = SYMPTOM_SYNONYM_MAP.get(symptom_clean, symptom_clean)
            if mapped in feature_names:
                idx = feature_names.index(mapped)
                feature_vector[idx] = 1
                matched_symptoms.append(f"{symptom_clean}→{mapped}")
            elif symptom_clean in feature_names:
                idx = feature_names.index(symptom_clean)
                feature_vector[idx] = 1
                matched_symptoms.append(symptom_clean)
        
        logger.info(f"General predict: input={symptoms}, matched={matched_symptoms}, hits={int(feature_vector.sum())}")

        # Predict with probabilities
        X = feature_vector.reshape(1, -1)
        try:
            probas = model.predict_proba(X)[0]
            classes = model.classes_
            top_indices = np.argsort(probas)[::-1][:3]
            top_k = [
                {"disease": str(classes[i]), "confidence": round(float(probas[i]), 4)}
                for i in top_indices
            ]
            prediction = str(classes[top_indices[0]])
            confidence = float(probas[top_indices[0]])
        except Exception as e:
            logger.error(f"General prediction error: {e}")
            prediction = model.predict(X)[0]
            confidence = 0.0
            top_k = [{"disease": str(prediction), "confidence": confidence}]

        result = {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "top_k": top_k,
            "model_name": "general",
        }

        if db:
            report_id = self._save_history(
                db, "general", {"symptoms": symptoms},
                prediction, confidence, top_k, user_id=user_id
            )
            result["report_id"] = report_id

        return result

    def predict_diabetes(self, features: dict, db: Session = None, user_id: int = None) -> dict:
        """Diabetes prediction."""
        model = model_registry.get_model("diabetes", self.artifacts_dir)
        if model is None:
            return {"error": "Diabetes model not loaded"}

        feature_order = [
            "pregnancies", "glucose", "blood_pressure", "skin_thickness",
            "insulin", "bmi", "diabetes_pedigree_function", "age"
        ]
        X = np.array([[features[f] for f in feature_order]])

        try:
            prediction = int(model.predict(X)[0])
            probas = model.predict_proba(X)[0]
            confidence = float(probas[prediction])
        except Exception as e:
            logger.error(f"Diabetes prediction error: {e}")
            prediction = int(model.predict(X)[0])
            confidence = 0.0

        label = "Diabetic" if prediction == 1 else "Not Diabetic"
        result = {
            "prediction": label,
            "confidence": round(confidence, 4),
            "top_k": [
                {"disease": "Not Diabetic", "confidence": round(float(probas[0]), 4)},
                {"disease": "Diabetic", "confidence": round(float(probas[1]), 4)},
            ],
            "model_name": "diabetes",
        }

        if db:
            report_id = self._save_history(
                db, "diabetes", features, label, confidence, result["top_k"], user_id=user_id
            )
            result["report_id"] = report_id

        return result

    def predict_heart(self, features: dict, db: Session = None, user_id: int = None) -> dict:
        """Heart disease prediction."""
        model = model_registry.get_model("heart", self.artifacts_dir)
        if model is None:
            return {"error": "Heart disease model not loaded"}

        feature_order = [
            "age", "sex", "cp", "trestbps", "chol", "fbs",
            "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
        ]
        X = np.array([[features[f] for f in feature_order]])

        try:
            prediction = int(model.predict(X)[0])
            probas = model.predict_proba(X)[0]
            confidence = float(probas[min(prediction, len(probas) - 1)])
        except Exception as e:
            logger.error(f"Heart prediction error: {e}")
            prediction = int(model.predict(X)[0])
            confidence = 0.0

        label = "Heart Disease Detected" if prediction >= 1 else "No Heart Disease"
        result = {
            "prediction": label,
            "confidence": round(confidence, 4),
            "top_k": [{"disease": label, "confidence": round(confidence, 4)}],
            "model_name": "heart",
        }

        if db:
            report_id = self._save_history(
                db, "heart", features, label, confidence, result["top_k"], user_id=user_id
            )
            result["report_id"] = report_id

        return result

    def predict_breast_cancer(self, features: list[float], db: Session = None, user_id: int = None) -> dict:
        """Breast cancer prediction using 30 Wisconsin features."""
        model = model_registry.get_model("breast_cancer", self.artifacts_dir)
        if model is None:
            return {"error": "Breast cancer model not loaded"}

        X = np.array([features])

        try:
            prediction = int(model.predict(X)[0])
            probas = model.predict_proba(X)[0]
            confidence = float(probas[prediction])
        except Exception as e:
            logger.error(f"Breast cancer prediction error: {e}")
            prediction = int(model.predict(X)[0])
            confidence = 0.0

        label = "Malignant" if prediction == 0 else "Benign"
        result = {
            "prediction": label,
            "confidence": round(confidence, 4),
            "top_k": [
                {"disease": "Malignant", "confidence": round(float(probas[0]), 4)},
                {"disease": "Benign", "confidence": round(float(probas[1]), 4)},
            ],
            "model_name": "breast_cancer",
        }

        if db:
            report_id = self._save_history(
                db, "breast_cancer", {"features": features}, label, confidence, result["top_k"], user_id=user_id
            )
            result["report_id"] = report_id

        return result

    def predict_liver(self, features: dict, db: Session = None, user_id: int = None) -> dict:
        """Liver disease prediction."""
        model = model_registry.get_model("liver", self.artifacts_dir)
        if model is None:
            return {"error": "Liver disease model not loaded"}

        feature_order = [
            "age", "gender", "total_bilirubin", "direct_bilirubin",
            "alkaline_phosphotase", "alamine_aminotransferase",
            "aspartate_aminotransferase", "total_proteins",
            "albumin", "albumin_and_globulin_ratio"
        ]
        X = np.array([[features[f] for f in feature_order]])

        try:
            prediction = int(model.predict(X)[0])
            probas = model.predict_proba(X)[0]
            confidence = float(probas[prediction])
        except Exception as e:
            logger.error(f"Liver prediction error: {e}")
            prediction = int(model.predict(X)[0])
            confidence = 0.0

        label = "Liver Disease Detected" if prediction == 1 else "No Liver Disease"
        result = {
            "prediction": label,
            "confidence": round(confidence, 4),
            "top_k": [{"disease": label, "confidence": round(confidence, 4)}],
            "model_name": "liver",
        }

        if db:
            report_id = self._save_history(
                db, "liver", features, label, confidence, result["top_k"], user_id=user_id
            )
            result["report_id"] = report_id

        return result

    def predict_kidney(self, features: dict, db: Session = None, user_id: int = None) -> dict:
        """Chronic kidney disease prediction."""
        model = model_registry.get_model("kidney", self.artifacts_dir)
        if model is None:
            return {"error": "Kidney disease model not loaded"}

        feature_order = [
            "age", "blood_pressure", "specific_gravity", "albumin", "sugar",
            "red_blood_cells", "pus_cell", "pus_cell_clumps", "bacteria",
            "blood_glucose_random", "blood_urea", "serum_creatinine",
            "sodium", "potassium", "hemoglobin", "packed_cell_volume",
            "white_blood_cell_count", "red_blood_cell_count",
            "hypertension", "diabetes_mellitus", "coronary_artery_disease",
            "appetite", "pedal_edema", "anemia"
        ]
        X = np.array([[features[f] for f in feature_order]])

        try:
            prediction = int(model.predict(X)[0])
            probas = model.predict_proba(X)[0]
            confidence = float(probas[prediction])
        except Exception as e:
            logger.error(f"Kidney prediction error: {e}")
            prediction = int(model.predict(X)[0])
            confidence = 0.0

        label = "Chronic Kidney Disease" if prediction == 1 else "No Kidney Disease"
        result = {
            "prediction": label,
            "confidence": round(confidence, 4),
            "top_k": [{"disease": label, "confidence": round(confidence, 4)}],
            "model_name": "kidney",
        }

        if db:
            report_id = self._save_history(
                db, "kidney", features, label, confidence, result["top_k"], user_id=user_id
            )
            result["report_id"] = report_id

        return result

    def predict_mental_health(self, features: dict, db: Session = None, user_id: int = None) -> dict:
        """Mental health risk screening."""
        model = model_registry.get_model("mental_health", self.artifacts_dir)
        if model is None:
            return {"error": "Mental health model not loaded"}

        phq9_total = sum(features["phq9_scores"])
        gad7_total = sum(features["gad7_scores"])

        feature_vector = features["phq9_scores"] + features["gad7_scores"] + [
            features["age"], features["sleep_hours"], features["stress_level"],
            phq9_total, gad7_total
        ]
        X = np.array([feature_vector])

        try:
            prediction = int(model.predict(X)[0])
            probas = model.predict_proba(X)[0]
            confidence = float(probas[prediction])
        except Exception as e:
            logger.error(f"Mental health prediction error: {e}")
            prediction = int(model.predict(X)[0])
            confidence = 0.0

        risk_map = {0: "Low Risk", 1: "Moderate Risk", 2: "High Risk"}
        label = risk_map.get(prediction, "Unknown")
        result = {
            "prediction": label,
            "confidence": round(confidence, 4),
            "top_k": [
                {"disease": risk_map.get(i, f"Class {i}"), "confidence": round(float(probas[i]), 4)}
                for i in range(len(probas))
            ],
            "model_name": "mental_health",
        }

        if db:
            report_id = self._save_history(
                db, "mental_health", features, label, confidence, result["top_k"], user_id=user_id
            )
            result["report_id"] = report_id

        return result

    def predict_severity(self, symptoms: list[str], db: Session = None, user_id: int = None) -> dict:
        """Symptom severity scoring."""
        model = model_registry.get_model("severity", self.artifacts_dir)
        if model is None:
            return {"error": "Severity model not loaded"}

        meta = model_registry.get_metadata("severity", self.artifacts_dir)
        feature_names = meta.get("feature_list", [])

        # Apply synonym resolution for severity scoring too
        feature_vector = np.zeros(len(feature_names))
        for symptom in symptoms:
            symptom_clean = symptom.strip().lower().replace(" ", "_")
            mapped = SYMPTOM_SYNONYM_MAP.get(symptom_clean, symptom_clean)
            if mapped in feature_names:
                idx = feature_names.index(mapped)
                feature_vector[idx] = 1
            elif symptom_clean in feature_names:
                idx = feature_names.index(symptom_clean)
                feature_vector[idx] = 1

        X = feature_vector.reshape(1, -1)

        try:
            score = float(model.predict(X)[0])
            score = max(0.0, min(10.0, score))
        except Exception as e:
            logger.error(f"Severity prediction error: {e}")
            score = 5.0

        if score <= 3:
            urgency = "Low"
        elif score <= 6:
            urgency = "Moderate"
        elif score <= 8:
            urgency = "High"
        else:
            urgency = "Emergency"

        result = {
            "severity_score": round(score, 2),
            "urgency_level": urgency,
        }

        if db:
            self._save_history(
                db, "severity", {"symptoms": symptoms},
                urgency, score / 10.0, severity_score=score, user_id=user_id
            )

        return result

    def predict_pneumonia(self, image_bytes: bytes, filename: str, db: Session = None, user_id: int = None) -> dict:
        """Pneumonia detection from chest X-ray image."""
        model = model_registry.get_model("pneumonia", self.artifacts_dir)
        if model is None:
            return {"error": "Pneumonia model not loaded"}

        import cv2
        img_array = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"error": "Invalid image"}

        try:
            is_keras = hasattr(model, 'layers')  # TensorFlow Keras model
            if is_keras:
                img = cv2.resize(img, (150, 150))
                img = img.astype("float32") / 255.0
                img = img.reshape(1, 150, 150, 1)
                pred = model.predict(img, verbose=0)[0][0]
                confidence = float(pred) if pred > 0.5 else float(1 - pred)
                label = "Pneumonia Detected" if pred > 0.5 else "Normal"
            else:
                # Fallback sklearn stub: resize to 16x16, flatten to 256 features
                img = cv2.resize(img, (16, 16))
                img = img.astype("float32") / 255.0
                X = img.flatten().reshape(1, -1)
                prediction = int(model.predict(X)[0])
                probas = model.predict_proba(X)[0]
                confidence = float(probas[prediction])
                label = "Pneumonia Detected" if prediction == 1 else "Normal"
                pred = float(probas[1])  # probability of pneumonia class
        except Exception as e:
            logger.error(f"Pneumonia prediction error: {e}")
            label = "Error"
            confidence = 0.0
            pred = 0.5

        result = {
            "prediction": label,
            "confidence": round(confidence, 4),
            "top_k": [
                {"disease": "Normal", "confidence": round(float(1 - pred), 4)},
                {"disease": "Pneumonia", "confidence": round(float(pred), 4)},
            ],
            "model_name": "pneumonia",
        }

        if db:
            report_id = self._save_history(
                db, "pneumonia", {}, label, confidence,
                result["top_k"], image_filename=filename, user_id=user_id
            )
            result["report_id"] = report_id

        return result

    def predict_skin(self, image_bytes: bytes, filename: str, db: Session = None, user_id: int = None) -> dict:
        """Skin disease classification from image."""
        model = model_registry.get_model("skin", self.artifacts_dir)
        if model is None:
            return {"error": "Skin disease model not loaded"}

        import cv2
        img_array = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            return {"error": "Invalid image"}

        class_indices = model_registry.get_class_indices("skin", self.artifacts_dir)
        idx_to_class = {v: k for k, v in class_indices.items()} if class_indices else {}

        try:
            is_keras = hasattr(model, 'layers')  # TensorFlow Keras model
            if is_keras:
                img = cv2.resize(img, (128, 128))
                img = img.astype("float32") / 255.0
                img = img.reshape(1, 128, 128, 3)
                preds = model.predict(img, verbose=0)[0]
            else:
                # Fallback sklearn stub: resize to 16x16, flatten to 768 features
                img = cv2.resize(img, (16, 16))
                img = img.astype("float32") / 255.0
                X = img.flatten().reshape(1, -1)
                preds = model.predict_proba(X)[0]

            top_indices = np.argsort(preds)[::-1][:3]
            top_k = []
            for i in top_indices:
                class_name = idx_to_class.get(i, f"Class_{i}")
                top_k.append({"disease": class_name, "confidence": round(float(preds[i]), 4)})
            prediction = top_k[0]["disease"]
            confidence = top_k[0]["confidence"]
        except Exception as e:
            logger.error(f"Skin prediction error: {e}")
            prediction = "Error"
            confidence = 0.0
            top_k = []

        result = {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "top_k": top_k,
            "model_name": "skin",
        }

        if db:
            report_id = self._save_history(
                db, "skin", {}, prediction, confidence,
                top_k, image_filename=filename, user_id=user_id
            )
            result["report_id"] = report_id

        return result


# Global service instance
prediction_service = PredictionService()
