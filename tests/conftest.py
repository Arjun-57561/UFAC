# File: tests/conftest.py
"""Pytest configuration and fixtures."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from api.app import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def event_loop():
    """Event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_groq_response():
    """Mock Groq API response."""
    return {
        "facts": ["User is a farmer", "User owns 2 hectares"],
        "consensus": 0.8
    }


@pytest.fixture
def mock_user_data():
    """Mock user data for testing."""
    return {
        "occupation": "farmer",
        "land_ownership": "yes",
        "aadhaar_linked": True,
        "aadhaar_ekyc_done": True,
        "bank_account": True,
        "annual_income": 50000,
        "income_tax_payer": False,
        "govt_employee": False,
        "pension_above_10k": False,
        "practicing_professional": False,
        "constitutional_post_holder": False,
    }
