#app/rotas_auth/auth.py

from flask import Blueprint, render_template , request , redirect , url_for
from flask_login import login_user

from werkzeug.security import check_password_hash , generate_password_hash
from sqlalchemy import or_
from ..models import Usuario , db
# O nome do Blueprint é 'auth'
bp_auth = Blueprint("auth", __name__)

@bp_auth.route("/cadastro" , methods = ["GET", "POST"])
def criar_conta():
    if request.method == "GET":
        return render_template("criar_conta.html")
    elif request.method == "POST":
        nome_cliente = request.form.get('Nome_cliente')
        email_cliente = request.form.get('email_cliente')
        senha_cliente = request.form.get('senha_cliente')
        senha = generate_password_hash(senha_cliente)
        nova_usuaria = Usuario(nome = nome_cliente , email = email_cliente , senha = senha)
        db.session.add(nova_usuaria)
        db.session.commit() 
        login_user(nova_usuaria)

    return redirect(url_for("principal.pagina_principal"))

@bp_auth.route("/login" , methods= ["GET" , "POST"])
def entrar():
    if request.method == "GET":
        return render_template("entrar.html")  
    elif request.method == "POST":     
        # 47-49: Coletando dados (Correto)
        identificador = request.form.get("id_cliente")
        senha_digitada = request.form.get("senha_cliente")
        # 50-55: A Query OR (Sintaxe Corrigida)
        # A consulta OR precisa de (())) para fechar as duas funções
        usuario_encontrado = Usuario.query.filter(
                or_(
                    Usuario.nome == identificador,
                    Usuario.email == identificador
                )).first()
        # 57-64: Bloco de Verificação (Indentação Corrigida)
        if usuario_encontrado:
            # A senha está correta?        
            if check_password_hash(usuario_encontrado.senha, senha_digitada):
                login_user(usuario_encontrado)                      # Login bem-sucedido!
                return redirect(url_for("principal.pagina_principal"))
            else:
                # Senha incorreta
                return "Nome / Senha incorreto(s)" # Corrigindo o erro d
        else:
            # Usuário não encontrado (Nome ou Email inválido)
            return "Nome/E-mail/ Senha incorretos"

@bp_auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("principal.pagina_principal"))

