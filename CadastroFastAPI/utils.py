import random
import string
import requests

def gerar_codigo_verificacao(tamanho=6):

    return ''.join(random.choices(string.digits, k=tamanho))

def consultar_cep(cep: str):

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Erro ao consultar o CEP. Verifique o formato ou a disponibilidade da API.")
