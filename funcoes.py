import sqlite3
import os


class Banco():
    def __init__(self):
        self.connect = sqlite3.connect("tarefas.db")
        self.cursor = self.connect.cursor()
        self.criar_tabela()


    def criar_tabela(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS grupo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT NOT NULL
                );
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tarefa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT NOT NULL,
                    status TEXT NOT NULL,
                    prioridade TEXT NOT NULL,
                    prazo DATE NOT NULL,
                    data_atual TIMESTAMP NOT NULL DEFAULT (DATETIME('now', '-3 hours')),
                    grupo INTEGER,
                    FOREIGN KEY (grupo) REFERENCES grupo(id)
                );
            """)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pomodoro (
                    id INTEGER
                )
                ''')
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            self.connect.commit()
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")

    

    def cadastrar(self, descricao, prioridade, prazo, grupo):
        try:
            self.cursor.execute(f"""
            INSERT INTO tarefa(
                descricao, status, prioridade, prazo, grupo)
            VALUES ('{descricao}', 'Pendente', '{prioridade}', '{prazo}', {grupo});
            """)
            self.connect.commit()
            print(f"Tarefa {descricao} cadastrada com sucesso")
        except Exception as e:
            print(f"Ocorreu um erro ao salvar a tarefa {descricao} erro: {e}")

    def pomodoro(self, id):
        try:
            self.cursor.execute('UPDATE pomodoro SET linha = ? where id = 1', (id,))
            self.connect.commit()
        except Exception as e:
            print(e)
    
    def busca_id(self):
        try:
            busca = self.cursor.execute("SELECT linha from pomodoro")
            resultado = busca.fetchall()
            return resultado[0][0]
        except Exception as e:
            print(e)

    def cadastra_grupo(self, descricao):
        try:
            self.cursor.execute(f"""
            INSERT INTO grupo(
                descricao)
            VALUES ('{descricao}');
            """)
            self.connect.commit()
            print(f"Tarefa {descricao} cadastrada com sucesso")
        except Exception as e:
            print(f"Ocorreu um erro ao salvar o grupo {descricao} erro: {e}")

    def buscar_grupo(self):
        busca = self.cursor.execute(f"""
            select descricao from grupo order by id
            """)
        resultado = busca.fetchall()
        lista = []
        for grupo in resultado:
            lista.append(grupo[0])
        return lista

    def buscar(self):
        busca = self.cursor.execute(f"""
            SELECT tarefa.id, tarefa.descricao, tarefa.status, tarefa.prioridade, tarefa.prazo, grupo.descricao 
            FROM tarefa, grupo 
            WHERE tarefa.grupo = grupo.id;
            """)
        resultado = busca.fetchall()
        tarefas = []
        for tarefa in resultado:
            tarefas.append(list(tarefa))
        return tarefas


    def apagar(self, id):
        try:
            self.cursor.execute(f"DELETE FROM tarefa WHERE id = {id}")
            self.connect.commit()
        except Exception as e:
            print(f"ocorreu um erro ao excluir o aluno erro: {e}")

    def editar(self,id):                
        try:
            self.cursor.execute(f"UPDATE tarefa SET status = 'Concluido' WHERE id = {id}")
            self.connect.commit()
        except Exception as e:
            print(f"ocorreu um erro ao editar status erro: {e}")