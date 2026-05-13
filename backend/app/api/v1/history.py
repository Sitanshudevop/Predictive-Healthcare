"""
History API endpoints — view, list, delete prediction history (public, no auth).
Predictions are linked by optional session_id instead of user accounts.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.prediction import PredictionHistory
from app.schemas.history import HistoryOut, HistoryListOut

router = APIRouter(prefix="/history", tags=["History"])


from app.core.deps import get_current_user
from app.models.user import User

@router.get("", response_model=HistoryListOut)
def list_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List prediction history for the current user."""
    records = db.query(PredictionHistory).filter(PredictionHistory.user_id == current_user.id).order_by(PredictionHistory.created_at.desc()).limit(100).all()
    return HistoryListOut(
        history=[HistoryOut.model_validate(r) for r in records],
        total=len(records),
    )


@router.get("/{report_id}", response_model=HistoryOut)
def get_history_item(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific prediction report for the current user."""
    record = db.query(PredictionHistory).filter(
        PredictionHistory.id == report_id,
        PredictionHistory.user_id == current_user.id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Report not found")
    return HistoryOut.model_validate(record)


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history_item(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific prediction report."""
    record = db.query(PredictionHistory).filter(
        PredictionHistory.id == report_id,
        PredictionHistory.user_id == current_user.id
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(record)
    db.commit()
    return None
