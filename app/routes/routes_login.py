from flask import render_template , Blueprint

login_bp = Blueprint('login_routes', __name__)

@login_bp.route('/')
def home():
    return render_template('login.html')