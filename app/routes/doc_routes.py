from flask import Blueprint,render_template,request,session,jsonify,current_app,send_from_directory,url_for,redirect
from datetime import datetime
from flask import current_app as app
import os
from werkzeug.utils import secure_filename
import requests
from variaveis_da_api import bitrix_domain, bitrix_user_id, bitrix_token, folder_id, autor
import sqlite3

doc_bp  = Blueprint('doc_routes', __name__)



####################### FUNCOES DE ENVIAR AQUIVO ############################
def coleta_texto(placa, km, data, hora, motorista, descricao):
    COMMENT_TEXT = f"""
    Motorista: {motorista}
    Data: {data}
    Hora: {hora}
    Placa: {placa}
    KM: {km}
    Descrição: {descricao}
    """
    return COMMENT_TEXT
# Função para enviar os arquivos para o Bitrix24
def enviar_todos_arquivos_para_bitrix(pasta="uploads"):
    extensoes_validas = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.mov', '.avi', '.mkv']
    media_ids = []

    for arquivo in os.listdir(pasta):
        if any(arquivo.endswith(ext) for ext in extensoes_validas):
            caminho_arquivo = os.path.join(pasta, arquivo)

            # Passo 1: Obter a URL de upload
            url_obter_url = f"https://{bitrix_domain}/rest/{bitrix_user_id}/{bitrix_token}/disk.folder.uploadfile"
            response = requests.post(url_obter_url, data={"id": folder_id})

            if response.status_code == 200 and "result" in response.json():
                upload_url = response.json()["result"].get("uploadUrl")
                
                if not upload_url:
                    print(f"Erro ao obter URL de upload para {arquivo}")
                    continue
                
                # Passo 2: Enviar o arquivo para a URL recebida
                with open(caminho_arquivo, "rb") as file:
                    files = {"file": (arquivo, file)}
                    response_upload = requests.post(upload_url, files=files)

                if response_upload.status_code == 200 and "result" in response_upload.json():
                    media_id = response_upload.json()["result"].get("ID")
                    if media_id:
                        media_ids.append(f'n{media_id}')  # Adicionando prefixo 'n' ao ID do arquivo
                        print(f"Arquivo {arquivo} enviado com sucesso! ID: {media_id}")
                    else:
                        print(f"Erro ao obter ID do arquivo {arquivo}: {response_upload.json()}")
                else:
                    print(f"Erro no upload de {arquivo}: {response_upload.status_code}, {response_upload.text}")
            else:
                print(f"Erro ao obter URL de upload para {arquivo}: {response.status_code}, {response.text}")

    return media_ids

def salvar_arquivos(files, upload_folder):
    """Função para salvar arquivos enviados no formulário"""
    
    # Definir as extensões permitidas dentro da função
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'pdf'}
    
    # Função para verificar se o arquivo tem uma extensão permitida
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    saved_files = []
    
    # Garantir que o diretório de upload exista
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    for file in files:
        if file.filename != '':  # Verificar se o arquivo tem nome
            # Gerar um nome de arquivo seguro
            filename = secure_filename(file.filename)
            
            # Verificar a extensão do arquivo
            if allowed_file(filename):  # Se a extensão for permitida
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)  # Salvar o arquivo
                saved_files.append(filepath)  # Adicionar ao registro dos arquivos salvos
            else:
                # Se o arquivo não for permitido, gerar um erro
                raise ValueError(f"Arquivo {filename} não permitido!")
    
    return saved_files

def adicionar_comentario_bitrix(texto, ids_arquivos,IDTASK):
    COMMENT_TEXT = texto
    # URL para adicionar o comentário
    url = f"https://{bitrix_domain}/rest/{bitrix_user_id}/{bitrix_token}/task.commentitem.add.json"
    payload = {
        "TASKID": IDTASK,
        "FIELDS": {
            "POST_MESSAGE": COMMENT_TEXT,
            "AUTHOR_ID": bitrix_user_id,  # ID do autor do comentário (verifique o ID correto)
            "UF_FORUM_MESSAGE_DOC": ids_arquivos  # Lista de IDs dos arquivos para anexar
        }
    }

    # Faz a requisição para adicionar o comentário
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        resposta_json = response.json()
        if 'result' in resposta_json:
            print(f"Comentário adicionado com sucesso! ID: {resposta_json['result']}")
        else:
            print(f"Erro ao adicionar comentário: {resposta_json}")
    else:
        print(f"Erro na requisição: {response.status_code}, {response.text}")

