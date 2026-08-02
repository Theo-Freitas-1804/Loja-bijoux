from flask import Blueprint

bp_usuario = Blueprint("usuario", __name__ , url_prefix="/minha-conta")

from . import cupons
from . import endereco
from . import upload_foto
from . import pedidos
from . import editar_conta