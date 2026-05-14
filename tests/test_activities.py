"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern
"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all 9 activities"""
    # Arrange
    expected_activity_count = 9

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == expected_activity_count
    assert "Chess Club" in data


def test_get_activities_returns_correct_structure(client):
    """Test that each activity has the required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in data.items():
        assert set(activity_data.keys()) == required_fields


def test_get_activities_includes_current_participants(client):
    """Test that activities include current participants in the list"""
    # Arrange
    expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["Chess Club"]["participants"] == expected_chess_participants


def test_get_activities_returns_correct_chess_club_data(client):
    """Test that Chess Club data matches expected structure"""
    # Arrange
    expected_chess_data = {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    }

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["Chess Club"] == expected_chess_data
