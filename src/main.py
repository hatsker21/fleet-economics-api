from fastapi import FastAPI

app = FastAPI(
    title="B2B Fleet Economics API",
    description="API для управління автопарком та розрахунку економіки.",
    version="1.0.0"
)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "Fleet Economics API is running"}