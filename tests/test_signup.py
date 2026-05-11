from urllib.parse import quote

from src import app as app_module


def _signup_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/signup"


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(_signup_path(activity_name), params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_missing_activity(client):
    response = client.post(_signup_path("Imaginary Club"), params={"email": "test@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    response = client.post(
        _signup_path("Chess Club"),
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_400_when_activity_is_full(client):
    activity_name = "Debate Team"
    activity = app_module.activities[activity_name]

    # Fill the activity to capacity before attempting one more signup.
    remaining_slots = activity["max_participants"] - len(activity["participants"])
    for index in range(remaining_slots):
        activity["participants"].append(f"filled{index}@mergington.edu")

    response = client.post(
        _signup_path(activity_name),
        params={"email": "overflow@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
