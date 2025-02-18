from flask import Flask
from app.routes import login_bp
from app.config.settings import Config

def create_app():
    app = Flask(__name__)

    app.register_blueprint(login_bp)
    app.config.from_object(Config)

    return app