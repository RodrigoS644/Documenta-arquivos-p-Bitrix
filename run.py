# run.py

from app import create_app
from flask import Flask



  # Carrega variáveis do .env
app = Flask(__name__)


# Cria a aplicação Flask
app = create_app()

if __name__ == '__main__':
    # Roda a aplicação em modo de desenvolvimento
    app.run(debug=True)