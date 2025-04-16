from pydantic import BaseModel, EmailStr
from typing import Optional

class IniciarCadastro(BaseModel):
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True

class VerificarCadastro(BaseModel):
    email: EmailStr
    codigo: str

class CadastrarEndereco(BaseModel):
    email: EmailStr
    cep: str
    numero: str
    referencia: Optional[str] = None

    class Config:
        orm_mode = True
