from flask import render_template, request, redirect, url_for
from .bp import admin_bp
from ..models import Produtos, db , Usuario

import datetime



@admin_bp.route("/clientes")
def consultar_clientes():
  users = Usuario.query.all()
  dados_tratados = []

  for user in users:
      if user.data_registro:
          hora = user.data_registro.strftime("%d/%m/%y | %H:%M")
      else:
          hora = "-"

      dados_tratados.append({
          "nome": user.nome,
          "email": user.email,
          "hora": hora
      })

  return render_template("Admin/users.html", users=dados_tratados)