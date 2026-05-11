def test_get_activities_returns_activity_payload(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()

    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert set(payload["Chess Club"].keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }


def test_get_activities_disables_caching(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
