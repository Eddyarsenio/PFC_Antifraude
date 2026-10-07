from datetime import datetime


def extract_transaction_hour(transaction_time: datetime) -> int:
    return transaction_time.hour