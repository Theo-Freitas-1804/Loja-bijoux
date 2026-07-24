from flask import render_template, request, redirect, url_for , jsonify
from flask_login import login_required

from .bp import admin_bp

from ..models import db , Produtos , Usuario

from .services.filtros import filtrar_ticket_medio , filtrar_pedidos_cliente , filtrar_ultimo_acesso

from ..utils.tempo import tempo_desde

from ..decorators import admin_required

import datetime

@admin_bp.route("/clientes")
@admin_required
@login_required
def consultar_clientes():
  clientes = Usuario.query.all()
  return render_template(
      "Admin/users.html",
      clientes=clientes
  )

#dados dinâmicos

handlers_filtros = {
  "ticket_medio": filtrar_ticket_medio ,
  "pedidos": filtrar_pedidos_cliente ,
  "atividade": filtrar_ultimo_acesso
}

@admin_bp.route("/api/clientes")
@admin_required
@login_required
def api_clientes():
  
  opcao = request.args.get("opcao")
  print(opcao)
  print(handlers_filtros.keys())
  
  if opcao not in handlers_filtros:
    return jsonify({
      "erro": "Opção inexistente"
    }) , 400
  return jsonify(handlers_filtros[opcao]())