from flask import Blueprint, render_template , request , current_app , flash , redirect , url_for
from flask_login import login_user , logout_user , login_required , current_user
from ..rotas_principais.home import bp_principal

from .perfil import bp_usuario


import requests

@bp_usuario.route("/minha-conta/novo-endereco", methods=["GET", "POST"])
def adicionar_endereco():
  from ..models import db , Endereco
  print("🔥 ROTA CHAMADA")

  if request.method == "GET":
      print("📥 GET detectado")
      return render_template("perfil.html")

  # POST
  print("📤 POST detectado")

  rua = request.form.get("rua")
  numero = request.form.get("numero")
  bairro = request.form.get("bairro")
  cidade = request.form.get("cidade")
  cep = request.form.get("cep")
  tag = request.form.get("tipo")

  print("📦 DADOS FORM:")
  print("Rua:", rua)
  print("Numero:", numero)
  print("Bairro:", bairro)
  print("Cidade:", cidade)
  print("CEP:", cep)
  print("Tipo:", tag)

  if not cep:
      print("❌ CEP vazio")
      flash("CEP não informado")
      return redirect(url_for("usuario.perfil"))

  cep_limpo = cep.replace("-", "").strip()
  url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

  print("🌐 Consultando ViaCEP:", url)

  try:
      res = requests.get(url, timeout=3)
      print("📡 STATUS CODE:", res.status_code)

      if res.status_code != 200:
          print("❌ Erro HTTP na API")
          flash("Erro ao consultar CEP")
          return redirect(url_for("usuario.perfil"))

      dados = res.json()
      print("📨 RESPOSTA API:", dados)

      if "erro" in dados:
          print("❌ CEP inválido")
          flash("CEP inválido, tente novamente")
          return redirect(url_for("usuario.perfil"))

  except Exception as e:
      print("💥 EXCEÇÃO:", e)
      flash("Erro na conexão com o serviço de CEP")
      return redirect(url_for("usuario.perfil"))

  estado = dados.get("uf")
  print("📍 ESTADO:", estado)

  if not estado:
      print("❌ Estado não encontrado")
      flash("Erro ao obter estado do CEP")
      return redirect(url_for("usuario.perfil"))

  print("👤 USER ID:", current_user.id_usuaria)

  novo = Endereco(
      rua=rua,
      numero=numero,
      bairro=bairro,
      cidade=cidade,
      cep=cep,
      tipo=tag,
      estado=estado,
      cliente_id=current_user.id_usuaria
  )

  print("💾 SALVANDO NO BANCO...")

  try:
      db.session.add(novo)
      db.session.commit()
      print("✅ SALVO COM SUCESSO")

  except Exception as e:
      print("💥 ERRO AO SALVAR:", e)
      db.session.rollback()
      flash("Erro ao salvar endereço")
      return redirect(url_for("usuario.perfil"))

  flash("Endereço salvo com sucesso!")
  return redirect(url_for("usuario.perfil"))