from flask import render_template, request, redirect, url_for
from flask_login import login_required

from .bp import admin_bp
from ..models import Produtos, db , Usuario

from ..decorators import admin_required
print(admin_required)

import datetime

@admin_bp.route("/clientes")
@admin_required
@login_required
def consultar_clientes():
  print("ROTA CLIENTES EXECUTOU")

  clientes = Usuario.query.all()
  print(consultar_clientes)
  return render_template(
      "Admin/users.html",
      clientes=clientes
  )