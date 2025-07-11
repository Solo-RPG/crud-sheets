from typing import Any, Dict
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import SheetForm, SheetCreateRequest
from app.sheets_rules import create_sheet_from_template
from app.dependencies import fetch_template, get_template_from_service_by_name, get_template_from_service_by_id
from app.config import settings
from app.database import get_database
import httpx

router = APIRouter(prefix="/sheets", tags=["Sheets"])

@router.post("/", response_model=SheetForm)
async def create_sheet(
    request: Dict[str, Any],  # Recebe o JSON bruto
    db=Depends(get_database)
):
    try:
        # 1. Normalização dos dados
        clean_data = {
            "template_id": request.get("template_id"),
            "system_name": request.get("system_name"),
            "owner_id": request["owner_id"],
            "fields": request.get("fields") or request.get("user_data") or {}
        }

        print(f"Dados normalizados: {clean_data}")

        # 2. Validação mínima
        if not clean_data["template_id"] and not clean_data["system_name"]:
            raise HTTPException(400, detail="Pelo menos um identificador deve ser fornecido (template_id ou system_name)")

        if not clean_data["owner_id"]:
            raise HTTPException(400, detail="owner_id é obrigatório")
        if not isinstance(clean_data["fields"], dict):
            raise HTTPException(400, detail="fields deve ser um dicionário")
        if not clean_data["fields"]:
            raise HTTPException(400, detail="fields não pode ser vazio")
        
        # 3. Validação de owner_id

        # 4. Busca do template
        template = await fetch_template(
            template_id=clean_data["template_id"],
            system_name=clean_data["system_name"]
        )

        # 5. Criação da ficha
        sheet = create_sheet_from_template(
            template=template,
            user_data=clean_data["fields"],
            owner_id=clean_data["owner_id"]
        )
        
        # 6. Persistência
        inserted = await db.sheets.insert_one(sheet.model_dump(by_alias=True))
        
        data = sheet.model_dump(exclude={"id"})
        return SheetForm(
            **data,
            id=str(inserted.inserted_id)
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback.print_exc()  # Log detalhado para debug
        raise HTTPException(500, detail=f"Erro ao criar ficha: {str(e)}")

@router.get("/template/")
async def get_templates():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.TEMPLATES_SERVICE_URL}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        print(f"Erro HTTP: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(status_code=exc.response.status_code, detail="Erro ao buscar templates.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")

@router.get("/{sheet_id}")
async def get_sheet(sheet_id: str, db=Depends(get_database)):
    sheet = await get_template_from_service_by_id(sheet_id)
    if not sheet:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    return sheet

@router.get("/by-name/{system_name}")
async def get_sheet_by_name(system_name: str, db=Depends(get_database)):
    sheet = await get_template_from_service_by_name(system_name)
    if not sheet:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    return sheet
