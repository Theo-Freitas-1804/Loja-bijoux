import re
import random
import datetime as dt
from flask_login import current_user

from .dados import atendentes

from .intents import INTENTS , INTENTS_ADMIN , FOCOS_AJUDA

def detectar_intencao(msg):
  for intent , palavras in INTENTS.items():
    if any(p in msg for p in palavras):
      return intent
  return None
  

def extrair_cep(msg):
    match = re.search(r"\d{5}-?\d{3}", msg)
    if match:
        return match.group().replace("-", "")
    return None

def transferir_conversa(intent ,atendente_atual):
  if intent in atendente_atual["especialidade"]:
    return atendente_atual
  
  for atendente in atendentes:
    if intent in atendente["especialidade"]:
      return atendente
  
  return atendente_atual
  
def detectar_intencao_admin(msg):
  msg = msg.lower()
  for intent, palavras in INTENTS_ADMIN.items():
    for palavra in palavras:
      if palavra.lower() in msg:
        return intent

  return None
  
def detectar_intencao_chat(msg):

  if current_user.is_admin:

      intent = detectar_intencao_admin(msg)

      if intent:
          return intent

      foco = detectar_foco(msg)

      if foco:
          return "pedidos"

      return detectar_intencao(msg)

  return detectar_intencao(msg)
  
def detectar_foco(msg):
  msg = msg.lower()

  for foco, palavras in FOCOS_AJUDA.items():
      for palavra in palavras:
          if palavra in msg:
              return foco

  return None
  
def escolher_atendente():
  return random.choice(atendentes)