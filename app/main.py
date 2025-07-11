# sheets-service/app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import sheets
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    print("✅ Sheets Service: MongoDB conectado")
    yield
    await close_mongo_connection()
    print("❌ Sheets Service: MongoDB desconectado")

app = FastAPI(
    title="Sheets Service",
    description="API para CRUD de fichas de personagens",
    lifespan=lifespan
)

app.include_router(
    sheets.router,
    prefix="/api/sheets",
    tags=["Sheets"]
)

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "service": "sheets",
        "template_service_url": settings.TEMPLATES_SERVICE_URL
    }