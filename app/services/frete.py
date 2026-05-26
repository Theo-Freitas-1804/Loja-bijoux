import requests
from flask_login import current_user
from app.models import db ,Endereco
from flask import request

from datetime import datetime, timedelta

def calcular_frete(cep_ou_endereco):

  # =========================
  # ACEITA CEP OU OBJETO
  # =========================

  if hasattr(cep_ou_endereco, "cep"):

      cep = cep_ou_endereco.cep

  else:

      cep = cep_ou_endereco

  # =========================
  # LIMPEZA
  # =========================

  cep = str(cep).replace("-", "").strip()

  # =========================
  # BASE MOCK
  # =========================

  if cep.startswith("01"):

      pac = 12.90
      sedex = 21.90

      dias_pac = 5
      dias_sedex = 2

  elif cep.startswith("20"):

      pac = 18.50
      sedex = 29.90

      dias_pac = 8
      dias_sedex = 3

  else:

      pac = 25.00
      sedex = 39.90

      dias_pac = 15
      dias_sedex = 7

  # =========================
  # DATAS
  # =========================

  hoje = datetime.now()

  entrega_pac = (
      hoje + timedelta(days=dias_pac)
  ).strftime("%d/%m")

  entrega_sedex = (
      hoje + timedelta(days=dias_sedex)
  ).strftime("%d/%m")

  # =========================
  # RETORNO
  # =========================

  fretes = {

      "pac": {

          "valor": pac,

          "prazo": dias_pac,

          "entrega": entrega_pac

      },

      "sedex": {

          "valor": sedex,

          "prazo": dias_sedex,

          "entrega": entrega_sedex

      }

  }

  return fretes

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
