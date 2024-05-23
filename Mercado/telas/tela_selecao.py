import tkinter as tk
from tkinter import ttk
from data.context.postgre_sql_context import Postgre_Sql_Context


class TelaSelecao(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Lista de Produtos")
        self.geometry("600x500")

        # Exemplo de componente da tela de seleção
        self.label = ttk.Label(self, text="Lista de Produtos Cadastrados")
        self.label.place(x=20, y=10)

        self.back_button = ttk.Button(self, text="Voltar para a Tela Principal", command=self.voltarTelaPrincipal)
        self.back_button.pack(pady=20)

        # Exemplo de dados (substituir por dados reais do banco de dados)
        self.dados = []

        # Criar Treeview
        self.tree = ttk.Treeview(self, columns=("ID", "Codigo", "Nome", "Preco"), show='headings')
        self.tree.heading('ID', text="ID")
        self.tree.heading("Codigo", text="Codigo")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Preco", text="Preço")

        # Definir largura das colunas
        self.tree.column("ID", width=50)
        self.tree.column("Codigo", width=100)
        self.tree.column("Nome", width=200)
        self.tree.column("Preco", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Executa a conexão com o banco de dados
        self.db_pg_context = Postgre_Sql_Context()

        # Executa a obtenção dos dados para inserir na tabela
        self.obterDados()

    def obterDados(self):
        try:
            query = "SELECT id, codigo, nome, preco FROM public.produtos"
            self.db_pg_context.conectar()
            result = self.db_pg_context.executar_query_sql(query)
            self.db_pg_context.desconectar()

            self.dados = [{"id": row[0], "codigo": row[1], "nome": row[2], "preco": row[3]} for row in result]
            self.inserirDadosTabela()

        except Exception as e:
            print('Não foi possível obter os dados', e)

    def inserirDadosTabela(self):
        # Inserir dados no Treeview
        for produto in self.dados:
            self.tree.insert("", "end", values=(produto["id"], produto["codigo"], produto["nome"], produto["preco"]))

    def voltarTelaPrincipal(self):
        self.destroy()
        self.master.deiconify()
