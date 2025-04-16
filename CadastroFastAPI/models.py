from sqlalchemy import Column, Integer, String, Integer, Boolean, DateTime
from database import Base
from sqlalchemy.orm import Session
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    codigo_verificacao = Column(String)
    verificado = Column(Boolean, default=False)
    cep = Column(String)
    logradouro = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    referencia = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<User(id={self.id}, nome={self.nome}, email={self.email}, "
            f"verificado={self.verificado}, numero={self.numero}, referencia={self.referencia})>"
        )

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    acao = Column(String)
    descricao = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Log(id={self.id}, email={self.email}, acao={self.acao}, descricao={self.descricao})>"

    @staticmethod
    def registrar_log(db: Session, email: str, acao: str, descricao: str):
        novo_log = Log(email=email, acao=acao, descricao=descricao)
        db.add(novo_log)
        db.commit()