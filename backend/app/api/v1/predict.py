"""
Prediction API endpoints — all ML prediction routes (public, no auth).
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import get_settings
from app.schemas.predict import (
    GeneralPredictionInput, DiabetesInput, HeartDiseaseInput,
    BreastCancerInput, LiverDiseaseInput, KidneyDiseaseInput,
    MentalHealthInput, SeverityInput,
    PredictionResponse, SeverityResponse,
)
from app.services.prediction_service import prediction_service
from app.services.recommendation_service import recommendation_service

settings = get_settings()
router = APIRouter(prefix="/predict", tags=["Predictions"])

DISCLAIMER = settings.MEDICAL_DISCLAIMER


def _build_response(result: dict, db: Session, severity_score: float = 5.0) -> PredictionResponse:
    """Build a standardized prediction response with recommendation."""
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=result["error"])

    # Try to get recommendation from KB
    prediction_slug = result["prediction"].lower().replace(" ", "-")
    rec = recommendation_service.get_recommendation(prediction_slug, severity_score, db)

    return PredictionResponse(
        prediction=result["prediction"],
        confidence=result.get("confidence", 0.0),
        top_k=result.get("top_k", []),
        severity_score=severity_score,
        recommendation=rec,
        disclaimer=DISCLAIMER,
        model_name=result.get("model_name", ""),
        report_id=result.get("report_id"),
    )


from app.core.deps import get_current_user
from app.models.user import User

@router.post("/general", response_model=PredictionResponse)
def predict_general(
    payload: GeneralPredictionInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict disease from a list of symptoms using the general VotingClassifier."""
    result = prediction_service.predict_general(payload.symptoms, db, user_id=current_user.id)
    return _build_response(result, db)


@router.post("/diabetes", response_model=PredictionResponse)
def predict_diabetes(
    payload: DiabetesInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict diabetes risk from clinical features."""
    features = payload.model_dump()
    result = prediction_service.predict_diabetes(features, db, user_id=current_user.id)
    return _build_response(result, db)


@router.post("/heart", response_model=PredictionResponse)
def predict_heart(
    payload: HeartDiseaseInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict heart disease from clinical features."""
    features = payload.model_dump()
    result = prediction_service.predict_heart(features, db, user_id=current_user.id)
    return _build_response(result, db)


@router.post("/breast_cancer", response_model=PredictionResponse)
def predict_breast_cancer(
    payload: BreastCancerInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict breast cancer from 30 Wisconsin features."""
    result = prediction_service.predict_breast_cancer(payload.features, db, user_id=current_user.id)
    return _build_response(result, db)


@router.post("/liver", response_model=PredictionResponse)
def predict_liver(
    payload: LiverDiseaseInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict liver disease from lab values."""
    features = payload.model_dump()
    result = prediction_service.predict_liver(features, db, user_id=current_user.id)
    return _build_response(result, db)


@router.post("/kidney", response_model=PredictionResponse)
def predict_kidney(
    payload: KidneyDiseaseInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Predict chronic kidney disease from clinical parameters."""
    features = payload.model_dump()
    result = prediction_service.predict_kidney(features, db, user_id=current_user.id)
    return _build_response(result, db)


@router.post("/mental_health", response_model=PredictionResponse)
def predict_mental_health(
    payload: MentalHealthInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Screen mental health risk using PHQ-9, GAD-7, and lifestyle factors."""
    features = payload.model_dump()
    result = prediction_service.predict_mental_health(features, db, user_id=current_user.id)
    return _build_response(result, db)


@router.post("/severity", response_model=SeverityResponse)
def predict_severity(
    payload: SeverityInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Score symptom severity on a 0-10 scale."""
    result = prediction_service.predict_severity(payload.symptoms, db, user_id=current_user.id)
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=result["error"])
    return SeverityResponse(
        severity_score=result["severity_score"],
        urgency_level=result["urgency_level"],
        disclaimer=DISCLAIMER,
    )


@router.post("/pneumonia", response_model=PredictionResponse)
async def predict_pneumonia(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Detect pneumonia from chest X-ray image upload (public, no auth)."""
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {settings.ALLOWED_IMAGE_TYPES}",
        )

    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE // (1024*1024)} MB",
        )

    result = prediction_service.predict_pneumonia(contents, file.filename, db, user_id=1)
    return _build_response(result, db)


@router.post("/skin", response_model=PredictionResponse)
async def predict_skin(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Classify skin disease from image upload (public, no auth)."""
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {settings.ALLOWED_IMAGE_TYPES}",
        )

    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE // (1024*1024)} MB",
        )

    result = prediction_service.predict_skin(contents, file.filename, db, user_id=1)
    return _build_response(result, db)

