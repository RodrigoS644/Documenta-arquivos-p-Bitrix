# app/config/settings.py

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'uma_chave_secreta_padrao')  # Usa variável de ambiente ou um valor padrão