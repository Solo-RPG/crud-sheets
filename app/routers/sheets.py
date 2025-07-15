from typing import Any, Dict, List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.models import SheetForm, SheetCreateRequest
from app.sheets_rules import create_sheet_from_template
from app.dependencies import fetch_template, get_template_from_service_by_name, get_template_from_service_by_id
from app.config import settings
from app.database import get_database
import httpx

router = APIRouter(tags=["Sheets"])

@router.post("/", response_model=SheetForm, summary="Cria uma nova ficha")
async def create_sheet(
    request: Dict[str, Any] = Body(
        ...,
        example={
            "template_id": "686d5b64330ef6a44fadc9e9",
            "owner_id": "1234567890abcdef",
            "fields": {
                "nome": "Tharion Martelo Flamejante",
                "classe": "guerreiro",
                "atributos": {
                    "força": {"valor": 18, "bônus": 4},
                    "destreza": {"valor": 10, "bônus": 0},
                    "carisma": {"valor": 8, "bônus": -1}
                }
            }
        }
    ),
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

@router.get("/template/", summary="Busca templates disponíveis")
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

@router.get("/{sheet_id}", response_model=SheetForm, summary="Busca uma ficha pelo ID")
async def get_sheet(sheet_id: str, db=Depends(get_database)):
    sheet = await db.sheets.find_one({"_id": ObjectId(sheet_id)})
    if not sheet:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    return sheet

@router.get("/", response_model=List[SheetForm], summary= "Lista todas as fichas") # Listar todas as fichas
async def get_sheets(db=Depends(get_database)):
    sheets = await db.sheets.find().to_list(100)
    return sheets

@router.get("/by-user_id/{user_id}", response_model=List[SheetForm], summary="Busca um template pelo ID do usuário")
async def get_sheet_by_user_id(user_id: str, db=Depends(get_database)):
    sheets = await db.sheets.find({"owner_id": user_id}).to_list(100)
    if not sheets:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    return sheets

@router.get("/by-name/{system_name}", response_model=SheetForm, summary="Busca um template pelo nome do sistema")
async def get_sheet_by_name(system_name: str, db=Depends(get_database)):
    sheet = await get_template_from_service_by_name(system_name)
    if not sheet:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    return sheet

@router.delete("/{sheet_id}", summary="Deleta uma ficha pelo ID")
async def delete_sheet(sheet_id: str, db=Depends(get_database)):
    result = await db.sheets.delete_one({"_id": ObjectId(sheet_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")
    return {"detail": "Ficha deletada com sucesso"}

@router.put("/{sheet_id}", response_model=SheetForm, summary="Atualiza uma ficha pelo ID")
async def update_sheet(
    sheet_id: str,
    request: Dict[str, Any] = Body(...),
    db=Depends(get_database)
):
    update_data = {k: v for k, v in request.items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar fornecido")

    result = await db.sheets.update_one({"_id": ObjectId(sheet_id)}, {"$set": update_data})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Ficha não encontrada ou nenhum dado foi alterado")
    
    updated_sheet = await db.sheets.find_one({"_id": ObjectId(sheet_id)})
    return updated_sheet