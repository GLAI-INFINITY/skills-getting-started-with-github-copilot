from pathlib import Path
import json
import os

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DEFAULT_FILE = DATA_DIR / "activities.json"


def _file_path() -> Path:
    return Path(os.environ.get("ACTIVITIES_FILE", str(DEFAULT_FILE)))


def load_activities():
    path = _file_path()
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)

    # Fallback default activities
    activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": [
                "michael@mergington.edu",
                "daniel@mergington.edu",
            ],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        },
    }
    save_activities(activities)
    return activities


def save_activities(activities: dict):
    path = _file_path()
    with open(path, "w") as f:
        json.dump(activities, f, indent=2)
