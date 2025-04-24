
# 🚀 API de Cadastro de Usuários com Verificação por Código e Endereço via CEP

Este projeto é uma API REST construída com **FastAPI** que realiza o cadastro de usuários em duas etapas:

1. Envio de nome e e-mail com código de verificação por e-mail.  
2. Validação do código e finalização do cadastro com o endereço via CEP.

## 🧠 Visão Geral do Projeto

A proposta desta API é simular um fluxo completo de cadastro de usuários, muito comum em sistemas como **e-commerces**, **plataformas de serviços** ou **sites de reservas de viagem**.

O processo é dividido em três etapas principais:

- O usuário envia seu **nome** e **e-mail**. Um código de verificação é gerado e enviado por e-mail.  
- O usuário insere o **código recebido por e-mail** para validar o cadastro.  
- Após a validação, o usuário informa o **CEP**, e a API consulta automaticamente o endereço completo via integração com o ViaCEP.

⚠️ **Observações**:  
- Foi adicionado um sistema de autenticação simples para facilitar os testes (os detalhes para testar são enviados no privado).  
- Caso haja falha na geração ou envio do código por e-mail, é possível utilizar o **código 010101** como um *bypass* para avançar no processo.  
- Todo o processo é registrado em **logs**.

---

## 🔧 Tecnologias utilizadas

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Requests
- Pydantic

---

## ▶️ Como executar o projeto localmente

```bash
# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Rode a aplicação
uvicorn main:app --reload
```

---

## 🌐 Rotas da API (hospedada no Render)

### 📩 Cadastro inicial de usuário  
`POST /usuarios/cadastro_inicial`  
Envia o código de verificação para o e-mail informado.

```bash
curl --location 'https://cadastro-fast-api.onrender.com/usuarios/cadastro_inicial'   --header 'Authorization: Bearer token'   --header 'Content-Type: application/json'   --data '{
    "nome": "João da Silva",
    "email": "joao.silva@email.com"
  }'
```

---

### ✅ Verificação de código  
`POST /usuarios/verificar_codigo`  
Valida o código de verificação enviado por e-mail.

```bash
curl --location 'https://cadastro-fast-api.onrender.com/usuarios/verificar_codigo'   --header 'Authorization: Bearer token'   --header 'Content-Type: application/json'   --data '{
    "email": "joao.silva@email.com",
    "codigo": "010101"
  }'
```

---

### 🏠 Finalização do cadastro com CEP  
`POST /usuarios/finalizar_cadastro`  
Consulta endereço via CEP e finaliza o cadastro.

```bash
curl --location 'https://cadastro-fast-api.onrender.com/usuarios/finalizar_cadastro'   --header 'Authorization: Bearer token'   --header 'Content-Type: application/json'   --data '{
    "email": "joao.silva@email.com",
    "cep": "12345678",
    "numero": "123",
    "referencia": "próximo à praça central"
  }'
```

---

### ❌ Remover usuário  
`DELETE /usuarios/delete/{email}`

```bash
curl --location --globoff --request DELETE 'https://cadastro-fast-api.onrender.com/usuarios/delete/{email}'   --header 'Authorization: Bearer token'
```

---

### 📋 Listar todos os usuários  
`GET /usuarios`

```bash
curl --location 'https://cadastro-fast-api.onrender.com/usuarios'   --header 'Authorization: Bearer token'
```

---

### 📑 Ver logs de uso  
`GET /logs`

```bash
curl --location 'https://cadastro-fast-api.onrender.com/logs'   --header 'Authorization: Bearer token'
```
