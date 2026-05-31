import streamlit as st
from agent import RoboMentor
from storage import save_state
import json

st.set_page_config(page_title="RoboMentor Pro", layout="wide")

agent = RoboMentor()

st.title("🤖 RoboMentor Pro Dashboard")

# =========================
# INIT PROJECT
# =========================
if agent.state["project"] is None or agent.state["project"] < 0:

    st.subheader("📦 Selección de proyecto")

    project = st.selectbox(
        "Elige un proyecto",
        list(range(len(agent.roadmap["projects"]))),
        format_func=lambda i: agent.roadmap["projects"][i]["name"]
    )

    if st.button("🚀 Iniciar proyecto"):
        agent.start_project(project)
        st.rerun()

# =========================
# MAIN
# =========================
else:

    data = agent.get_ui_data()
    project_obj = agent.get_project_obj()

    col1, col2 = st.columns([2, 1])

    # =========================
    # IZQUIERDA
    # =========================
    with col1:

        current, total, percent = agent.get_progress()

        project_name = project_obj["name"] if project_obj else "N/A"

        st.subheader(f"📦 Proyecto: {project_name}")
        st.write(f"🔢 Fase: {current} / {total}")
        st.write(f"📊 Progreso: {percent}%")

        progress_value = min(percent / 100, 1.0)
        st.progress(progress_value)

        st.markdown(f"## 🧭 {data['title']}")
        st.markdown("### 🛠 Tareas")

        for i, task in enumerate(data["tasks"]):

            status = False
            if i < len(data.get("task_status", [])):
                status = data["task_status"][i]

            c1, c2 = st.columns([6, 1])

            with c1:
                if status:
                    st.success(f"✔ {task}")
                else:
                    st.write(f"⬜ {task}")

            with c2:
                if st.button("✓", key=f"task_{i}"):
                    agent.toggle_task(i)
                    st.rerun()

        # HARDWARE
        if data.get("hardware"):
            st.markdown("### 🔧 Hardware")
            for h in data["hardware"]:
                st.write("•", h)

        # RECURSOS
        if data.get("resources"):
            st.markdown("### 📚 Recursos")
            for r in data["resources"]:
                st.write("•", r)

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("✔ HECHO (fase)"):
                agent.confirm_phase(True)
                st.rerun()

        with c2:
            if st.button("❌ ERROR"):
                agent.confirm_phase(False)
                st.rerun()

    # =========================
    # DERECHA
    # =========================
    with col2:

        st.subheader("📊 Estado")

        st.metric("Proyecto", agent.state["project"])
        st.metric("Fase", agent.state["phase"])

        st.markdown("---")

        if st.button("🔄 Reset"):
            agent.reset_project()
            st.rerun()

        st.markdown("---")

        st.subheader("🧾 Logs")

        def load_logs():
            try:
                with open("logs.json", "r") as f:
                    return json.load(f)
            except:
                return []

        logs = load_logs()[-8:]

        for log in reversed(logs):
            if log["type"] == "OK":
                st.success(f"{log['time']} - {log['message']}")
            elif log["type"] == "ERROR":
                st.error(f"{log['time']} - {log['message']}")
            else:
                st.info(f"{log['time']} - {log['message']}")

        st.markdown("---")

        st.subheader("🧠 IA Assistant")

        if st.button("Generar prompt"):
            prompt = f"""
Proyecto: {project_name}
Fase: {data['title']}
Tareas: {data['tasks']}

Dame:
- pasos exactos
- código si aplica
- errores comunes
- verificación
"""
            st.code(prompt)

        st.markdown("---")

        st.subheader("🗺 Roadmap")

        if project_obj:
            phases = project_obj["phases"]

            for i, p in enumerate(phases):
                if i == agent.state["phase"]:
                    st.markdown(f"👉 **Fase {i}: {p['title']}**")
                else:
                    st.markdown(f"Fase {i}: {p['title']}")

            st.markdown("---")

            selected = st.selectbox(
                "Ir a fase",
                list(range(len(phases))),
                format_func=lambda i: phases[i]["title"]
            )

            if st.button("📍 Saltar fase"):
                # FIX IMPORTANTE: no romper estado
                agent.state["phase"] = selected
                save_state(agent.state)
                st.rerun()