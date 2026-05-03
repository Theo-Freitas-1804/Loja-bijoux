from flask import render_template, request, redirect, url_for
from .bp import admin_bp
from ..models import Produtos, db , Usuario

import datetime



@admin_bp.route("/clientes")
def consultar_clientes():
  clientes = Usuario.query.all()
 
  return render_template("Admin/users.html", clientes=clientes)