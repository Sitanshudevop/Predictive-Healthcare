"""
Pydantic schemas for prediction endpoints.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field


# ---------- Input Schemas ----------

class GeneralPredictionInput(BaseModel):
    symptoms: list[str] = Field(..., min_length=1, description="List of symptom names")


class DiabetesInput(BaseModel):
    pregnancies: int = Field(..., ge=0, le=20)
    glucose: float = Field(..., ge=0, le=300)
    blood_pressure: float = Field(..., ge=0, le=200)
    skin_thickness: float = Field(..., ge=0, le=100)
    insulin: float = Field(..., ge=0, le=900)
    bmi: float = Field(..., ge=0, le=70)
    diabetes_pedigree_function: float = Field(..., ge=0, le=3)
    age: int = Field(..., ge=1, le=120)


class HeartDiseaseInput(BaseModel):
    age: int = Field(..., ge=1, le=120)
    sex: int = Field(..., ge=0, le=1, description="0=Female, 1=Male")
    cp: int = Field(..., ge=0, le=3, description="Chest pain type (0-3)")
    trestbps: float = Field(..., ge=0, le=300, description="Resting blood pressure")
    chol: float = Field(..., ge=0, le=600, description="Serum cholesterol mg/dl")
    fbs: int = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl")
    restecg: int = Field(..., ge=0, le=2, description="Resting ECG results (0-2)")
    thalach: float = Field(..., ge=0, le=300, description="Max heart rate achieved")
    exang: int = Field(..., ge=0, le=1, description="Exercise induced angina")
    oldpeak: float = Field(..., ge=0, le=10, description="ST depression")
    slope: int = Field(..., ge=0, le=2, description="Slope of peak exercise ST segment")
    ca: int = Field(..., ge=0, le=4, description="Number of major vessels colored by fluoroscopy")
    thal: int = Field(..., ge=0, le=3, description="Thalassemia (0=normal, 1=fixed defect, 2=reversible defect, 3=unknown)")


class BreastCancerInput(BaseModel):
    features: list[float] = Field(..., min_length=30, max_length=30, description="30 numeric features from Wisconsin dataset")


class LiverDiseaseInput(BaseModel):
    age: int = Field(..., ge=1, le=120)
    gender: int = Field(..., ge=0, le=1, description="0=Female, 1=Male")
    total_bilirubin: float = Field(..., ge=0)
    direct_bilirubin: float = Field(..., ge=0)
    alkaline_phosphotase: float = Field(..., ge=0)
    alamine_aminotransferase: float = Field(..., ge=0)
    aspartate_aminotransferase: float = Field(..., ge=0)
    total_proteins: float = Field(..., ge=0)
    albumin: float = Field(..., ge=0)
    albumin_and_globulin_ratio: float = Field(..., ge=0)


class KidneyDiseaseInput(BaseModel):
    age: float = Field(..., ge=0, le=120)
    blood_pressure: float = Field(..., ge=0, le=200)
    specific_gravity: float = Field(..., ge=1.0, le=1.03)
    albumin: float = Field(..., ge=0, le=5)
    sugar: float = Field(..., ge=0, le=5)
    red_blood_cells: int = Field(..., ge=0, le=1, description="0=abnormal, 1=normal")
    pus_cell: int = Field(..., ge=0, le=1, description="0=abnormal, 1=normal")
    pus_cell_clumps: int = Field(..., ge=0, le=1, description="0=not present, 1=present")
    bacteria: int = Field(..., ge=0, le=1, description="0=not present, 1=present")
    blood_glucose_random: float = Field(..., ge=0)
    blood_urea: float = Field(..., ge=0)
    serum_creatinine: float = Field(..., ge=0)
    sodium: float = Field(..., ge=0)
    potassium: float = Field(..., ge=0)
    hemoglobin: float = Field(..., ge=0)
    packed_cell_volume: float = Field(..., ge=0)
    white_blood_cell_count: float = Field(..., ge=0)
    red_blood_cell_count: float = Field(..., ge=0)
    hypertension: int = Field(..., ge=0, le=1)
    diabetes_mellitus: int = Field(..., ge=0, le=1)
    coronary_artery_disease: int = Field(..., ge=0, le=1)
    appetite: int = Field(..., ge=0, le=1, description="0=poor, 1=good")
    pedal_edema: int = Field(..., ge=0, le=1)
    anemia: int = Field(..., ge=0, le=1)


class MentalHealthInput(BaseModel):
    phq9_scores: list[int] = Field(..., min_length=9, max_length=9, description="PHQ-9 scores (0-3 each)")
    gad7_scores: list[int] = Field(..., min_length=7, max_length=7, description="GAD-7 scores (0-3 each)")
    age: int = Field(..., ge=10, le=100)
    sleep_hours: float = Field(..., ge=0, le=24)
    stress_level: int = Field(..., ge=1, le=10)


class SeverityInput(BaseModel):
    symptoms: list[str] = Field(..., min_length=1)


# ---------- Output Schemas ----------

class PredictionTopK(BaseModel):
    disease: str
    confidence: float


class RecommendationOut(BaseModel):
    disease_name: Optional[str] = None
    description: Optional[str] = None
    home_remedies: list[str] = []
    otc_medications: list[dict] = []
    diet_suggestions: list[str] = []
    exercise_suggestions: list[str] = []
    recommended_specialist: Optional[str] = None
    urgency: float = 0.0
    when_to_see_doctor: Optional[str] = None
    red_flags: list[str] = []
    disclaimer: str = "Consult a licensed physician before use."


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    top_k: list[PredictionTopK] = []
    severity_score: float = Field(0.0, ge=0.0, le=10.0)
    recommendation: Optional[RecommendationOut] = None
    disclaimer: str = (
        "⚠️ This is an academic project. Not medical advice. Consult a licensed physician."
    )
    model_name: str = ""
    report_id: Optional[int] = None


class SeverityResponse(BaseModel):
    severity_score: float = Field(..., ge=0.0, le=10.0)
    urgency_level: str
    disclaimer: str = (
        "⚠️ This is an academic project. Not medical advice. Consult a licensed physician."
    )
