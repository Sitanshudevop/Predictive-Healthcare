"""
Predictive Healthcare System — FastAPI Main Application

This is the main entry point for the backend API server.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.db.session import engine
from app.db.base import Base
from app.ml_loader import model_registry

# Import all models for table creation
from app.models import PredictionHistory, Disease

# Import routers
from app.api.v1.predict import router as predict_router
from app.api.v1.nlp import router as nlp_router
from app.api.v1.disease import router as disease_router
from app.api.v1.history import router as history_router
from app.api.v1.chatbot import router as chatbot_router

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    # Startup
    logger.info("Starting Predictive Healthcare System...")

    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")

    # Load ML model registry
    model_registry.load_registry(settings.MODEL_REGISTRY_PATH)
    logger.info(f"Model registry loaded: {model_registry.registered_models}")

    yield

    # Shutdown
    logger.info("Shutting down Predictive Healthcare System...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "An academic predictive healthcare system using ML models for disease prediction, "
        "symptom analysis, and health recommendations. "
        "⚠️ NOT a medical device. For educational purposes only."
    ),
    lifespan=lifespan,
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers under /api prefix
app.include_router(predict_router, prefix="/api")
app.include_router(nlp_router, prefix="/api")
app.include_router(disease_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(chatbot_router, prefix="/api")


# Health check endpoints
@app.get("/api/health", tags=["Health"])
def health_check():
    """Liveness probe."""
    return {"status": "healthy", "service": settings.APP_NAME}


@app.get("/api/version", tags=["Health"])
def version():
    """Application version."""
    return {
        "version": settings.APP_VERSION,
        "name": settings.APP_NAME,
        "models_loaded": model_registry.loaded_models,
        "models_registered": model_registry.registered_models,
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler to prevent stack trace leakage."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal error occurred. Please try again later.",
            "disclaimer": settings.MEDICAL_DISCLAIMER,
        },
    )

import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Serve Frontend SPA if built
dist_dir = os.environ.get("FRONTEND_DIST_DIR", "")
if dist_dir and os.path.isdir(dist_dir):
    # Mount the assets directory specifically
    assets_dir = os.path.join(dist_dir, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    # Catch-all route to serve index.html for React Router
    @app.api_route("/{path_name:path}", methods=["GET"])
    async def catch_all(path_name: str):
        file_path = os.path.join(dist_dir, path_name)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(dist_dir, "index.html"))
