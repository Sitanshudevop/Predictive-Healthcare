"""
Recommendation service — hybrid KB lookup + severity gating.
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session
from app.models.disease import Disease

logger = logging.getLogger(__name__)

DIET_SUGGESTIONS = {
    "mild": [
        "Maintain a balanced diet with fruits, vegetables, and whole grains",
        "Stay hydrated with 8-10 glasses of water daily",
        "Include immune-boosting foods like citrus fruits and leafy greens",
    ],
    "moderate": [
        "Follow a nutrient-dense diet with lean proteins and complex carbs",
        "Reduce processed foods, sugar, and saturated fats",
        "Consider anti-inflammatory foods like turmeric, ginger, and fish oil",
        "Stay hydrated and limit caffeine and alcohol",
    ],
    "severe": [
        "Follow your doctor's prescribed dietary plan",
        "Focus on easily digestible, high-nutrition foods",
        "Ensure adequate caloric intake; consider meal replacement if appetite is low",
        "Avoid any known trigger foods",
        "Stay well-hydrated; consider oral rehydration salts if needed",
    ],
    "emergency": [
        "Follow hospital/medical team dietary instructions",
        "NPO (nothing by mouth) if directed before procedures",
        "Focus on recovery nutrition as advised by your medical team",
    ],
}

EXERCISE_SUGGESTIONS = {
    "mild": [
        "Continue regular moderate exercise (30 min/day, 5 days/week)",
        "Walking, yoga, and light stretching are beneficial",
        "Listen to your body and rest when needed",
    ],
    "moderate": [
        "Engage in light exercise like walking or gentle yoga",
        "Avoid strenuous activities until symptoms improve",
        "Deep breathing exercises can help with stress and recovery",
    ],
    "severe": [
        "Rest is priority; avoid strenuous activities",
        "Gentle range-of-motion exercises only if approved by doctor",
        "Gradual return to activity as symptoms improve",
    ],
    "emergency": [
        "Complete rest as directed by medical team",
        "Follow rehabilitation plan once medically cleared",
    ],
}


class RecommendationService:
    """Hybrid recommendation engine: ML prediction → KB lookup → severity gating."""

    def get_recommendation(
        self,
        disease_slug: str,
        severity_score: float,
        db: Session,
    ) -> dict:
        """
        Generate a recommendation based on disease KB and severity.

        Args:
            disease_slug: The disease identifier slug
            severity_score: 0-10 severity score
            db: Database session

        Returns:
            Recommendation dictionary
        """
        # Look up disease in KB
        disease = db.query(Disease).filter(Disease.slug == disease_slug).first()

        if disease is None:
            # Try partial match
            disease = db.query(Disease).filter(
                Disease.disease_name.ilike(f"%{disease_slug}%")
            ).first()

        if disease is None:
            return self._default_recommendation(severity_score)

        # Determine severity level from score
        if severity_score <= 3:
            severity_level = "mild"
        elif severity_score <= 6:
            severity_level = "moderate"
        elif severity_score <= 8:
            severity_level = "severe"
        else:
            severity_level = "emergency"

        return {
            "disease_name": disease.disease_name,
            "description": disease.description,
            "home_remedies": disease.home_remedies or [],
            "otc_medications": disease.otc_medications or [],
            "diet_suggestions": DIET_SUGGESTIONS.get(severity_level, DIET_SUGGESTIONS["moderate"]),
            "exercise_suggestions": EXERCISE_SUGGESTIONS.get(severity_level, EXERCISE_SUGGESTIONS["moderate"]),
            "recommended_specialist": disease.recommended_specialist,
            "urgency": severity_score,
            "when_to_see_doctor": disease.when_to_see_doctor,
            "red_flags": disease.red_flag_symptoms or [],
            "disclaimer": "Consult a licensed physician before use. This is not medical advice.",
        }

    def _default_recommendation(self, severity_score: float) -> dict:
        """Default recommendation when disease is not found in KB."""
        if severity_score <= 3:
            severity_level = "mild"
        elif severity_score <= 6:
            severity_level = "moderate"
        elif severity_score <= 8:
            severity_level = "severe"
        else:
            severity_level = "emergency"

        return {
            "disease_name": "Unknown",
            "description": "The predicted condition was not found in our knowledge base.",
            "home_remedies": ["Rest and stay hydrated", "Monitor symptoms"],
            "otc_medications": [],
            "diet_suggestions": DIET_SUGGESTIONS.get(severity_level, DIET_SUGGESTIONS["moderate"]),
            "exercise_suggestions": EXERCISE_SUGGESTIONS.get(severity_level, EXERCISE_SUGGESTIONS["moderate"]),
            "recommended_specialist": "General Physician",
            "urgency": severity_score,
            "when_to_see_doctor": "If symptoms persist for more than 3 days or worsen, consult a doctor.",
            "red_flags": ["Sudden worsening of symptoms", "High fever above 103°F", "Difficulty breathing"],
            "disclaimer": "Consult a licensed physician before use. This is not medical advice.",
        }


# Global service instance
recommendation_service = RecommendationService()
