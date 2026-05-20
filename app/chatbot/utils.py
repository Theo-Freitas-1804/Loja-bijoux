from .intents import INTENTS
import re
import random
import datetime as dt

from .dados import atendentes

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
    
def escolher_atendente():
  return random.choice(atendentes)