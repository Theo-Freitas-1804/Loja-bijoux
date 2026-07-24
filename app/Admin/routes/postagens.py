# Admin/routes/acessorios.py

from flask import Blueprint, render_template, request , jsonify , url_for , redirect , current_app
from flask_login import login_required

import os
import datetime as dt

from ...decorators import admin_required

from app.chatbot.dados import atendentes

from ..bp import admin_bp

from ...models import db,  Conteudo , Produtos , Banners

from ..services.acessorios import criar_banner

@admin_bp.route("/gerenciar")
@admin_required
def visao_geral():
  
  for atendente in atendentes:
    atendente["foto_url"] = (
        url_for(
            "static",
            filename=f"imagens/attendants/{atendente['foto']}"
        )
        if atendente["foto"]
        else None
    )
    
  produtos = Produtos.query.filter(Produtos.em_estoque >= 1).all()
  
  return render_template("Admin/posts.html" , atendentes=atendentes , produtos=produtos)
  
@admin_bp.route("/gerenciar/atendente/editar", methods=["POST"])
@admin_required
def editar_atendente():
  id_atendente = int(request.form.get("id"))
  nome_atendente = request.form.get("nome")
  foto= request.files.get("foto-atendente")
  cargo= request.form.get("cargo")
  funcoes = request.form.getlist("funcoes")
  
  path = os.path.join("app", "static", "imagens", "attendants")
  
    
  mensagem = None
  
  if foto and foto.filename:
    nome_original , extensao = os.path.splitext(foto.filename)
    nome_novo = nome_atendente
    arquivo = f"{nome_novo}{extensao}"
    caminho = os.path.join(path , arquivo)
    try:
      foto.save(caminho)
      mensagem = "Foto adicionada com sucesso!"
    except Exception as e:
      mensagem = "Não foi possível salvar"
  else:
    extensao = None
    nome_original = None
    nome_novo= None
    arquivo = None
  for a in atendentes:
    if a["id"] == id_atendente:
      a["nome"] = nome_atendente
      a["cargo"] = cargo
      a["especialidade"] = funcoes
      if arquivo:
        a["foto"] = arquivo
      break
    
  return jsonify({
    "sucesso": True,
    "mensagem": "Atendente atualizado."
})
  
@admin_bp.route("/api/gerenciar/atendente/<int:id>")
def api_atendentes(id):
  print(" API CHAMADA! ".center(60, "="))
  for a in atendentes:
    if a["id"] == id:
      return jsonify(a)
    
  return None

@admin_bp.route("/gerenciar/atendente/nova", methods=["POST"])
@admin_required
def criar_nova_atendente():
  
  foto_nova = request.files.get("foto-nova-atendente")
  nome_nova = request.form.get("nome-nova")
  cargo_nova = request.form.get("cargo-nova")
  espec_nova = request.form.getlist("especialidade-nova")
  
  path = os.path.join("app", "static", "imagens", "attendants")
  
  mensagem = None
  
  maior_id = max(a["id"] for a in atendentes)
  
  if foto_nova and foto_nova.filename:
    nome_original , extensao = os.path.splitext(foto_nova.filename)
    nome_novo = nome_nova
    arquivo_nova = f"{nome_novo}{extensao}"
    caminho = os.path.join(path , arquivo_nova)
    try:
      foto_nova.save(caminho)
      mensagem = "Foto adicionada com sucesso!"
    except Exception as e:
      mensagem = "Não foi possível salvar"
  else:
    extensao = None
    nome_original = None
    nome_novo= None
    arquivo_nova = None
  
  
  nova_atendente = {
    "id": maior_id + 1,
    "nome": nome_nova ,
    "foto": arquivo_nova ,
    "cargo": cargo_nova ,
    "especialidade": espec_nova
  }
  atendentes.append(nova_atendente)
  return jsonify({
    "sucesso": True,
    "mensagem": "Atendente criado com sucesso!"
  })
  
@admin_bp.route("/upload-conteudo" , methods=["POST"])
def upload_conteudo():
  
  paths = {
      "tutoriais": os.path.join(current_app.static_folder, "imagens", "tutoriais"),
      "banners": os.path.join(current_app.static_folder, "imagens", "banners"),
      "looks": os.path.join(current_app.static_folder, "imagens", "looks"),
  }
  
  arquivo = request.files.get("midia")
  nome = request.form.get("nome_arquivo")
  categoria = request.form.get("tipo")
  
  for pasta in paths.values():
    os.makedirs(pasta, exist_ok=True)
  
  print("Arquivo:", arquivo)
  print("Filename:", arquivo.filename if arquivo else None)
  print("Categoria:", categoria)
  print("Nome:", nome)
  
  if arquivo and arquivo.filename:
    
    _, extensao = os.path.splitext(arquivo.filename)
    arquivo_final = f"{nome}{extensao}"
    pasta = paths[categoria]
    caminho = os.path.join(pasta, arquivo_final)
    try:
      print("Vai salvar em:", os.path.abspath(caminho))
      arquivo.save(caminho)
      print("Arquivo salvo com sucesso!")
    except Exception as e:
      return {"mensagem":f" Impossível salvar , {e}"}
      
    print("IF começou")
    match categoria:
      case "tutoriais":
        print("Case tutorial on")
        
        novo = Conteudo(
          tipo=categoria,
          titulo=nome,
          arquivo=arquivo_final,
          descricao=None
        )
        db.session.add(novo)
        db.session.commit()
      case "banners":
        print("case banner on")
        criar_banner(arquivo , pasta , nome)
      case "looks":
        print("case looks")
        
        novo = Conteudo(
          tipo=categoria,
          titulo=nome,
          arquivo=arquivo_final,
          descricao=None
        )
        
        db.session.add(novo)
        db.session.commit()
    
  return redirect(url_for("principal.pagina_principal"))