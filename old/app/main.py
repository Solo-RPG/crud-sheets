# sheets-service/app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import sheets
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

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

# Configuração CORS
origins = [
    "http://localhost:3000",
    # Você pode adicionar outros domínios aqui, se precisar
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite o frontend localhost:3000
    allow_credentials=True,
    allow_methods=["*"],    # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],    # Permite todos os headers
)
