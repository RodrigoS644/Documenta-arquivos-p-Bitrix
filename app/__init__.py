from flask import Flask
from app.routes import login_bp
from app.routes import placa_task_bp
from app.config.settings import Config
from app.routes import doc_bp
import os
def create_app():
    app = Flask(__name__)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Raiz do projeto
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
    app.register_blueprint(doc_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(placa_task_bp)
    app.config.from_object(Config)

    return app