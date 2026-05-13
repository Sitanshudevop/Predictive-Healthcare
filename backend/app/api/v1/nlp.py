"""
NLP API endpoints — symptom extraction from free text (public, no auth).
"""

from fastapi import APIRouter

from app.schemas.nlp import NLPExtractInput, NLPExtractResponse, ExtractedSymptom
from app.services.nlp_service import nlp_service

router = APIRouter(prefix="/nlp", tags=["NLP"])


@router.post("/extract-symptoms", response_model=NLPExtractResponse)
def extract_symptoms(
    payload: NLPExtractInput,
):
    """Extract symptoms from free-text description using spaCy NLP."""
    results = nlp_service.extract_symptoms(payload.text)
    symptoms = [
        ExtractedSymptom(
            symptom=r["symptom"],
            negated=r.get("negated", False),
            duration=r.get("duration"),
            severity_hint=r.get("severity_hint"),
        )
        for r in results
    ]
    return NLPExtractResponse(
        symptoms=symptoms,
        raw_text=payload.text,
    )
