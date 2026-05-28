import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture that provides a test client and resets activities between tests"""
    # Arrange: Save original activities state
    original_activities = {
        activity: {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": details["participants"].copy()
        }
        for activity, details in activities.items()
    }
    
    # Act: Yield test client for the test to use
    yield TestClient(app)
    
    # Assert: Restore original activities after test
    activities.clear()
    activities.update(original_activities)
