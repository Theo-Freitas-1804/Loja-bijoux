from .intents import INTENTS
import re

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