import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

def enviar_codigo_verificacao(email_destino: str, codigo: str):
    email_host = os.getenv("EMAIL_HOST")
    email_port = int(os.getenv("EMAIL_PORT"))
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")

    try:
        server = smtplib.SMTP(email_host, email_port)
        server.starttls()
        server.login(email_user, email_password)

        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_destino
        msg['Subject'] = 'Código de Verificação'
        body = f'O seu código de verificação é: {codigo}'
        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(email_from, email_destino, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        raise

def consultar_cep(cep: str):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Erro ao consultar o CEP")

    data = response.json()
    if "erro" in data:
        raise ValueError("CEP inválido")

    return {
        "logradouro": data.get("logradouro"),
        "bairro": data.get("bairro"),
        "cidade": data.get("localidade"),
        "estado": data.get("uf")
    }
