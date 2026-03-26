# run.py

from app.meu_app import create_app

# Cria a instância do app chamando a função de fábrica
app = create_app()

if __name__ == '__main__':
    # Inicia o servidor em modo de desenvolvimento
    app.run(debug=True)

