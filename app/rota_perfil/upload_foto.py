from flask import Blueprint, render_template , request , current_app , flash , redirect , url_for
from flask_login import login_user , logout_user , login_required , current_user
from ..rotas_principais.home import bp_principal

from .perfil import bp_usuario , arquivo_permitido
import os
import secrets


@bp_usuario.route("/minha-conta/editar-dados", methods= ["GET" , "POST"])
def upload_foto():
    if request.method == 'POST':
        imagem_adicionada = request.files.get("imagem_adicionada")
        #1. Cheque de segurança (Arquivo e Nome)
        if not imagem_adicionada or not imagem_adicionada.filename: 
            # ✅ Correção: return redirect() e 'error' como string literal
            flash("Arquivo não encontrado" , "error")
            return redirect(url_for('usuario.perfil'))

        # 2. Cheque de segurança (Extensão)
        if arquivo_permitido(imagem_adicionada.filename):
            # Tudo certo! Próximo passo: Salvar o arquivo
            # ✅ Correção: 'success' com dois 'c'
            # O código de SALVAMENTO entrará AQUI, antes do redirecionamento
            _, extensao = os.path.splitext(imagem_adicionada.filename)
            nome_aleatorio = secrets.token_hex(8)
            nome_arquivo = nome_aleatorio + extensao
            
            savepath = os.path.join(
              current_app.root_path,"static/imagens/UPLOADS_FOTOS_PERFIL", nome_arquivo
              )
            
            diretorio_upload = os.path.dirname(savepath)
            os.makedirs(diretorio_upload, exist_ok=True)
            # Linhas 181-187 (Ajuste no app.py)
            try:
              print("SALVANDO EM:", savepath)
              imagem_adicionada.save(savepath)
              # 1. Atribui o caminho:
              caminho_salvo = nome_arquivo
              # app.py, dentro de upload_foto
              current_user.foto_perfil = caminho_salvo
              # VERIFICAÇÃO FINAL: Imprime o que FOI SALVO no banco
               # 2. Persiste a mudança no banco de dados
              db.session.commit()
              flash("Envio bem-sucedido" , "sucess")
              return redirect(url_for('principal.pagina_principal'))
            except Exception as e:
                print(f"Erro ao enviar a foto {e}")
                return redirect(url_for('usuario.perfil'))
        else:
            # Extensão não permiatida! Retorna com erro
            # ✅ Correção: return redirect()
            flash("Extensão inválida, tente outro arquivo", "error")
            return redirect(url_for('perfil'))
    elif request.method == "GET":
      return render_template("perfil.html")
