from PIL import Image
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

# tenta importar rembg (sem quebrar o sistema)
try:
    from rembg import remove
    REMBG_OK = True
except:
    REMBG_OK = False

def processar_imagem(caminho_entrada, caminho_saida):
    input_image = Image.open(caminho_entrada).convert("RGBA")

    if REMBG_OK:
        try:
            sem_fundo = remove(input_image)
        except:
            sem_fundo = input_image
    else:
        sem_fundo = input_image

    # fundo branco
    fundo_branco = Image.new("RGBA", sem_fundo.size, (255, 255, 255, 255))
    fundo_branco.paste(sem_fundo, (0, 0), sem_fundo)

    final = fundo_branco.convert("RGB")

    # 🔥 mantém proporção
    final.thumbnail((500, 500))

    # 🔥 cria fundo quadrado
    fundo = Image.new("RGB", (500, 500), (255, 255, 255))

    # centraliza
    x = (500 - final.width) // 2
    y = (500 - final.height) // 2

    fundo.paste(final, (x, y))

    fundo.save(caminho_saida)

import os

def salvar_imagem_processada(img, pasta_destino):
    nome_seguro = secure_filename(img.filename)
    nome_unico = f"{uuid.uuid4()}_{nome_seguro}"
    caminho_original = os.path.join(current_app.root_path,"static/imagens/UPLOADS_FOTOS_BIJOUX",
    nome_unico
    )
    nome_final = nome_unico.rsplit(".", 1)[0] + ".jpg"
    caminho_final = os.path.join(
      current_app.root_path,
      pasta_destino,
      nome_final
      )
    # 💥 GARANTE QUE AS PASTAS EXISTEM
    os.makedirs(os.path.dirname(caminho_original), exist_ok=True)
    os.makedirs(os.path.dirname(caminho_final), exist_ok=True)
    # salva original
    img.save(caminho_original)
    # processa e salva final
    processar_imagem(caminho_original, caminho_final)
    # remove temporário
    if os.path.exists(caminho_original):
      os.remove(caminho_original)
    return nome_final
