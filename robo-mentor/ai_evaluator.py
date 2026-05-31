def evaluate_phase_completion(project_name, phase, user_report):
    """
    Evaluación híbrida (simulada + lista para LLM real)
    """

    report = user_report.lower()

    # heurística simple (luego esto lo sustituimos por LLM real)
    keywords_ok = [
        "funciona", "ok", "listo", "hecho", "correcto", "subido",
        "compila", "ejecuta", "mqtt", "docker", "esp32", "ros"
    ]

    score = sum(1 for k in keywords_ok if k in report)

    confidence = min(1.0, score / 5)

    if confidence >= 0.4:
        status = "PASS"
    else:
        status = "FAIL"

    feedback = []

    if status == "PASS":
        feedback = [
            "La evidencia indica progreso funcional",
            "Se detectan señales de ejecución correcta"
        ]
    else:
        feedback = [
            "No hay suficiente evidencia técnica clara",
            "Falta demostrar ejecución real (logs, pruebas, resultados)"
        ]

    next_actions = [
        "Revisar que el sistema realmente ejecuta",
        "Adjuntar logs o pruebas reales",
        "Probar paso mínimo funcional"
    ]

    return {
        "status": status,
        "confidence": round(confidence, 2),
        "feedback": feedback,
        "next_actions": next_actions
    }