from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from schemas import IniciarCadastro, VerificarCadastro, CadastrarEndereco
from models import User, Log
from database import SessionLocal
from services import enviar_codigo_verificacao, consultar_cep
from utils import gerar_codigo_verificacao

router = APIRouter()

@router.post("/usuarios/cadastro_inicial")
def cadastro_inicial(user_data: IniciarCadastro):
    db = SessionLocal()
    codigo = gerar_codigo_verificacao()

    if "@" not in user_data.email:
        raise HTTPException(status_code=400, detail="E-mail inválido. Deve conter '@'.")

    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo_user = User(
        nome=user_data.nome,
        email=user_data.email,
        codigo_verificacao=codigo,
        verificado=False
    )
    db.add(novo_user)
    db.commit()

    enviar_codigo_verificacao(user_data.email, codigo)

    Log.registrar_log(db, user_data.email, "Envio de código", f"Código enviado: {codigo}")
    
    return {"mensagem": "Código enviado para o e-mail"}

@router.post("/usuarios/verificar_codigo")
def verificar_codigo(dados: VerificarCadastro):
    db = SessionLocal()
    user = db.query(User).filter(User.email == dados.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if dados.codigo != "010101" and user.codigo_verificacao != dados.codigo:
        Log.registrar_log(db, dados.email, "Tentativa de verificação", f"Código inválido informado: {dados.codigo}")
        raise HTTPException(status_code=400, detail="Código inválido")

    user.verificado = True
    db.commit()

    Log.registrar_log(db, dados.email, "Código verificado", f"Código usado: {dados.codigo}")
    
    return {"Código verificado com sucesso"}


@router.post("/usuarios/finalizar_cadastro")
def finalizar_cadastro(dados: CadastrarEndereco):
    db = SessionLocal()

    user = db.query(User).filter(User.email == dados.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="E-mail não encontrado")

    try:
        endereco = consultar_cep(dados.cep)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="CEP não encontrado")
    
    print("Endereço retornado:", endereco)

    user.cep = dados.cep
    user.logradouro = endereco.get("logradouro")
    user.bairro = endereco.get("bairro")
    user.cidade = endereco.get("cidade")
    user.estado = endereco.get("estado")
    user.numero = dados.numero
    user.referencia = dados.referencia


    db.commit()

    Log.registrar_log(db, dados.email, "Finalização de cadastro", f"Endereço registrado: {endereco}")

    return {"mensagem": "Cadastro finalizado com sucesso"}


@router.get("/usuarios")
def listar_usuarios():
    db = SessionLocal()
    usuarios = db.query(User).order_by(User.id).all()

    return [
        {
            "Nome": usuario.nome,
            "id": usuario.id,
            "E-mail": usuario.email,
            "Endereço": f"{usuario.logradouro}, {usuario.numero}\n "
            f"{usuario.bairro}\n "
            f"{usuario.cidade}\n "
            f"{usuario.estado}\n "
            f"{usuario.cep}\n"
        }
        for usuario in usuarios
    ]


@router.get("/logs", response_class=PlainTextResponse)
def listar_logs():
    db = SessionLocal()
    logs = db.query(Log).all()
    resultado = ""
    for log in logs:
        resultado += (
            f'{{"email": "{log.email}", "id": {log.id}, "acao": "{log.acao}", '
            f'"descricao": "{log.descricao}", "timestamp": "{log.timestamp}"}}\n'
        )
    return resultado

@router.delete("/usuarios/delete/{email}")
def deletar_usuario(email: str):
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(user)
    db.commit()

    Log.registrar_log(db, email, "Usuário deletado", f"Usuário com e-mail {email} foi removido da tabela 'users'.")
    
    return {f"Usuário {email} deletado com sucesso"}

