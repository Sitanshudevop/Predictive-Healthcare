"""Tests for /api/health and /api/version endpoints."""


class TestHealthEndpoints:
    """Health check and version endpoints."""

    def test_health_check(self, client):
        """GET /api/health returns healthy status."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data

    def test_version_endpoint(self, client):
        """GET /api/version returns version info."""
        response = client.get("/api/version")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "name" in data
        assert data["version"] == "1.0.0"

    def test_nonexistent_route_returns_404_or_405(self, client):
        """Unknown routes should not return 200."""
        response = client.get("/api/nonexistent-route-xyz")
        assert response.status_code in (404, 405)
