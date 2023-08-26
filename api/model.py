from typing import Optional
from sqlmodel import SQLModel, Field


class Pessoa(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    apelido: str = Field(unique=True)
    nome: str
    nascimento: str
    stack: Optional[str] = None
