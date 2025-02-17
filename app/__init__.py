

from flask import Flask

def create_app():
    """
    Factory function para criar e configurar a aplicação Flask.
    """
    # Cria a instância do Flask
    app = Flask(__name__)

    # Configurações básicas (vamos adicionar mais depois)
    app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_segura'

    # Rota de exemplo para testar se o Flask está funcionando
    @app.route('/')
    def hello():
        return "Olá, mundo! O Flask está funcionando!"

    return app