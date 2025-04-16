# API de Cadastro de Usuários com Verificação por Código e Endereço via CEP

Este projeto é uma API REST construída com **FastAPI** que realiza o cadastro de usuários em duas etapas:

1. Envio de nome e e-mail com código de verificação por e-mail.
2. Validação do código e finalização do cadastro com o endereço via CEP.

## Funcionalidades

- Cadastro inicial com envio de e-mail
- Validação de código de verificação
- Consulta de endereço via API de CEP
- Registro de logs
- Validação de dados com Pydantic

## Tecnologias utilizadas

- Python 3.10+
- FastAPI
- SQLAlchemy
- Postgre
- Requests
- Pydantic

## Como executar o projeto

```bash
# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Rode a aplicação
uvicorn main:app --reload
