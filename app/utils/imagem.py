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

    # RGB final
    final = fundo_branco.convert("RGB")

    # 🔥 CORREÇÃO DO SEU BUG
    final = final.resize((500, 500))

    final.save(caminho_saida)


def salvar_imagem_processada(img, pasta_destino):
    nome_seguro = secure_filename(img.filename)
    nome_unico = f"{uuid.uuid4()}_{nome_seguro}"

    caminho_original = os.path.join(
        current_app.root_path,
        "static/imagens/temp",
        nome_unico
    )

    nome_final = nome_unico.rsplit(".", 1)[0] + ".jpg"

    caminho_final = os.path.join(
        current_app.root_path,
        pasta_destino,
        nome_final
    )

    img.save(caminho_original)

    processar_imagem(caminho_original, caminho_final)

    # remove temporário
    if os.path.exists(caminho_original):
        os.remove(caminho_original)

    return nome_final