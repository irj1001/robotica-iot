import json
from storage import load_state, save_state, add_log
from ai import improve_phase


class RoboMentor:

    def __init__(self):
        self.state = load_state()
        self.roadmap = self.load_roadmap()

    # =========================
    # ROADMAP
    # =========================
    def load_roadmap(self):
        with open("roadmap.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def get_project(self):
        idx = self.state["project"]

        if idx is None:
            return None

        if idx < 0 or idx >= len(self.roadmap["projects"]):
            return None

        return self.roadmap["projects"][idx]

    def start_project(self, index=0):
        self.state["project"] = index
        self.state["phase"] = 0
        self.state["task_status"] = {}

        project = self.get_project()
        project_name = project["name"] if project else str(index)

        add_log("INFO", f"Proyecto iniciado: {project_name}", self.state)
        save_state(self.state)

    # =========================
    # PHASE
    # =========================
    def get_phase(self):
        project = self.get_project()

        if not project:
            return None

        idx = self.state["phase"]

        if idx < 0 or idx >= len(project["phases"]):
            return None

        return project["phases"][idx]

    def show_phase(self):
        phase = self.get_phase()

        if not phase:
            print("\n🎉 Proyecto completado")
            return

        phase_ai = improve_phase(self.state["project"], phase)

        print("\n====================")
        print(f"FASE {self.state['phase']}: {phase_ai['title']}")
        print("====================\n")

        for task in phase_ai["tasks"]:
            print(" -", task)

    # =========================
    # CHECKLIST
    # =========================
    def _task_key(self):
        return f"{self.state['project']}_{self.state['phase']}"

    def init_task_status(self, phase):
        key = self._task_key()

        if "task_status" not in self.state:
            self.state["task_status"] = {}

        if key not in self.state["task_status"]:
            self.state["task_status"][key] = [False] * len(phase["tasks"])
            save_state(self.state)

        return self.state["task_status"][key]

    def toggle_task(self, index):
        phase = self.get_phase()
        if not phase:
            return

        status = self.init_task_status(phase)

        if index < 0 or index >= len(status):
            return

        status[index] = not status[index]
        self.state["task_status"][self._task_key()] = status

        save_state(self.state)

        if all(status):
            self.confirm_phase(True)

    # =========================
    # TRANSICIÓN SEGURA
    # =========================
    def confirm_phase(self, ok=True):
        project = self.get_project()

        if not project:
            return

        project_name = project["name"]
        total_phases = len(project["phases"])

        if ok:
            self.state["phase"] += 1
            add_log("OK", "Fase completada", self.state)
        else:
            add_log("ERROR", "Fase fallida", self.state)

        # si termina proyecto → siguiente proyecto automático
        if self.state["phase"] >= total_phases:
            self.state["project"] += 1
            self.state["phase"] = 0
            self.state["task_status"] = {}

            add_log("INFO", f"Proyecto completado → siguiente proyecto ({project_name})", self.state)

        save_state(self.state)

    # =========================
    # UI DATA
    # =========================
    def get_ui_data(self):
        phase = self.get_phase()

        if not phase:
            return {
                "title": "Proyecto completado",
                "tasks": [],
                "project": self.state["project"],
                "phase": self.state["phase"],
                "task_status": []
            }

        status = self.init_task_status(phase)

        return {
            "title": phase["title"],
            "tasks": phase["tasks"],
            "hardware": phase.get("hardware", []),
            "resources": phase.get("resources", []),
            "project": self.state["project"],
            "phase": self.state["phase"],
            "task_status": status
        }

    # =========================
    # PROGRESS
    # =========================
    def get_progress(self):
        project = self.get_project()

        if not project:
            return 0, 0, 0

        total = len(project["phases"])
        current = self.state["phase"]

        percent = int((current / total) * 100) if total > 0 else 0

        return current, total, percent

    # =========================
    # RESET
    # =========================
    def reset_project(self):
        self.state["project"] = 0
        self.state["phase"] = 0
        self.state["task_status"] = {}
        save_state(self.state)

    def get_project_obj(self):
        return self.get_project()