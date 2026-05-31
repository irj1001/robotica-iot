import json
import os
from datetime import datetime

STATE_FILE = "state.json"
LOG_FILE = "logs.json"

# =========================
# STATE
# =========================
def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "project": None,
            "phase": 0,
            "history": [],
            "task_status": {}
        }

    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {
            "project": None,
            "phase": 0,
            "history": [],
            "task_status": {}
        }


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def add_log(event_type, message, state=None):
    logs = load_logs()

    logs.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": event_type,
        "message": message,
        "project": state.get("project") if state else None,
        "phase": state.get("phase") if state else None
    })

    save_logs(logs)


# =========================
# LOGS
# =========================
def load_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)