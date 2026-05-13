"""
Pydantic schemas for chatbot and recommendation endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    suggestions: list[str] = []
    disclaimer: str = (
        "⚠️ This chatbot is for informational purposes only. Not medical advice."
    )


class RecommendInput(BaseModel):
    disease_id: str
    severity_score: float = Field(..., ge=0, le=10)
