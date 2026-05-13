"""
Chatbot API endpoint (public, no auth).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chatbot import ChatMessage, ChatResponse, RecommendInput
from app.services.chatbot_service import chatbot_service
from app.services.recommendation_service import recommendation_service
from app.db.session import get_db

router = APIRouter(tags=["Chatbot & Recommendations"])


@router.post("/chatbot/message", response_model=ChatResponse)
def chatbot_message(
    payload: ChatMessage,
):
    """Send a message to the health assistant chatbot."""
    result = chatbot_service.process_message(payload.message, payload.session_id)
    return ChatResponse(
        reply=result["reply"],
        session_id=result["session_id"],
        suggestions=result["suggestions"],
    )


@router.post("/recommend")
def get_recommendation(
    payload: RecommendInput,
    db: Session = Depends(get_db),
):
    """Get health recommendations based on disease and severity."""
    rec = recommendation_service.get_recommendation(payload.disease_id, payload.severity_score, db)
    return rec
