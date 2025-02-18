from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from configDB.Funcoes_placaTask import ( inserir_relacao_placa_task, consultar_relacoes_placa_task,
    atualizar_placa_task, deletar_relacao_placa_task, consultar_relacao_placa_task_por_id
)

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

