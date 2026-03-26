from flask_login import login_required , current_user
from flask import redirect , url_for , abort
from functools import wraps


def admin_required(f):
    @wraps(f)
    @login_required # Primeiro, verifica se está logado
    def decorated_function(*args, **kwargs):
        # Segundo, verifica se o usuário NÃO é admin
        if not current_user.is_admin:
            # Se não for admin, redireciona para a página principal ou erro 403 
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
