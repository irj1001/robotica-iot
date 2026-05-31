def improve_phase(project_name, phase):
    """
    IA simulada que optimiza una fase de robótica.
    Preparada para ser sustituida por LLM real en el futuro.
    """

    base_tasks = phase.get("tasks", [])

    improved_tasks = base_tasks + [
        "✔ Validar conexiones antes de encender",
        "✔ Comprobar alimentación eléctrica (5V / 3.3V)",
        "✔ Ejecutar test mínimo del sistema",
    ]

    return {
        "title": f"{phase['title']} (IA optimized)",
        "tasks": improved_tasks,
        "tips": [
            "Divide el sistema en partes pequeñas antes de probar",
            "No conectes todo al mismo tiempo",
            "Si falla, vuelve al último punto funcional",
            "Usa multímetro antes de asumir errores de software"
        ],
        "risks": [
            "Conexiones invertidas",
            "Falta de alimentación estable",
            "Drivers incorrectos",
            "Firmware mal cargado"
        ],
        "debug_steps": [
            "Revisar alimentación",
            "Verificar conexiones físicas",
            "Comprobar puerto serie",
            "Ejecutar ejemplo mínimo"
        ]
    }


def debug_help(error_text):
    """
    IA básica de debugging.
    En el futuro esto será un LLM real.
    """

    base = [
        "Revisa conexiones físicas",
        "Comprueba alimentación USB",
        "Verifica puerto COM / dispositivo",
        "Prueba ejemplo mínimo primero"
    ]

    # heurística simple (mejora importante)
    error_text = error_text.lower()

    if "port" in error_text or "com" in error_text:
        base.insert(0, "⚠️ Problema de puerto serie detectado")

    if "power" in error_text or "voltage" in error_text:
        base.insert(0, "⚠️ Posible problema de alimentación")

    if "timeout" in error_text:
        base.insert(0, "⚠️ Timeout: conexión o firmware inestable")

    return base