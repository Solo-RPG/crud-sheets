from httpx import AsyncClient
from fastapi import HTTPException
from app.config import settings
from app.models import SheetForm, SheetField, SheetFieldValue
import uuid
from typing import Dict, Any, List

def create_sheet_from_template(
    template: Dict[str, Any], 
    user_data: Dict[str, Any], 
    owner_id: str
) -> SheetForm:
    """
    Cria uma ficha a partir de um template e dados do usuário.
    
    :param template: Template do sistema (ex: D&D 5e).
    :param user_data: Dados enviados pelo frontend (estrutura aninhada).
    :param owner_id: ID do dono da ficha.
    :return: Objeto SheetForm pronto para ser salvo.
    """
    # 1. Gera ID único para a ficha
    sheet_id = str(uuid.uuid4())

    # 2. Converte os dados do usuário em SheetFields, validando contra o template
    sheet_data = _build_sheet_data(
        user_data=user_data,
        template_fields=template["fields"],
        parent_path=""
    )

    # 3. Retorna a ficha completa
    return SheetForm(
        id=sheet_id,
        template_id=template["id"],
        template_system_name=template["system_name"],
        template_system_version=template["version"],
        owner_id=owner_id,
        data=sheet_data
    )

def _build_sheet_data(
    user_data: Dict[str, Any],
    template_fields: List[Dict[str, Any]],
    parent_path: str
) -> Dict[str, SheetField]:
    """
    Método auxiliar recursivo para construir dados da ficha.
    
    :param user_data: Dados do frontend para o nível atual.
    :param template_fields: Campos do template para o nível atual.
    :param parent_path: Caminho pai (usado para mensagens de erro).
    :return: Dicionário de SheetFields.
    """
    sheet_data = {}

    for template_field in template_fields:
        field_name = template_field["name"]
        current_path = f"{parent_path}.{field_name}" if parent_path else field_name

        # Verifica se o campo está presente nos dados do usuário
        if field_name not in user_data:
            if template_field["required"]:
                raise ValueError(f"Campo obrigatório faltando: {current_path}")
            continue  # Ignora campos opcionais não enviados

        # Processa campos aninhados (objetos)
        if template_field.get("fields"):
            nested_user_data = user_data.get(field_name, {})
            nested_fields = _build_sheet_data(
                user_data=nested_user_data,
                template_fields=template_field["fields"],
                parent_path=current_path
            )
            sheet_data[field_name] = SheetField(
                value=nested_fields,
                required=template_field.get("required", True),
                options=template_field.get("options")
            )
        # Processa campos simples
        else:
            user_value = user_data[field_name]
            _validate_field(user_value, template_field, current_path)
            sheet_data[field_name] = SheetField(
                value=user_value,
                required=template_field.get("required", True),
                options=template_field.get("options")
            )
    return sheet_data

def _validate_field(value: Any, template_field: Dict[str, Any], field_path: str):
    """
    Valida um campo simples contra as regras do template.
    """
    # Valida tipo
    expected_type = template_field["type"]
    if expected_type == "number" and not isinstance(value, (int, float)):
        raise ValueError(f"Campo {field_path} deve ser um número")
    elif expected_type == "string" and not isinstance(value, str):
        raise ValueError(f"Campo {field_path} deve ser uma string")

    # Valida opções
    if template_field.get("options") and value not in template_field["options"]:
        raise ValueError(f"Valor inválido para {field_path}. Opções: {template_field['options']}")