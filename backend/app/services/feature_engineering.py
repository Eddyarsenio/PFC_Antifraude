from datetime import datetime


def extract_transaction_hour(transaction_time: datetime) -> int:
    return transaction_time.hour

def calculate_amount_ratio(amount: float, customer_avg_amount: float) -> float:
    if customer_avg_amount <= 0:
        return 0.0

    return amount / customer_avg_amount

def is_new_beneficiary(
    beneficiary_id: str,
    known_beneficiaries: list[str]
) -> int:
    return 0 if beneficiary_id in known_beneficiaries else 1

def is_new_device(
    device_id: str,
    known_devices: list[str]
) -> int:
    return 0 if device_id in known_devices else 1