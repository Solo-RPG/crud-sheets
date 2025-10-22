from motor.motor_asyncio import AsyncIOMotorClient
import certifi
from app.config import settings
from fastapi import HTTPException   

class MongoDB:
    client: AsyncIOMotorClient = None

db = MongoDB()

async def connect_to_mongo():
    try:
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            tls=True,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=False,
            serverSelectionTimeoutMS=5000
        )
        # Teste simplificado de conexão
        await db.client.server_info()
        print("✅ Conectado ao MongoDB Atlas com SSL!")
    except Exception as e:
        print(f"❌ Falha na conexão SSL: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erro ao conectar ao MongoDB Atlas. Verifique as configurações."
        )

def get_database():
    return db.client[settings.MONGODB_NAME]

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("❌ Desconectado do MongoDB Atlas")