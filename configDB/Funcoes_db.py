import sqlite3
import hashlib

# Função para hashear a senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Conectar ao banco de dados
def conectar_banco():
    conn = sqlite3.connect('usuarios.db')
    return conn

# Função para criar a tabela de usuários (se não existir)
def criar_tabela_usuarios():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL,
        adm BOOLEAN NOT NULL DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()

# Função para inserir um novo usuário
def inserir_usuario(nome, senha, adm=False):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO usuarios (nome, senha, adm)
    VALUES (?, ?, ?)
    ''', (nome, senha, adm))
    conn.commit()
    conn.close()
    print(f"Usuário '{nome}' inserido com sucesso!")

# Função para consultar todos os usuários
def consultar_usuarios():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    print(usuarios)
    return usuarios

# Função para consultar um usuário pelo ID
def consultar_usuario_por_id(id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

# Função para atualizar um usuário
def atualizar_usuario(id, novo_nome=None, nova_senha=None, novo_adm=None):
    conn = conectar_banco()
    cursor = conn.cursor()
    if novo_nome:
        cursor.execute('UPDATE usuarios SET nome = ? WHERE id = ?', (novo_nome, id))
    if nova_senha:
        
        cursor.execute('UPDATE usuarios SET senha = ? WHERE id = ?', (nova_senha, id))
    if novo_adm is not None:
        cursor.execute('UPDATE usuarios SET adm = ? WHERE id = ?', (novo_adm, id))
    conn.commit()
    conn.close()
    print(f"Usuário com ID {id} atualizado com sucesso!")

# Função para deletar um usuário
def deletar_usuario(id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print(f"Usuário com ID {id} deletado com sucesso!")

# Função para verificar credenciais de login
def verificar_login(nome, senha):
    conn = conectar_banco()
    cursor = conn.cursor()
    senha_hash = senha
    cursor.execute('SELECT * FROM usuarios WHERE nome = ? AND senha = ?', (nome, senha_hash))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

 


consultar_usuarios()