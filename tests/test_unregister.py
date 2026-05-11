from urllib.parse import quote

from src import app as app_module


def _signup_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/signup"


def test_unregister_removes_participant(client):
    activity_name = "Basketball Team"
    email = "james@mergington.edu"

    response = client.delete(_signup_path(activity_name), params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_404_for_missing_activity(client):
    response = client.delete(_signup_path("Imaginary Club"), params={"email": "test@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_non_participant(client):
    response = client.delete(
        _signup_path("Chess Club"),
        params={"email": "not.registered@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
