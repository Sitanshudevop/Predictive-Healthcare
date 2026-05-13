"""Tests for /api/predict/* — all prediction endpoints are now publicly accessible (no auth required)."""

import pytest


class TestPredictEndpoints:
    """Prediction endpoints are public — no auth required."""

    def test_predict_general_is_public(self, client):
        """POST /api/predict/general is accessible without auth (200 or 503 if model missing)."""
        response = client.post("/api/predict/general", json={
            "symptoms": ["headache", "fever"]
        })
        assert response.status_code in (200, 503)

    def test_predict_diabetes_is_public(self, client):
        """POST /api/predict/diabetes is accessible without auth."""
        response = client.post("/api/predict/diabetes", json={
            "pregnancies": 1, "glucose": 120, "blood_pressure": 70,
            "skin_thickness": 20, "insulin": 80, "bmi": 25.0,
            "diabetes_pedigree_function": 0.5, "age": 30
        })
        assert response.status_code in (200, 503)

    def test_predict_heart_is_public(self, client):
        """POST /api/predict/heart is accessible without auth."""
        response = client.post("/api/predict/heart", json={
            "age": 55, "sex": 1, "cp": 2, "trestbps": 130,
            "chol": 250, "fbs": 0, "restecg": 0, "thalach": 150,
            "exang": 0, "oldpeak": 1.5, "slope": 1, "ca": 0, "thal": 2
        })
        assert response.status_code in (200, 503)

    def test_predict_severity_is_public(self, client):
        """POST /api/predict/severity is accessible without auth."""
        response = client.post("/api/predict/severity", json={
            "symptoms": ["chest pain", "shortness of breath", "dizziness"]
        })
        assert response.status_code in (200, 503)

    def test_predict_mental_health_is_public(self, client):
        """POST /api/predict/mental-health is accessible without auth."""
        response = client.post("/api/predict/mental-health", json={
            "phq9_scores": [1, 1, 1, 1, 1, 1, 1, 1, 1],
            "gad7_scores": [1, 1, 1, 1, 1, 1, 1],
            "age": 28, "sleep_hours": 5.5, "stress_level": 6
        })
        assert response.status_code in (200, 503)

    def test_predict_pneumonia_invalid_file_type(self, client):
        """POST /api/predict/pneumonia with non-image returns 400."""
        response = client.post(
            "/api/predict/pneumonia",
            files={"file": ("test.txt", b"not an image", "text/plain")},
        )
        assert response.status_code == 400

    def test_predict_skin_invalid_file_type(self, client):
        """POST /api/predict/skin with non-image returns 400."""
        response = client.post(
            "/api/predict/skin",
            files={"file": ("test.pdf", b"not an image", "application/pdf")},
        )
        assert response.status_code == 400

    def test_predict_diabetes_validation_error(self, client):
        """Missing required fields returns 422."""
        response = client.post("/api/predict/diabetes", json={
            "glucose": 120  # Missing all other required fields
        })
        assert response.status_code == 422

    def test_predict_general_empty_symptoms(self, client):
        """Empty symptoms list is a validation error (422) or success/unavailable (200/503)."""
        response = client.post("/api/predict/general", json={"symptoms": []})
        assert response.status_code in (200, 422, 503)


class TestHistoryEndpoints:
    """History endpoints — public, no auth required."""

    def test_list_history_is_public(self, client):
        """GET /api/history is accessible without auth."""
        response = client.get("/api/history")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert "total" in data

    def test_list_history_with_session_id(self, client):
        """GET /api/history?session_id=... filters by session."""
        response = client.get("/api/history?session_id=test-session-123")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["history"], list)

    def test_get_nonexistent_history_item(self, client):
        """GET /api/history/99999 returns 404 for non-existent report."""
        response = client.get("/api/history/99999")
        assert response.status_code == 404
