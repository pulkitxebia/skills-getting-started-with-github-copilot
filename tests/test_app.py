"""
Backend tests for the High School Activities API
Tests follow the AAA (Arrange-Act-Assert) pattern
"""

import pytest
from src.app import activities


# GET /activities tests
def test_get_activities(client):
    """Test GET /activities returns all activities"""
    # Arrange
    # (no setup needed - activities come from fixture)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_structure(client):
    """Test GET /activities returns proper activity structure"""
    # Arrange
    # (no setup needed)
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


# POST /signup tests
def test_signup_new_student(client):
    """Test signing up a new student for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 1
    assert "Signed up" in response.json()["message"]


def test_signup_duplicate_student(client):
    """Test that signing up the same student twice returns error"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_nonexistent_activity(client):
    """Test signup for non-existent activity returns 404"""
    # Arrange
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_multiple_students(client):
    """Test signing up multiple different students works correctly"""
    # Arrange
    activity_name = "Programming Class"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])
    
    # Act
    response1 = client.post(f"/activities/{activity_name}/signup?email={email1}")
    response2 = client.post(f"/activities/{activity_name}/signup?email={email2}")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email1 in activities[activity_name]["participants"]
    assert email2 in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 2


# POST /unregister tests
def test_unregister_existing_participant(client):
    """Test unregistering an existing participant"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count - 1
    assert "Unregistered" in response.json()["message"]


def test_unregister_nonexistent_participant(client):
    """Test unregistering a participant not in the activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Participant not found in activity"


def test_unregister_nonexistent_activity(client):
    """Test unregister from non-existent activity returns 404"""
    # Arrange
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_then_unregister(client):
    """Test signing up and then unregistering a student"""
    # Arrange
    activity_name = "Art Club"
    email = "teststudent@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])
    
    # Act: Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert: Signup successful
    assert signup_response.status_code == 200
    assert email in activities[activity_name]["participants"]
    
    # Act: Unregister
    unregister_response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert: Unregister successful, back to original count
    assert unregister_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count


# GET / test
def test_root_redirect(client):
    """Test that GET / redirects to /static/index.html"""
    # Arrange
    # (no setup needed)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
