from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import make_msgid

from dotenv import load_dotenv

from flask import render_template
from flask_login import current_user

from ..models import db , Usuario


import smtplib
import os

load_dotenv()

def enviar_token_senha(usuario):
  email_remetente= os.getenv("email_remetente")
  senha_app = os.getenv("senha")
  destino = usuario.email
  
  logo_id = make_msgid()
  
  expira = usuario.token_expira.strftime("%d/%m/%Y às %H:%M")
  
  html = render_template("emails/email_recuperar_senha.html" , usuario=usuario , logo_id=logo_id[1:-1] , expira=expira)
  msg = MIMEMultipart("related")
  msg.attach(MIMEText(html, "html"))
  msg["Subject"] = "Recuperação de senha"
  msg["From"] = email_remetente
  msg["To"] = destino

  with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    
    with open("app/static/imagens/logo.png" ,"rb") as img:
      imagem = MIMEImage(img.read())
    imagem.add_header("Content-ID" ,logo_id)
    msg.attach(imagem)
    server.login(email_remetente, senha_app)
    server.send_message(msg)
  
