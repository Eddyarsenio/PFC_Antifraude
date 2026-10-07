import json
from pathlib import Path

import joblib


MODEL_PATH = Path("ml/models/random_forest_model.joblib")
METADATA_PATH = Path("ml/models/model_metadata.json")


def load_model_metadata() -> dict:
    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Metadata do modelo não encontrado: {METADATA_PATH}"
        )

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def load_fraud_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Modelo de Machine Learning não encontrado: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)

def classify_risk(risk_score: float) -> str:
    if risk_score < 0 or risk_score > 100:
        raise ValueError("O Risk Score deve estar entre 0 e 100.")

    if risk_score <= 30:
        return "LOW"

    if risk_score <= 70:
        return "MEDIUM"

    return "HIGH"

def calculate_rule_score(
    beneficiary_new: int,
    device_new: int,
    ip_anomaly: int,
    location_anomaly: int
) -> float:
    signals = [
        beneficiary_new,
        device_new,
        ip_anomaly,
        location_anomaly
    ]

    if any(signal not in (0, 1) for signal in signals):
        raise ValueError("Os sinais das regras devem ser 0 ou 1.")

    score = 0.0

    if beneficiary_new == 1:
        score += 20

    if device_new == 1:
        score += 20

    if ip_anomaly == 1:
        score += 30

    if location_anomaly == 1:
        score += 30

    return score