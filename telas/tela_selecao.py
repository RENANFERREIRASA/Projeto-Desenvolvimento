import tkinter as tk
from tkinter import ttk
from data.context.postgre_sql_context import Postgre_Sql_Context


class TelaSelecao(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Lista de Notas")
        self.geometry("600x500")

        # Exemplo de componente da tela de seleção
        self.label = ttk.Label(self, text="Lista de Notas Cadastradas")
        self.label.place(x=20, y=10)

        self.back_button = ttk.Button(self, text="Voltar para a Tela Principal", command=self.voltarTelaPrincipal)
        self.back_button.pack(pady=20)

        # Exemplo de dados (substituir por dados reais do banco de dados)
        self.dados = []

        # Criar Treeview
        self.tree = ttk.Treeview(self, columns=("Aluno", "Disciplina", "Nota"), show='headings')
        self.tree.heading('Aluno', text="Aluno")
        self.tree.heading("Disciplina", text="Disciplina")
        self.tree.heading("Nota", text="Nota")

        # Definir largura das colunas
        self.tree.column("Aluno", width=200)
        self.tree.column("Disciplina", width=200)
        self.tree.column("Nota", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Executa a conexão com o banco de dados
        self.db_pg_context = Postgre_Sql_Context()

        # Executa a obtenção dos dados para inserir na tabela
        self.obterDados()

    def obterDados(self):
        try:
            query = """
            SELECT DISTINCT Alunos.nome, Disciplinas.nome, Notas.nota
            FROM Alunos
            INNER JOIN Notas ON Alunos.id = Notas.aluno_id
            INNER JOIN Disciplinas ON Disciplinas.id = Notas.disciplina_id
            """
            self.db_pg_context.conectar()
            result = self.db_pg_context.executar_query_sql(query)
            self.db_pg_context.desconectar()

            self.dados = result
            self.inserirDadosTabela()

        except Exception as e:
            print('Não foi possível obter os dados', e)

    def inserirDadosTabela(self):
        # Inserir dados no Treeview
        for aluno, disciplina, nota in self.dados:
            self.tree.insert("", "end", values=(aluno, disciplina, nota))

    def voltarTelaPrincipal(self):
        self.destroy()
        self.master.deiconify()