# Chama a função para adicionar o comentário com os arquivos


####################### FIM DAS FUNCOES DE ENVIAR AQUIVO ############################






@doc_bp .route('/enviarArquivosDoMotorista', methods=['POST'])
def enviar_arquivos(): 
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login')) 
 





    try:
        placa = request.form.get('placa')
        km = request.form.get('km')
        descricao = request.form.get('descricao')
        IDTASK = request.form.get('id_task')
        motorista = session['usuario'][1]

        agora = datetime.now()
        data = agora.strftime("%Y-%m-%d")
        hora = agora.strftime("%H:%M")

        if not all([placa, km, descricao]):
            return jsonify({'error': 'Preencha todos os campos obrigatórios!'}), 400

        text = coleta_texto(placa, km, data, hora, motorista, descricao)
        arquivos = request.files.getlist('midia[]')
        print(text)


        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
          os.makedirs(current_app.config['UPLOAD_FOLDER'])

        
        for arquivo in os.listdir(current_app.config['UPLOAD_FOLDER']):
            caminho_arquivo = os.path.join(current_app.config['UPLOAD_FOLDER'], arquivo)
            if os.path.isfile(caminho_arquivo):
                os.remove(caminho_arquivo)
        
        salvar_arquivos(arquivos, current_app.config['UPLOAD_FOLDER'])
        ids_arquivos = enviar_todos_arquivos_para_bitrix()
        adicionar_comentario_bitrix(text, ids_arquivos, IDTASK)
        
        
    
        #media_files = os.listdir(app.config['UPLOAD_FOLDER'])
        
    
        return render_template('Lista_de_arquivos_enviados.html', placa=placa, km=km, data=data, hora=hora, motorista=motorista, descricao=descricao, IDTASK=IDTASK)
    
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar a requisição: aqui MERDA{str(e)}"}), 500
    








    
@doc_bp .route("/listar-veiculos", methods=["GET"])
def listar_veiculos():
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login')) 

    conn = None
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect("PlacaTask.db")
        cursor = conn.cursor()

        # Executa a consulta
        cursor.execute("SELECT Name, Placa, IdTask FROM PlacaTask")
        veiculos = cursor.fetchall()

        # Formata os resultados
        lista_veiculos = [{"nome": v[0], "placa": v[1], "id_task": v[2]} for v in veiculos]

        # Retorna os dados em formato JSON
        return jsonify(lista_veiculos), 200

    except Exception as e:
        # Log do erro (opcional)
        current_app.logger.error(f"Erro ao buscar veículos: {str(e)}")

        # Retorna uma mensagem de erro
        return jsonify({"erro": f"Erro ao buscar veículos: {str(e)}"}), 500

    finally:
        # Fecha a conexão com o banco de dados
        if conn:
            conn.close()


@doc_bp .route("/documentar-veiculo")
def documentar_veiculo():
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login')) 
    return render_template("Formulario_Upload.html")

@doc_bp .route('/uploads/<filename>')
def uploaded_file(filename):
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login')) 
    
    UPLOADS_FOLDER = os.path.join(os.getcwd(), 'uploads')
    app.config['UPLOAD_FOLDER'] = 'uploads'
    return send_from_directory(UPLOADS_FOLDER, filename)


@doc_bp .route('/listar_pastas')
def listar_pastas():
    if 'usuario' not in session:  # Verifica se o usuário está autenticado
        return redirect(url_for('login_routes.login')) 
    """Rota para buscar as pastas do Bitrix e retornar como JSON."""
    url = f"https://{bitrix_domain}/rest/{bitrix_user_id}/{bitrix_token}/disk.storage.getchildren?id=1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        pastas = response.json().get('result', [])

        return jsonify(pastas)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
