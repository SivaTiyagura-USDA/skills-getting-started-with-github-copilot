from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_student_cannot_sign_up_for_activity_twice():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    participants = activities[activity_name]["participants"]
    participants_before = participants.copy()

    try:
        first_response = client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )
        duplicate_response = client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )

        assert first_response.status_code == 200
        assert duplicate_response.status_code == 400
        assert duplicate_response.json()["detail"] == "Student is already signed up"
        assert participants.count(email) == 1
    finally:
        participants[:] = participants_before


def test_sign_up_for_unknown_activity_returns_not_found():
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
