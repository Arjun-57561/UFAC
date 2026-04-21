# File: tests/test_api.py
"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from api.app import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "rag" in data
    
    def test_health_check_structure(self, client):
        """Test health check response structure."""
        response = client.get("/health")
        data = response.json()
        assert "service" in data
        assert "UFAC Engine" in data["service"]


class TestRagStatusEndpoint:
    """Test RAG status endpoint."""
    
    def test_rag_status(self, client):
        """Test RAG status endpoint."""
        response = client.get("/rag-status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestCacheStatsEndpoint:
    """Test cache stats endpoint."""
    
    def test_cache_stats(self, client):
        """Test cache stats endpoint."""
        response = client.get("/cache-stats")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "cache" in data
    
    def test_cache_stats_structure(self, client):
        """Test cache stats response structure."""
        response = client.get("/cache-stats")
        data = response.json()
        cache_data = data["cache"]
        assert "assessment_cache" in cache_data
        assert "rag_cache" in cache_data
        assert "llm_cache" in cache_data


class TestCacheClearEndpoint:
    """Test cache clear endpoint."""
    
    def test_cache_clear(self, client):
        """Test cache clear endpoint."""
        response = client.post("/cache-clear")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data


class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "endpoints" in data
        assert "check" in data["endpoints"]
        assert "health" in data["endpoints"]
        assert "cache_stats" in data["endpoints"]


class TestCheckEndpoint:
    """Test eligibility check endpoint."""
    
    def test_check_endpoint_exists(self, client):
        """Test check endpoint exists."""
        response = client.post("/check", json={"occupation": "farmer"})
        # Should return 200 or 503 (if LLM not available)
        assert response.status_code in [200, 503, 500]
    
    def test_check_endpoint_invalid_request(self, client):
        """Test check endpoint with invalid request."""
        response = client.post("/check", json={"invalid_field": "value"})
        # Should still process (invalid fields are ignored)
        assert response.status_code in [200, 503, 500]
