from flask import Blueprint, render_template , request , current_app , flash , redirect , url_for
from flask_login import login_user , logout_user , login_required , current_user
from ..rotas_principais.home import bp_principal
import os
import secrets
# Exemplo, assumindo que db está em 'app.meu_app' ou similar:
from ..meu_app import db 

 #1. Definição do Blueprint (Nome do Blueprint é 'usuario' para o url_for)
bp_usuario = Blueprint("usuario", __name__)
extensoes_imagens = ["png" , "jpg" , "gif"]

@bp_usuario.route("/minha-conta")
def perfil():
    # A variável caminho_icone não está sendo usada, mas a função está correta
    return render_template("perfil.html" , name= current_user.nome)

def arquivo_permitido(filename):
    # 1. Checa se o nome tem ponto (necessário para os.path.sp    litext)
    if not "." in filename:
        return False
    # 2. Extrai a extensão, converte para minúsculas e remove     o ponto
    _, extensao = os.path.splitext(filename)
    extensao_limpa = extensao.lower().replace(".", "")
    # 3. Retorna TRUE ou FALSE com base na checagem
    return extensao_limpa in extensoes_imagens


@bp_usuario.route("/minha-conta/sair")
@login_required
def sair():
    # 1. Encerra a sessão do Flask-Login e remove o cookie de logi    n
    logout_user()
    # 2. Redireciona para a página principal
    return redirect(url_for("principal.pagina_principal"))
    
@bp_usuario.route("/meu-perfil/deletar-conta")
@login_required
def deletar_conta():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return url_for('principal.pagina_principal')
