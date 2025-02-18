from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from configDB.Funcoes_placaTask import ( inserir_relacao_placa_task, consultar_relacoes_placa_task,
    atualizar_placa_task, deletar_relacao_placa_task, consultar_relacao_placa_task_por_id
)
import os
import json
import importlib.util
# Cria uma instância do Blueprint
placa_task_bp = Blueprint('placa_task_routes', __name__)

# Rota para listar todas as relações Placa-Task
@placa_task_bp.route('/placa-task', methods=['GET'])
def listar_placa_task():
    relacoes = consultar_relacoes_placa_task()
    return render_template('lista_placa_task.html', relacoes=relacoes)

# Rota para adicionar uma nova relação Placa-Task
@placa_task_bp.route('/placa-task/adicionar', methods=['GET', 'POST'])
def adicionar_placa_task():
    if request.method == 'POST':
        nome = request.form.get('nome')
        placa = request.form.get('placa')
        id_task = request.form.get('id_task')
        inserir_relacao_placa_task(nome, placa, id_task)
        return redirect(url_for('placa_task_routes.listar_placa_task'))
    return render_template('adicionar_placa_task.html')

# Rota para editar uma relação Placa-Task
@placa_task_bp.route('/placa-task/editar/<int:id>', methods=['GET', 'POST'])
def editar_placa_task(id):
    relacao = consultar_relacao_placa_task_por_id(id)
    if not relacao:
        return jsonify({"erro": f"Relação com ID {id} não encontrada."}), 404

    if request.method == 'POST':
        novo_nome = request.form.get('nome')
        nova_placa = request.form.get('placa')
        novo_id_task = request.form.get('id_task')
        atualizar_placa_task(id, novo_nome, nova_placa, novo_id_task)
        return redirect(url_for('placa_task_routes.listar_placa_task'))
    return render_template('editar_placa_task.html', relacao=relacao)

# Rota para deletar uma relação Placa-Task
@placa_task_bp.route('/placa-task/deletar/<int:id>', methods=['POST'])
def deletar_placa_task(id):
    deletar_relacao_placa_task(id)
    return redirect(url_for('placa_task_routes.listar_placa_task'))






# Caminho para o arquivo de configurações (agora usando JSON)
CONFIG_FILE = "variaveis_da_api.py"

    # Função para carregar as configurações salvas
def carregar_configuracoes():
    """Carrega as configurações do arquivo Python como módulo"""
    if os.path.exists(CONFIG_FILE):
        spec = importlib.util.spec_from_file_location("config_module", CONFIG_FILE)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)

        return {
            "bitrix_domain": getattr(config_module, "bitrix_domain", ""),
            "bitrix_user_id": getattr(config_module, "bitrix_user_id", ""),
            "bitrix_token": getattr(config_module, "bitrix_token", ""),
            "folder_id": getattr(config_module, "folder_id", ""),
        }
    return {}

    # Função para salvar as configurações
def salvar_configuracoes(config):
    """Salva as configurações dentro do arquivo variaveis_da_api.py"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(f'bitrix_domain = "{config["bitrix_domain"]}"\n')
        f.write(f'bitrix_user_id = "{config["bitrix_user_id"]}"\n')
        f.write(f'bitrix_token = "{config["bitrix_token"]}"\n')
        f.write(f'folder_id = "{config["folder_id"]}"\n')

    # Rota para exibir o formulário de configurações
@placa_task_bp.route("/config", methods=["GET"])
def config():
    
    return render_template("ConfiguracoesdaAPI.html")


    # Rota para processar o envio do formulário
@placa_task_bp.route("/config/salvar", methods=["POST"])
def salvar_config():
    # Captura os dados do formulário
    bitrix_domain = request.form.get("bitrix_domain")
    bitrix_user_id = request.form.get("bitrix_user_id")
    bitrix_token = request.form.get("bitrix_token")
    folder_id = request.form.get("folder_id")
    autor = request.form.get("autor")

    # Valida se todos os campos foram preenchidos
    if not all([bitrix_domain, bitrix_user_id, bitrix_token, folder_id, autor]):
        return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

    # Salva as configurações no arquivo
    config = {
        "bitrix_domain": bitrix_domain,
        "bitrix_user_id": bitrix_user_id,
        "bitrix_token": bitrix_token,
        "folder_id": folder_id,
        "autor": autor
    }

    salvar_configuracoes(config)

    print("Configuração salva em variaveis_da_api.py!")

    # Retorna para a página de configurações sem precisar recarregar
    return redirect(url_for("placa_task_bp.config"))

