from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

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


@app.get("/")
def root():
    return {
        "message": "Sistema Antifraude API",
        "status": "online"
    }

@app.post("/transactions")
def create_transaction(transaction: TransactionRequest):
    transaction_time = datetime.now()

    return {
        "message": "Transacção recebida com sucesso",
        "transaction": transaction,
        "timestamp": transaction_time
    }
