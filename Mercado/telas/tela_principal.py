import tkinter as tk
from tkinter import ttk
from data.context.postgre_sql_context import Postgre_Sql_Context


class TelaPrincipal():
    def __init__(self, win):
        self.win = win

        # Componentes
        self.lbCodigo = tk.Label(win, text='Código do produto:')
        self.lblNome = tk.Label(win, text='Nome do produto:')
        self.lblPreco = tk.Label(win, text='Preço:')

        self.textCodigo = tk.Entry(bd=3)
        self.txtNome = tk.Entry()
        self.txtPreco = tk.Entry()

        self.btnCadastrar = tk.Button(win, text='Cadastrar', command=self.fCadastrarProduto)
        self.btnAtualizar = tk.Button(win, text='Atualizar')
        self.btnExcluir = tk.Button(win, text='Excluir')
        self.btnLimpar = tk.Button(win, text='Limpar', command=self.fLimparTela)
        self.btnListaProdutos = tk.Button(win, text='Lista de Produtos', command=self.ListaProdutos)

        # Posicionamento dos Componentes
        self.lbCodigo.place(x=100, y=50)
        self.textCodigo.place(x=250, y=50)
        self.lblNome.place(x=100, y=100)
        self.txtNome.place(x=250, y=100)
        self.lblPreco.place(x=100, y=150)
        self.txtPreco.place(x=250, y=150)
        self.btnCadastrar.place(x=100, y=200)
        self.btnAtualizar.place(x=200, y=200)
        self.btnExcluir.place(x=300, y=200)
        self.btnLimpar.place(x=400, y=200)
        self.btnListaProdutos.place(x=100, y=250)

        # Inicia a conexão com o banco de dados
        self.db_pg_context = Postgre_Sql_Context()

    def fCadastrarProduto(self):
        try:
            codigo, nome, preco = self.fLerCampos()
            self.inserirDados(codigo, nome, preco)
            self.fLimparTela()
            print('Produto Cadastrado com Sucesso!')
        except Exception as e:
            print('Não foi possível fazer o cadastro.', e)

    def inserirDados(self, codigo, nome, preco):
        try:
            query = f"INSERT INTO public.produtos (nome, codigo, preco) VALUES ('{nome}', '{codigo}', '{preco}')"
            self.db_pg_context.conectar()
            self.db_pg_context.executar_update_sql(query)
            self.db_pg_context.desconectar()
        except Exception as e:
            print('Não foi possível fazer o cadastro.', e)

    def fLimparTela(self):
        try:
            self.textCodigo.delete(0, tk.END)
            self.txtNome.delete(0, tk.END)
            self.txtPreco.delete(0, tk.END)
            print('Campos Limpos!')
        except Exception as e:
            print('Não foi possível limpar os campos.', e)

    def fLerCampos(self):
        try:
            codigo = self.textCodigo.get()
            nome = self.txtNome.get()
            preco = self.txtPreco.get()
            print('Leitura dos dados com Sucesso!')
            return codigo, nome, preco
        except Exception as e:
            print('Não foi possível ler os dados.', e)
            return None, None, None

    def ListaProdutos(self):
        self.win.withdraw()
        lista_produtos = TelaSelecao(self.win)
        lista_produtos.mainloop()


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


if __name__ == "__main__":
    root = tk.Tk()
    app = TelaPrincipal(root)
    root.title("Cadastro de Produtos")
    root.geometry("600x400")
    root.mainloop()
