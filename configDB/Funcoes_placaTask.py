import sqlite3
import hashlib


def conectar_banco():
    conn = sqlite3.connect('PlacaTask.db')
    return conn

def criar_relacao_placa_task():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PlacaTask (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,           
        Placa TEXT NOT NULL,
        IdTask INTEGER NOT NULL
                   
        
    )
    ''')
    conn.commit()
    conn.close()

 
def inserir_relacao_placa_task(Name,Placa, IdTask):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO PlacaTask (Name, Placa, idTask)
    VALUES (?, ?, ?)
    ''', (Name, Placa, IdTask))
    conn.commit()
    conn.close()
    print(f"O Veiculo:'{Name}' da Placa:'{Placa}'foi relacionada com a Task:'{IdTask}' com sucesso!")   

def consultar_relacoes_placa_task():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PlacaTask')
    PlacaTask = cursor.fetchall()
    conn.close()
    print(PlacaTask)
    return PlacaTask  


def atualizar_placa_task(id, novo_nome=None, nova_placa=None, novo_IdTask=None):
    conn = conectar_banco()
    cursor = conn.cursor()
    if novo_nome:
        cursor.execute('UPDATE PlacaTask SET Name = ? WHERE id = ?', (novo_nome, id))
    if nova_placa:
        cursor.execute('UPDATE PlacaTask SET Placa = ? WHERE id = ?', (nova_placa, id))
    if novo_IdTask is not None:
        cursor.execute('UPDATE PlacaTask SET IdTask = ? WHERE id = ?', (novo_IdTask, id))
    conn.commit()
    conn.close()
    print(f"O veiculo do id; {id} foi atualizado com sucesso!")


def deletar_relacao_placa_task(id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM PlacaTask WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    print(f"Relação com ID {id} foi deletada com sucesso!")

def consultar_relacao_placa_task_por_id(id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PlacaTask WHERE id = ?', (id,))
    relacao = cursor.fetchone()
    conn.close()
    return relacao