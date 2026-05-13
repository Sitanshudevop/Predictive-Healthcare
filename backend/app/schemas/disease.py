"""
Pydantic schemas for Disease KB endpoints.
"""

from typing import Optional
from pydantic import BaseModel


class OTCMedication(BaseModel):
    category: str
    examples: list[str] = []
    disclaimer: str = "Consult a licensed physician before use."


class DiseaseOut(BaseModel):
    id: int
    slug: str
    disease_name: str
    icd10_code: Optional[str] = None
    description: str
    common_symptoms: list[str] = []
    rare_symptoms: list[str] = []
    causes: list[str] = []
    risk_factors: list[str] = []
    complications: list[str] = []
    prevention: list[str] = []
    home_remedies: list[str] = []
    otc_medications: list[dict] = []
    prescription_drug_categories: list[str] = []
    recommended_specialist: Optional[str] = None
    severity_level: str = "moderate"
    avg_recovery_time: Optional[str] = None
    when_to_see_doctor: Optional[str] = None
    red_flag_symptoms: list[str] = []

    model_config = {"from_attributes": True}


class DiseaseListOut(BaseModel):
    diseases: list[DiseaseOut]
    total: int
    page: int
    page_size: int
