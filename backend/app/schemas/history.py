"""
Pydantic schemas for history endpoints.
"""

from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel


class HistoryOut(BaseModel):
    id: int
    model_name: str
    prediction: str
    confidence: Optional[float] = None
    severity_score: Optional[float] = None
    created_at: datetime
    input_data: Optional[Any] = None
    top_k: Optional[list] = None
    recommendation: Optional[dict] = None

    model_config = {"from_attributes": True}


class HistoryListOut(BaseModel):
    history: list[HistoryOut]
    total: int
