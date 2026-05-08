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

def salvar_imagem_processada(img, pasta_destino):

  # nome seguro
  nome_seguro = secure_filename(img.filename)

  # uuid + nome original
  nome_unico = f"{uuid.uuid4()}_{nome_seguro}"

  # nome final SEMPRE jpg
  nome_final = nome_unico.rsplit(".", 1)[0] + ".jpg"

  # =========================
  # PASTA TEMPORÁRIA
  # =========================
  pasta_temp = os.path.join(
      current_app.root_path,
      "static/temp"
  )

  os.makedirs(pasta_temp, exist_ok=True)

  caminho_original = os.path.join(
      pasta_temp,
      nome_unico
  )

  # =========================
  # DESTINO FINAL
  # =========================
  caminho_final = os.path.join(
      current_app.root_path,
      pasta_destino,
      nome_final
  )

  # garante pasta final
  os.makedirs(
      os.path.dirname(caminho_final),
      exist_ok=True
  )

  try:

      # salva original temporário
      img.save(caminho_original)

      print("ORIGINAL SALVO:", caminho_original)

      # processa imagem
      processar_imagem(
          caminho_original,
          caminho_final
      )

      print("FINAL SALVO:", caminho_final)

      # remove temporário SOMENTE se final existir
      if os.path.exists(caminho_final):

          os.remove(caminho_original)

          print("TEMP REMOVIDO")

      else:

          print("ERRO: imagem final não criada")

          return None

      return nome_final

  except Exception as erro:

      print("ERRO AO SALVAR IMAGEM:", erro)

      return None
