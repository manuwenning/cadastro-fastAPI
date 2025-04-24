import random
import string
import requests
import os
from fastapi import Header, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

def verificar_token(authorization: str = Header(...)):

    if authorization != f"Bearer {TOKEN}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )


def gerar_codigo_verificacao(tamanho: int = 6) -> str:

    return ''.join(random.choices(string.digits, k=tamanho))


def consultar_cep(cep: str) -> dict:

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "erro" in data:
            raise ValueError("CEP não encontrado.")
        return data
    else:
        raise ValueError("Erro ao consultar o CEP")
