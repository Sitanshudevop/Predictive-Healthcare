"""Schemas package init."""

from app.schemas.predict import (
    GeneralPredictionInput, DiabetesInput, HeartDiseaseInput, BreastCancerInput,
    LiverDiseaseInput, KidneyDiseaseInput, MentalHealthInput, SeverityInput,
    PredictionResponse, SeverityResponse, RecommendationOut, PredictionTopK,
)
from app.schemas.nlp import NLPExtractInput, NLPExtractResponse, ExtractedSymptom
from app.schemas.disease import DiseaseOut, DiseaseListOut
from app.schemas.history import HistoryOut, HistoryListOut
from app.schemas.chatbot import ChatMessage, ChatResponse, RecommendInput
