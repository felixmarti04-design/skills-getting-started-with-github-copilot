"""
Tests for POST /activities/{activity_name}/unregister endpoint using AAA (Arrange-Act-Assert) pattern
"""


def test_unregister_successfully_removes_participant(client):
    """Test that a participant can successfully unregister from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_removes_participant_from_list(client):
    """Test that unregister removes the participant from the activity's participant list"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    client.post(f"/activities/{activity_name}/unregister?email={email}")
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert email not in data[activity_name]["participants"]


def test_unregister_returns_404_for_nonexistent_activity(client):
    """Test that unregister returns 404 when the activity doesn't exist"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_400_for_participant_not_signed_up(client):
    """Test that unregister returns 400 when participant is not signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "notsignedupstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_response_format(client):
    """Test that unregister response has correct format with message field"""
    # Arrange
    activity_name = "Soccer Team"
    email = "noah@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    data = response.json()

    # Assert
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_prevents_duplicate_unregistration(client):
    """Test that a participant cannot unregister twice"""
    # Arrange
    activity_name = "Drama Club"
    email = "elijah@mergington.edu"

    # Act - First unregister (should succeed)
    response1 = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    # Second unregister (should fail)
    response2 = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Student not signed up for this activity"
