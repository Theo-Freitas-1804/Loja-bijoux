import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

def enviar_token_senha(destino, codigo):
 email= os.getenv("email_remetente")
 senha_app = os.getenv("senha")
 html = f"""
 <html>
 <body style="margin:0; padding:0; font-family:Arial, sans-serif; background:#f5f5f5;">
 <table width="100%" cellpadding="0" cellspacing="0">
 <tr>
 <td align="center">
 <table width="400" cellpadding="20" cellspacing="0" style="background:white; border-radius:10px;">
 <tr>
 <td align="center">
 <h2>Kordonê Bijoux</h2>
 </td>
 </tr>
 <tr>
 <td align="center">
 <p>Você solicitou redefinir sua senha</p>
 <h1 style="letter-spacing:5px;">
 {codigo}
 </h1>
 <p style="color:#777;">
 Expira em 15 minutos
 </p>
 </td>
 </tr>
 </table>
 </td>
 </tr>
 </table>
 </body>
 </html>
 """
 msg = MIMEText(html, "html")
 msg["Subject"] = "Recuperação de senha"
 msg["From"] = email_remetente
 msg["To"] = destino
 with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(email_remetente, senha)
    server.send_message(msg)