import tkinter as tk
from tkinter import ttk, messagebox
from data.context.postgre_sql_context import Postgre_Sql_Context
from telas.tela_selecao import TelaSelecao

class TelaPrincipal:
    def __init__(self, win):
        self.win = win

        # Componentes
        self.lbAluno = tk.Label(win, text='Nome do Aluno:')
        self.lblDisciplina = tk.Label(win, text='Disciplina:')
        self.lblNota = tk.Label(win, text='Nota:')

        self.txtAluno = tk.Entry(bd=3)
        self.txtDisciplina = tk.Entry(bd=3)
        self.txtNota = tk.Entry(bd=3)

        self.btnCadastrar = tk.Button(win, text='\n    Cadastrar    \n', command=self.fCadastrarNota)
        self.btnAtualizar = tk.Button(win, text='\n    Atualizar    \n', command=self.fAtualizarNota)
        self.btnExcluir = tk.Button(win, text='\n      Excluir      \n', command=self.fExcluirNota)
        self.btnLimpar = tk.Button(win, text='\n\n     Limpar     \n\n     Campos     \n\n', command=self.fLimparTela)
        self.btnListaNotas = tk.Button(win, text='\n           Lista de Notas           \n', command=self.ListaNotasbtnListaNotas)
        self.btnListaCR = tk.Button(win, text='\n               Lista de  CR               \n', command=self.fListaCR)

        # Posicionamento dos Componentes
        self.lbAluno.place(x=70, y=50)
        self.txtAluno.place(x=200, y=50)
        self.lblDisciplina.place(x=70, y=100)
        self.txtDisciplina.place(x=200, y=100)
        self.lblNota.place(x=70, y=150)
        self.txtNota.place(x=200, y=150)
        self.btnCadastrar.place(x=70, y=200)
        self.btnAtualizar.place(x=215, y=200)
        self.btnExcluir.place(x=350, y=200)
        self.btnLimpar.place(x=350, y=53)
        self.btnListaNotas.place(x=70, y=300)
        self.btnListaCR.place(x=280, y=300)

        # Inicia a conexão com o banco de dados
        self.db_pg_context = Postgre_Sql_Context()

    def fListaCR(self):
        try:
            self.db_pg_context.conectar()
            query_lista_cr = """
                SELECT a.nome AS aluno, AVG(n.nota) AS cr
                FROM public.notas n
                JOIN public.alunos a ON n.aluno_id = a.id
                GROUP BY a.nome
                ORDER BY cr DESC;
            """
            resultados = self.db_pg_context.executar_query_sql(query_lista_cr)
            self.db_pg_context.desconectar()

            self.mostrarResultadosCR(resultados)
        except Exception as e:
            print('Não foi possível listar o CR.', e)

    def mostrarResultadosCR(self, resultados):
        top = tk.Toplevel(self.win)
        top.title("Coeficiente de Rendimento (CR) dos Alunos")

        tree = ttk.Treeview(top, columns=('Aluno', 'CR'), show='headings')
        tree.heading('Aluno', text='Aluno')
        tree.heading('CR', text='CR')

        for resultado in resultados:
            tree.insert('', tk.END, values=(resultado[0], round(resultado[1], 2)))

        tree.pack(expand=True, fill='both')
        top.geometry("500x500")

    def fCadastrarNota(self):
        try:
            aluno, disciplina, nota = self.fLerCampos()
            if self.verificarExistenciaNota(aluno, disciplina):
                messagebox.showwarning("Erro", "A nota para essa disciplina já foi cadastrada para esse aluno.")
                return
            self.inserirDados(aluno, disciplina, nota)
            self.fLimparTela()
            print('Nota Cadastrada com Sucesso!')
        except Exception as e:
            print('Não foi possível fazer o cadastro.', e)

    def verificarExistenciaNota(self, aluno, disciplina):
        try:
            query_verificar_existencia = f"""
                SELECT 1
                FROM public.notas n
                JOIN public.alunos a ON n.aluno_id = a.id
                JOIN public.disciplinas d ON n.disciplina_id = d.id
                WHERE a.nome = '{aluno}' AND d.nome = '{disciplina}'
            """
            self.db_pg_context.conectar()
            resultado = self.db_pg_context.executar_query_sql(query_verificar_existencia)
            self.db_pg_context.desconectar()
            return bool(resultado)
        except Exception as e:
            print('Não foi possível verificar a existência da nota.', e)
            return False

    def inserirDados(self, aluno, disciplina, nota):
        try:
            # Verifica se o aluno já existe
            query_verificar_aluno = f"SELECT id FROM public.Alunos WHERE nome = '{aluno}'"
            self.db_pg_context.conectar()
            aluno_id = self.db_pg_context.executar_query_sql(query_verificar_aluno)
            if not aluno_id:
                # Se o aluno não existe, insere-o
                query_inserir_aluno = f"INSERT INTO public.Alunos (nome) VALUES ('{aluno}') RETURNING id"
                aluno_id = self.db_pg_context.executar_query_sql(query_inserir_aluno)[0][0]
            else:
                aluno_id = aluno_id[0][0]

            # Verifica se a disciplina já existe
            query_verificar_disciplina = f"SELECT id FROM public.Disciplinas WHERE nome = '{disciplina}'"
            disciplina_id = self.db_pg_context.executar_query_sql(query_verificar_disciplina)
            if not disciplina_id:
                # Se a disciplina não existe, insere-a
                query_inserir_disciplina = f"INSERT INTO public.Disciplinas (nome) VALUES ('{disciplina}') RETURNING id"
                disciplina_id = self.db_pg_context.executar_query_sql(query_inserir_disciplina)[0][0]
            else:
                disciplina_id = disciplina_id[0][0]

            # Insere a nota
            query_inserir_nota = f"INSERT INTO public.Notas (aluno_id, disciplina_id, nota) VALUES ('{aluno_id}', '{disciplina_id}', '{nota}')"
            self.db_pg_context.executar_update_sql(query_inserir_nota)
            self.db_pg_context.desconectar()
        except Exception as e:
            print('Não foi possível fazer o cadastro.', e)

    def fAtualizarNota(self):
        try:
            aluno, disciplina, nota = self.fLerCampos()
            self.atualizarDados(aluno, disciplina, nota)
            self.fLimparTela()
            print('Nota Atualizada com Sucesso!')
        except Exception as e:
            print('Não foi possível atualizar a nota.', e)

    def atualizarDados(self, aluno, disciplina, nota):
        try:
            query = f"""
                UPDATE Notas
                SET nota = '{nota}'
                WHERE aluno_id = (SELECT id FROM Alunos WHERE nome = '{aluno}')
                AND disciplina_id = (SELECT id FROM Disciplinas WHERE nome = '{disciplina}')
            """
            self.db_pg_context.conectar()
            self.db_pg_context.executar_update_sql(query)
            self.db_pg_context.desconectar()
        except Exception as e:
            print('Não foi possível atualizar a nota.', e)

    def fExcluirNota(self):
        try:
            aluno = self.txtAluno.get()
            disciplina = self.txtDisciplina.get()
            self.excluirDados(aluno, disciplina)
            self.fLimparTela()
            print('Nota Excluída com Sucesso!')
        except Exception as e:
            print('Não foi possível excluir a nota.', e)

    def excluirDados(self, aluno, disciplina):
        try:
            query = f"""
                DELETE FROM Notas
                WHERE aluno_id = (SELECT id FROM Alunos WHERE nome = '{aluno}')
                AND disciplina_id = (SELECT id FROM Disciplinas WHERE nome = '{disciplina}')
            """
            self.db_pg_context.conectar()
            self.db_pg_context.executar_update_sql(query)
            self.db_pg_context.desconectar()
        except Exception as e:
            print('Não foi possível excluir a nota.', e)

    def fLimparTela(self):
        try:
            self.txtAluno.delete(0, tk.END)
            self.txtDisciplina.delete(0, tk.END)
            self.txtNota.delete(0, tk.END)
            print('Campos Limpos!')
        except Exception as e:
            print('Não foi possível limpar os campos.', e)

    def fLerCampos(self):
        try:
            aluno = self.txtAluno.get()
            disciplina = self.txtDisciplina.get()
            nota = self.txtNota.get()
            print('Leitura dos dados com Sucesso!')
            return aluno, disciplina, nota
        except Exception as e:
            print('Não foi possível ler os dados.', e)
            return "", "", ""

    def ListaNotasbtnListaNotas(self):
        self.win.withdraw()
        lista_notas = TelaSelecao(self.win)
        lista_notas.mainloop()


# Criação da janela principal e inicialização do aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = TelaPrincipal(root)
    root.title("Sistema de Notas")
    root.geometry("500x500")
    root.mainloop()
