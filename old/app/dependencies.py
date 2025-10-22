from typing import Optional
import httpx
from fastapi import HTTPException
from app.config import settings

async def get_template_from_service_by_name(template_system_name: str):
    async with httpx.AsyncClient() as client:
        try:
            # Chama o serviço de templates
            response = await client.get(
                f"{settings.TEMPLATES_SERVICE_URL}by-name/{template_system_name}"
            )
            if response.status_code == 404:
                raise HTTPException(400, detail="Template não existe")
            return response.json()
        except httpx.ConnectError:
            raise HTTPException(500, detail="Serviço de templates indisponível")
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Erro ao acessar o serviço de templates: {e.response.text}"
            )
        
async def get_template_from_service_by_id(template_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.TEMPLATES_SERVICE_URL}by-id/{template_id}"
            )
            if response.status_code == 404:
                raise HTTPException(400, detail="Template não existe")
            return response.json()
        except httpx.ConnectError:
            raise HTTPException(500, detail="Serviço de templates indisponível")
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Erro ao acessar o serviço de templates: {e.response.text}"
            )

async def fetch_template(template_id: Optional[str], system_name: Optional[str]):
    if template_id:
        return await get_template_from_service_by_id(template_id)
    elif system_name:
        return await get_template_from_service_by_name(system_name)
    raise HTTPException(400, "Nenhum identificador fornecido")