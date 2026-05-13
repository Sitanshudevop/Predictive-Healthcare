"""Tests for /api/disease/* — disease KB list, search, and detail."""

import pytest
from app.models.disease import Disease


@pytest.fixture()
def seed_diseases(db_session):
    """Seed a few test diseases into the DB."""
    diseases = [
        Disease(slug="common-cold", disease_name="Common Cold", icd10_code="J00",
                description="A viral infection of the upper respiratory tract.",
                severity_level="mild", recommended_specialist="General Physician",
                avg_recovery_time="7-10 days"),
        Disease(slug="diabetes", disease_name="Diabetes Mellitus", icd10_code="E11",
                description="A metabolic disorder characterized by high blood sugar.",
                severity_level="severe", recommended_specialist="Endocrinologist",
                avg_recovery_time="Chronic — lifelong management"),
        Disease(slug="asthma", disease_name="Asthma", icd10_code="J45",
                description="A chronic condition causing narrowing of airways.",
                severity_level="moderate", recommended_specialist="Pulmonologist",
                avg_recovery_time="Chronic — managed with medication"),
    ]
    for d in diseases:
        db_session.add(d)
    db_session.commit()
    yield diseases
    # Cleanup
    for d in diseases:
        existing = db_session.query(Disease).filter(Disease.slug == d.slug).first()
        if existing:
            db_session.delete(existing)
    db_session.commit()


class TestDiseaseList:
    """Disease listing and pagination."""

    def test_list_diseases(self, client, seed_diseases):
        """GET /api/disease returns paginated list."""
        response = client.get("/api/disease")
        assert response.status_code == 200
        data = response.json()
        assert "diseases" in data
        assert "total" in data
        assert data["total"] >= 3

    def test_list_diseases_pagination(self, client, seed_diseases):
        """Pagination parameters work correctly."""
        response = client.get("/api/disease?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["diseases"]) <= 2
        assert data["page"] == 1
        assert data["page_size"] == 2


class TestDiseaseSearch:
    """Disease search endpoint."""

    def test_search_by_name(self, client, seed_diseases):
        """GET /api/disease/search?q=cold finds Common Cold."""
        response = client.get("/api/disease/search?q=cold")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        names = [d["disease_name"] for d in data["diseases"]]
        assert "Common Cold" in names

    def test_search_no_results(self, client, seed_diseases):
        """GET /api/disease/search?q=xyznonexistent returns empty."""
        response = client.get("/api/disease/search?q=xyznonexistent")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0

    def test_search_short_query_fails(self, client):
        """Query shorter than 2 chars should fail validation."""
        response = client.get("/api/disease/search?q=a")
        assert response.status_code == 422


class TestDiseaseDetail:
    """Single disease detail endpoint."""

    def test_get_by_slug(self, client, seed_diseases):
        """GET /api/disease/common-cold returns the disease."""
        response = client.get("/api/disease/common-cold")
        assert response.status_code == 200
        data = response.json()
        assert data["disease_name"] == "Common Cold"
        assert data["icd10_code"] == "J00"

    def test_get_nonexistent(self, client):
        """GET /api/disease/nonexistent returns 404."""
        response = client.get("/api/disease/does-not-exist-at-all")
        assert response.status_code == 404
