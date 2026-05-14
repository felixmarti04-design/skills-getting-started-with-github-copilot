"""
Pytest configuration and fixtures for testing the Mergington High School API
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture to provide a TestClient for API testing"""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """Fixture to provide a fresh copy of activities data for each test"""
    from src.data import activities
    return copy.deepcopy(activities)
