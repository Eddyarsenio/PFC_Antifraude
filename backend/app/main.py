from fastapi import FastAPI

app = FastAPI(
    title="Sistema Antifraude - PFC",
    description="API para prevenção e detecção de fraudes em serviços bancários digitais",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Sistema Antifraude API",
        "status": "online"
    }