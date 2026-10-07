from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4
from backend.app.services.feature_engineering import extract_transaction_hour

app = FastAPI(
    title="Sistema Antifraude - PFC",
    description="API para prevenção e detecção de fraudes em serviços bancários digitais",
    version="1.0.0"
)

class TransactionRequest(BaseModel):
    customer_id: str
    beneficiary_id: str
    amount: float = Field(gt=0)
    device_id: str

class TransactionResponse(BaseModel):
    message: str
    transaction_id: str
    transaction: TransactionRequest
    timestamp: datetime
    hour: int


@app.get("/")
def root():
    return {
        "message": "Sistema Antifraude API",
        "status": "online"
    }

@app.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=201
)
def create_transaction(transaction: TransactionRequest):
    transaction_id = str(uuid4())
    transaction_time = datetime.now()
    transaction_hour = extract_transaction_hour(transaction_time)

    return {
        "message": "Transacção recebida com sucesso",
        "transaction_id": transaction_id,
        "transaction": transaction,
        "timestamp": transaction_time,
        "hour": transaction_hour
    }
