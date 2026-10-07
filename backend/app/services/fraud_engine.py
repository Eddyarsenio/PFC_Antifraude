def classify_risk(risk_score: float) -> str:
    if risk_score < 0 or risk_score > 100:
        raise ValueError("O Risk Score deve estar entre 0 e 100.")

    if risk_score <= 30:
        return "LOW"

    if risk_score <= 70:
        return "MEDIUM"

    return "HIGH"