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
            "project": 0,
            "phase": 0,
            "history": [],
            "task_status": {},
            "progress": 0
        }

    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)

        # fallback de seguridad
        if "project" not in data:
            data["project"] = 0
        if "phase" not in data:
            data["phase"] = 0

        return data

    except json.JSONDecodeError:
        return {
            "project": 0,
            "phase": 0,
            "history": [],
            "task_status": {},
            "progress": 0
        }


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# =========================
# LOGS
# =========================
def load_logs():
    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


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
# SAFE STATE (FIX REAL)
# =========================
def safe_state(state, roadmap):
    total_projects = len(roadmap["projects"])

    # clamp project
    state["project"] = max(0, min(state["project"], total_projects - 1))

    current_project = roadmap["projects"][state["project"]]
    total_phases = len(current_project["phases"])

    # clamp phase
    state["phase"] = max(0, min(state["phase"], total_phases))

    # progreso global del proyecto actual
    if total_phases == 0:
        state["progress"] = 0
    else:
        state["progress"] = min(state["phase"] / total_phases, 1.0)

    return state