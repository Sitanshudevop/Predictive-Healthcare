"""Models package init — imports all models for Alembic discovery."""

from app.models.prediction import PredictionHistory
from app.models.disease import Disease
from app.models.user import User

__all__ = ["PredictionHistory", "Disease", "User"]
