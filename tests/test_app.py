import json
import importlib
from fastapi.testclient import TestClient


def test_get_activities(tmp_path, monkeypatch):
    test_file = tmp_path / "activities.json"
    initial = {
        "Test Club": {
            "description": "desc",
            "schedule": "now",
            "max_participants": 5,
            "participants": []
        }
    }
    test_file.write_text(json.dumps(initial))
    monkeypatch.setenv("ACTIVITIES_FILE", str(test_file))

    import src.app as appmodule
    importlib.reload(appmodule)
    client = TestClient(appmodule.app)

    r = client.get("/activities")
    assert r.status_code == 200
    body = r.json()
    assert "Test Club" in body


def test_signup_and_unregister(tmp_path, monkeypatch):
    test_file = tmp_path / "activities.json"
    initial = {
        "Chess Club": {
            "description": "desc",
            "schedule": "now",
            "max_participants": 2,
            "participants": []
        }
    }
    test_file.write_text(json.dumps(initial))
    monkeypatch.setenv("ACTIVITIES_FILE", str(test_file))

    import src.app as appmodule
    importlib.reload(appmodule)
    client = TestClient(appmodule.app)

    # signup
    r = client.post("/activities/Chess%20Club/signup?email=test@x.com")
    assert r.status_code == 200

    activities = client.get("/activities").json()
    assert "test@x.com" in activities["Chess Club"]["participants"]

    # unregister
    r2 = client.delete("/activities/Chess%20Club/participants/test@x.com")
    assert r2.status_code == 200
    activities2 = client.get("/activities").json()
    assert "test@x.com" not in activities2["Chess Club"]["participants"]
