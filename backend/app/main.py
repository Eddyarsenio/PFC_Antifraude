from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4
from backend.app.database import get_db_connection
from backend.app.services.feature_engineering import extract_transaction_hour
from backend.app.services.fraud_engine import analyze_transaction

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

class FraudAnalysisRequest(BaseModel):
    amount: float = Field(gt=0)
    beneficiary_new: int = Field(ge=0, le=1)
    device_new: int = Field(ge=0, le=1)
    ip_anomaly: int = Field(ge=0, le=1)
    location_anomaly: int = Field(ge=0, le=1)
    transactions_last_10m: int = Field(ge=0)
    customer_avg_amount: float = Field(gt=0)
    amount_ratio: float = Field(ge=0)
    customer_tx_count_24h: int = Field(ge=0)
    beneficiary_tx_count: int = Field(ge=0)
    hour: int = Field(ge=0, le=23)

class FraudAnalysisResponse(BaseModel):
    ml_score: float
    rule_score: float
    risk_score: float
    risk_level: str

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
    "/fraud/analyze",
    response_model=FraudAnalysisResponse
)
def fraud_analysis(request: FraudAnalysisRequest):
    features = request.model_dump()

    result = analyze_transaction(features)

    return result

@app.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=201,
    responses={
        404: {"description": "Cliente ou beneficiário não encontrado"}
    }
)
def create_transaction(transaction: TransactionRequest):
    transaction_id = str(uuid4())
    transaction_time = datetime.now()
    transaction_hour = extract_transaction_hour(transaction_time)

    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM customers WHERE customer_id = %s",
                (transaction.customer_id,)
            )

            customer_exists = cursor.fetchone()

            if customer_exists is None:
                raise HTTPException(
                    status_code=404,
                    detail="Cliente não encontrado"
                )

                cursor.execute(
                """
                SELECT 1
                FROM beneficiaries
                WHERE beneficiary_id = %s
                  AND customer_id = %s
                """,
                (
                    transaction.beneficiary_id,
                    transaction.customer_id
                )
            )

            beneficiary_exists = cursor.fetchone()

            if beneficiary_exists is None:
                raise HTTPException(
                    status_code=404,
                    detail="Beneficiário não encontrado para este cliente"
                )
            cursor.execute(
                """
                INSERT INTO transactions (
                    transaction_id,
                    customer_id,
                    beneficiary_id,
                    amount,
                    device_id,
                    transaction_time
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    transaction_id,
                    transaction.customer_id,
                    transaction.beneficiary_id,
                    transaction.amount,
                    transaction.device_id,
                    transaction_time
                )
            )

    return {
        "message": "Transacção recebida com sucesso",
        "transaction_id": transaction_id,
        "transaction": transaction,
        "timestamp": transaction_time,
        "hour": transaction_hour
    }
