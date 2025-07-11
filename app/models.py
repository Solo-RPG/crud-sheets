from typing import Dict, Optional, Any, Union, List
from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Dict, Optional

SheetFieldValue = Union[str, int, float, bool, Dict[str, 'SheetField']]

class SheetField(BaseModel):
    value: SheetFieldValue
    required: bool = True  # Se o campo é obrigatório
    options: Optional[List[str]] = None

# Resolve referência circular
SheetField.model_rebuild()

class SheetForm(BaseModel):
    id: str  # ID da ficha
    template_id: str  # ID do sistema de RPG usado
    template_system_name: str  # Nome do sistema de RPG
    template_system_version: str  # Versão do sistema de RPG
    owner_id: str  # ID do dono da ficha
    data: Dict[str, SheetField]  # Dados dinâmicos

class SheetCreateRequest(BaseModel):
    template_id: Optional[str] = None
    system_name: Optional[str] = None
    owner_id: str
    # Mantemos apenas um campo para os dados
    fields: Dict[str, Any]  # Ou user_data, escolha um padrão

    @field_validator('template_id', 'system_name', mode='before')
    def validate_identifier(cls, v: Any, info: ValidationInfo) -> Any:
        data = info.data
        if not data.get('template_id') and not data.get('system_name'):
            raise ValueError("Pelo menos um identificador deve ser fornecido")
        return v