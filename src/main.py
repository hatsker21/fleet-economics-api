from fastapi import FastAPI
from src.api import auth
from src.api import auth, vehicles
from src.api import auth, vehicles, trips

app = FastAPI(
    title="B2B Fleet Economics API",
    description="API для управління автопарком та розрахунку економіки.",
    version="1.0.0"
)

# Підключаємо роутер авторизації до головного додатку
app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(trips.router)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "Fleet Economics API is running"}