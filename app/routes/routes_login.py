from flask import render_template , Blueprint
import sys
from flask import Blueprint, request, jsonify, render_template, Flask, session, redirect, url_for
import os
from configDB.Funcoes_db import (
    inserir_usuario, consultar_usuarios, consultar_usuario_por_id,
    atualizar_usuario, deletar_usuario, verificar_login
)




login_bp = Blueprint('login_routes', __name__)



@login_bp.route('/')
def home():
    return render_template('login.html')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cria uma instância do Flask
  # Define o caminho para os templates

# Rota para inserir um novo usuário
@login_bp.route('/usuarios', methods=['POST'])
def adicionar_usuario():
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login'))

    if request.is_json:
        dados = request.json
    else:
        dados = request.form

    nome = dados.get('nome')
    senha = dados.get('senha')
    adm = dados.get('adm', False)

    if not nome or not senha:
        return jsonify({"erro": "Nome e senha são obrigatórios!"}), 400

    inserir_usuario(nome, senha, adm)
    return redirect(url_for('login_routes.listar_usuarios'))

# Rota para listar todos os usuários (HTML)
@login_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login'))

    usuarios = consultar_usuarios()  # Obtém a lista de usuários do banco de dados
    return render_template('lista_usuarios.html', usuarios=usuarios)


# Rota para consultar um usuário pelo ID (JSON)
@login_bp.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login'))

    usuario = consultar_usuario_por_id(id)
    if usuario:
        return jsonify(usuario), 200
    else:
        return jsonify({"erro": f"Usuário com ID {id} não encontrado."}), 404

# Rota para atualizar um usuário (JSON)
@login_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario_route(id):
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login'))

    dados = request.json
    novo_nome = dados.get('nome')
    nova_senha = dados.get('senha')
    novo_adm = dados.get('adm')

    if not novo_nome and not nova_senha and novo_adm is None:
        return jsonify({"erro": "Nenhum dado fornecido para atualização."}), 400

    atualizar_usuario(id, novo_nome, nova_senha, novo_adm)
    return jsonify({"mensagem": f"Usuário com ID {id} atualizado com sucesso!"}), 200

# Rota para deletar um usuário (JSON)
@login_bp.route('/usuarios/excluir/<int:id>', methods=['POST'])
def deletar_usuario_route(id):
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login'))

    deletar_usuario(id)  # Chama a função para deletar o usuário
    return redirect(url_for('login_routes.listar_usuarios'))  # Redireciona para a lista de usuários


# Rota para verificar login
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Renderiza a página de login (GET)
        return render_template('login.html')  # Certifique-se de que o caminho está correto
    elif request.method == 'POST':
        # Lógica para processar o login
        if request.is_json:
            dados = request.json
        else:
            dados = request.form

        nome = dados.get('nome')
        senha = dados.get('senha')

        if not nome or not senha:
            return jsonify({"erro": "Nome e senha são obrigatórios!"}), 400

        try:
            usuario = verificar_login(nome, senha)
            if usuario:
                # Armazenar informações do usuário na sessão
                session['usuario'] = usuario  # Armazenando o nome ou id do usuário, dependendo da necessidade
                return redirect(url_for('login_routes.menu'))
            else:
                return jsonify({"erro": "Nome de usuário ou senha incorretos."}), 401
        except Exception as e:
            return jsonify({"erro": str(e)}), 500

# Rota para o menu principal
@login_bp.route('/menu', methods=['GET'])
def menu():
    if 'usuario' not in session:  # Verifica se o usuário está autenticado na sessão
     return redirect(url_for('/login'))

    usuario = session['usuario']  # Recupera os dados do usuário na sessão
    is_admin = bool(usuario[3])  # Verifica se o usuário é administrador
    return render_template('menu_principal.html', show_admin=is_admin)




# Rota para editar um usuário (HTML)
@login_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login'))

    if request.method == 'GET':
        # Busca o usuário pelo ID
        usuario = consultar_usuario_por_id(id)
        if usuario:
            return render_template('editar_usuario.html', usuario=usuario)
        else:
            return jsonify({"erro": f"Usuário com ID {id} não encontrado."}), 404
    elif request.method == 'POST':
        # Atualiza o usuário
        dados = request.form
        novo_nome = dados.get('nome')
        nova_senha = dados.get('senha')
        novo_adm = dados.get('adm', False)

        atualizar_usuario(id, novo_nome, nova_senha, novo_adm)
        return redirect(url_for('login_routes.listar_usuarios'))

@login_bp .route("/usuariosadmin")
def listaradmin():
    return render_template("lista_usuarios.html")
