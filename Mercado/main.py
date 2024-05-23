import tkinter as tk
from tkinter import ttk

from telas.tela_principal import TelaPrincipal

janela = tk.Tk()

principal = TelaPrincipal(janela)

janela.title('Bem Vindo a Tela de Cadastro')
janela.geometry("600x500")
janela.mainloop()