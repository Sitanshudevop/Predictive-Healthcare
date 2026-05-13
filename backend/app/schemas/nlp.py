"""
Pydantic schemas for NLP endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field


class NLPExtractInput(BaseModel):
    text: str = Field(..., min_length=3, max_length=5000)


class ExtractedSymptom(BaseModel):
    symptom: str
    negated: bool = False
    duration: Optional[str] = None
    severity_hint: Optional[str] = None


class NLPExtractResponse(BaseModel):
    symptoms: list[ExtractedSymptom]
    raw_text: str
    disclaimer: str = (
        "⚠️ NLP extraction is approximate. Always verify extracted symptoms with the patient."
    )
