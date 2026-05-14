"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA (Arrange-Act-Assert) pattern
"""


def test_signup_successfully_registers_new_participant(client):
    """Test that a new participant can successfully sign up for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_adds_participant_to_activity_list(client):
    """Test that signup adds the participant to the activity's participant list"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert email in data[activity_name]["participants"]


def test_signup_prevents_duplicate_registration(client):
    """Test that a participant cannot sign up twice for the same activity"""
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


def test_signup_returns_404_for_nonexistent_activity(client):
    """Test that signup returns 404 when the activity doesn't exist"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_response_format(client):
    """Test that signup response has correct format with message field"""
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    data = response.json()

    # Assert
    assert "message" in data
    assert "Signed up" in data["message"]
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_with_multiple_different_students(client):
    """Test that multiple different students can sign up for the same activity"""
    # Arrange
    activity_name = "Art Club"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"

    # Act
    client.post(f"/activities/{activity_name}/signup?email={email1}")
    client.post(f"/activities/{activity_name}/signup?email={email2}")
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert email1 in data[activity_name]["participants"]
    assert email2 in data[activity_name]["participants"]
