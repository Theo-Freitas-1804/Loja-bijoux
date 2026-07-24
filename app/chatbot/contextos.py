from flask import session , request
from flask_login import current_user

from .utils import escolher_atendente , detectar_intencao_chat , detectar_foco
from .dados import atendentes

from .intents import *

import datetime as dt

def buscar_atendente(nome):
  for atendente in atendentes:
      if atendente["nome"] == nome:
          return atendente
  return None
  
def montar_contexto_chat():
  fuso = dt.timezone(dt.timedelta(hours= -3))
  
  agora = dt.datetime.now(fuso)
  hora = agora.strftime("%H:%M")
  
  if "atendente" not in session:
    if current_user.is_admin:
      session["atendente"] = buscar_atendente("Amanda")
    else:
      session["atendente"] = escolher_atendente()
  atendente = session["atendente"]
  
  msg = request.form.get("pergunta" , "").lower()
  return({
    "hora":hora ,
    "msg": msg ,
    "estado": session.get("estado_chat") ,
    "atendente": atendente ,
    "intent": detectar_intencao_chat(msg) ,
    "foco": detectar_foco(msg) , 
    "usuaria": current_user
  })
  
  