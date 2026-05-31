from agent import RoboMentor


def main():
    agent = RoboMentor()

    print("\n🤖 ROBO-MENTOR PRO (CLI MODE)\n")

    # -------------------------
    # SELECCIÓN DE PROYECTO
    # -------------------------
    if agent.state["project"] is None:

        print("📦 Proyectos disponibles:\n")

        projects = agent.roadmap.get("projects", [])

        for p in projects:
            print(" -", p["name"])

        print()

        name = input("👉 Elige proyecto: ").strip()

        if not any(p["name"] == name for p in projects):
            print("\n❌ Proyecto no encontrado. Saliendo...")
            return

        agent.start_project(name)
        print(f"\n🚀 Proyecto iniciado: {name}\n")

    # -------------------------
    # LOOP PRINCIPAL
    # -------------------------
    while True:

        agent.show_phase()

        print("\n-----------------------------------")
        print("HECHO = fase correcta")
        print("ERROR = repetir fase")
        print("SALIR = cerrar programa")
        print("-----------------------------------")

        user = input("👉 Acción: ").strip().lower()

        if user == "hecho":
            agent.confirm_phase(True)

        elif user == "error":
            agent.confirm_phase(False)

        elif user == "salir":
            print("\n👋 Saliendo de RoboMentor...\n")
            break

        else:
            print("\n⚠️ Entrada inválida. Usa HECHO / ERROR / SALIR")


if __name__ == "__main__":
    main()