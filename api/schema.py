from typing import List, Optional

from pydantic import BaseModel, constr, validator
from fastapi import HTTPException
from dateutil.parser import parse


class PessoaSchema(BaseModel):
    apelido: constr(max_length=32)
    nome: constr(max_length=100)
    nascimento: str
    stack: Optional[List[str]] = None
    
    @validator("stack", pre=True, each_item=True)
    def validate_stack_item(cls, value):
        if value is not None and not isinstance(value, str):
            raise HTTPException(
                status_code=400, 
                detail="stack deve conter apenas itens do tipo string",
            )
        elif value is not None and len(value) > 32:
            raise HTTPException(
                status_code=400, 
                detail="Cada item da stack deve ter no máximo 32 caracteres",
            )
        return value

    @validator("nome", pre=True)
    def validate_nome_type(cls, value):
        if not value:
            return HTTPException(
                status_code=422, detail="O campo 'nome' não pode ser nulo"
            )
        elif not isinstance(value, str):
            raise HTTPException(
                status_code=400, detail="O campo 'nome' deve ser uma string"
            )
        return value
    
    @validator("apelido", pre=True)
    def validate_apelido_type(cls, value):
        if not value:
            return HTTPException(
                status_code=422, detail="O campo 'apelido' não pode ser nulo"
            )
        elif not isinstance(value, str):
            raise HTTPException(
                status_code=400,
                detail="O campo 'apelido' deve ser uma string"
            )
        return value
    
    @validator("nascimento")
    def validate_nascimento_type(cls, value):
        if not value:
            return HTTPException(
                status_code=422,
                detail="O campo 'nascimento' não pode ser nulo"
            )
        try:
            parse(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="O campo 'nascimento' deve ser uma data válida no formato AAAA-MM-DD"
            )
        return value