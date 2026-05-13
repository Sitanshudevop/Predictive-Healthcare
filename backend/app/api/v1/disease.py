"""
Disease KB API endpoints — list, get, search diseases.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.disease import Disease
from app.schemas.disease import DiseaseOut, DiseaseListOut

router = APIRouter(prefix="/disease", tags=["Disease KB"])


@router.get("", response_model=DiseaseListOut)
def list_diseases(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """List all diseases with pagination."""
    total = db.query(Disease).count()
    diseases = (
        db.query(Disease)
        .order_by(Disease.disease_name)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return DiseaseListOut(
        diseases=[DiseaseOut.model_validate(d) for d in diseases],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/search", response_model=DiseaseListOut)
def search_diseases(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
):
    """Search diseases by name or symptoms."""
    diseases = (
        db.query(Disease)
        .filter(Disease.disease_name.ilike(f"%{q}%"))
        .order_by(Disease.disease_name)
        .all()
    )
    return DiseaseListOut(
        diseases=[DiseaseOut.model_validate(d) for d in diseases],
        total=len(diseases),
        page=1,
        page_size=len(diseases),
    )


@router.get("/{disease_id}", response_model=DiseaseOut)
def get_disease(disease_id: str, db: Session = Depends(get_db)):
    """Get a single disease by slug or numeric ID."""
    if disease_id.isdigit():
        disease = db.query(Disease).filter(Disease.id == int(disease_id)).first()
    else:
        disease = db.query(Disease).filter(Disease.slug == disease_id).first()

    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return DiseaseOut.model_validate(disease)
