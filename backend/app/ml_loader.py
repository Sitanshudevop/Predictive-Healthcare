"""
ML Model Loader — Singleton model registry for loading and caching ML artifacts.

Reads registry.json on startup and lazy-loads models on first prediction call.
"""

import json
import os
import logging
from pathlib import Path
from typing import Optional, Any

import joblib
import numpy as np

logger = logging.getLogger(__name__)


class ModelRegistry:
    """Singleton registry for all ML model artifacts."""

    _instance: Optional["ModelRegistry"] = None
    _models: dict[str, Any] = {}
    _metadata: dict[str, dict] = {}
    _registry: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._models = {}
            cls._instance._metadata = {}
            cls._instance._registry = {}
        return cls._instance

    def load_registry(self, registry_path: str) -> None:
        """Load the model registry JSON file."""
        registry_file = Path(registry_path)
        if registry_file.exists():
            with open(registry_file, "r") as f:
                self._registry = json.load(f)
            logger.info(f"Loaded model registry with {len(self._registry)} entries")
        else:
            logger.warning(f"Registry file not found at {registry_path}")
            self._registry = {}

    def get_model(self, model_name: str, artifacts_dir: str) -> Any:
        """Lazy-load and return a model by name."""
        if model_name in self._models:
            return self._models[model_name]

        if model_name not in self._registry:
            logger.warning(f"Model '{model_name}' not found in registry")
            return None

        entry = self._registry[model_name]
        artifact_path = Path(artifacts_dir) / entry["filename"]

        if not artifact_path.exists():
            logger.error(f"Artifact file not found: {artifact_path}")
            return None

        try:
            if str(artifact_path).endswith((".h5", ".keras")):
                # TensorFlow/Keras model
                import tensorflow as tf
                model = tf.keras.models.load_model(str(artifact_path))
            elif str(artifact_path).endswith(".pkl") or str(artifact_path).endswith(".joblib"):
                model = joblib.load(str(artifact_path))
            else:
                logger.error(f"Unknown artifact format: {artifact_path}")
                return None

            self._models[model_name] = model
            logger.info(f"Loaded model '{model_name}' from {artifact_path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model '{model_name}': {e}")
            return None

    def get_metadata(self, model_name: str, artifacts_dir: str) -> dict:
        """Load and return metrics metadata for a model."""
        if model_name in self._metadata:
            return self._metadata[model_name]

        metrics_path = Path(artifacts_dir) / f"{model_name}_metrics.json"
        if metrics_path.exists():
            with open(metrics_path, "r") as f:
                self._metadata[model_name] = json.load(f)
            return self._metadata[model_name]

        return {}

    def get_all_metrics(self, artifacts_dir: str) -> dict:
        """Return metrics for all registered models."""
        all_metrics = {}
        for model_name in self._registry:
            all_metrics[model_name] = self.get_metadata(model_name, artifacts_dir)
        return all_metrics

    def get_class_indices(self, model_name: str, artifacts_dir: str) -> dict:
        """Load class indices JSON for image classification models."""
        indices_path = Path(artifacts_dir) / f"{model_name}_class_indices.json"
        if indices_path.exists():
            with open(indices_path, "r") as f:
                return json.load(f)
        return {}

    def get_feature_names(self, model_name: str, artifacts_dir: str) -> list:
        """Get feature names from metrics metadata."""
        meta = self.get_metadata(model_name, artifacts_dir)
        return meta.get("feature_list", [])

    def reload_model(self, model_name: str, artifacts_dir: str) -> Any:
        """Force reload a model (after retrain)."""
        if model_name in self._models:
            del self._models[model_name]
        if model_name in self._metadata:
            del self._metadata[model_name]
        # Re-read registry
        registry_path = Path(artifacts_dir) / "registry.json"
        self.load_registry(str(registry_path))
        return self.get_model(model_name, artifacts_dir)

    @property
    def registered_models(self) -> list[str]:
        """List all registered model names."""
        return list(self._registry.keys())

    @property
    def loaded_models(self) -> list[str]:
        """List currently loaded model names."""
        return list(self._models.keys())


# Global singleton
model_registry = ModelRegistry()
