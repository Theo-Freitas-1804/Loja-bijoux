import requests
from flask_login import current_user
from app.models import db ,Endereco


def calcular_frete(cep):
    if cep.startswith("01"):
        return 12.90
    elif cep.startswith("20"):
        return 18.50
    else:
        return 25.00
        

from app.models import db, Endereco

import requests


def salvar_endereco(
    usuario,
    rua,
    numero,
    bairro,
    cidade,
    cep,
    tipo
):

  cep_limpo = cep.replace("-", "").strip()

  url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

  res = requests.get(url, timeout=3)

  if res.status_code != 200:
      raise ValueError("Erro ao consultar CEP")

  dados = res.json()

  if "erro" in dados:
      raise ValueError("CEP inválido")

  estado = dados.get("uf")

  if not estado:
      raise ValueError("Estado não encontrado")

  novo = Endereco(
      rua=rua,
      numero=numero,
      bairro=bairro,
      cidade=cidade,
      cep=cep,
      tipo=tipo,
      estado=estado,
      cliente_id=usuario.id_usuaria
  )

  db.session.add(novo)
  db.session.commit()

  return novo
