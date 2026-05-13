"""
PredictionHistory SQLAlchemy model — stores all prediction results.
Predictions are stored as standalone entries linked by optional session_id.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey

from app.db.base import Base


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    model_name = Column(String(100), nullable=False, index=True)
    input_data = Column(JSON, nullable=True)
    prediction = Column(String(500), nullable=False)
    confidence = Column(Float, nullable=True)
    top_k = Column(JSON, nullable=True)
    severity_score = Column(Float, nullable=True)
    recommendation = Column(JSON, nullable=True)
    image_filename = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
