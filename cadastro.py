import customtkinter as ctk
from tkinter import messagebox
from funcoes import Banco
from datetime import datetime
from tkcalendar import DateEntry

class Cadastro(ctk.CTkFrame):
	def __init__(self, janela, controller):
		super().__init__(janela)
		
		frame_descricao = ctk.CTkFrame(self)
		frame_descricao.pack(expand=True, side="top", anchor="n", fill="x", padx = 5, pady=5)
		frame_descricao.columnconfigure(1, weight=1)
		label_descricao = ctk.CTkLabel(frame_descricao, text="Descrição")
		label_descricao.grid(row=0, column=0, padx = 5, pady=5)
		self.nova_tarefa = ctk.CTkEntry(frame_descricao, placeholder_text="Digite a nova tarefa")
		self.nova_tarefa.grid(row=0, column=1, sticky="we", padx = 5, pady=5)
		
		frame_meio = ctk.CTkFrame(self)
		frame_meio.columnconfigure(0, weight=1)
		frame_meio.columnconfigure(1, weight=1)
		frame_meio.pack(expand=True, anchor="n", fill="x", padx = 5, pady=5)
		frame_calendario = ctk.CTkFrame(frame_meio)
		frame_calendario.grid(row=0, column=0, padx = 5, pady=5, sticky="nwe")
		frame_infos = ctk.CTkFrame(frame_meio)
		frame_infos.grid(row=0, column=2, padx = 5, pady=5, sticky="we")
		
		label_vencimento = ctk.CTkLabel(frame_calendario, text="Prazo")
		label_vencimento.grid(row=0, column=0, padx = 5, pady=5, sticky="w")
		
		self.data_vencimento = DateEntry(frame_calendario, background="darkblue", foreground="white", date_pattern="yyyy/mm/dd")
		self.data_vencimento.grid(row=0, column=1, padx = 5, pady=5, sticky="w")
		
		label_prioridade = ctk.CTkLabel(frame_calendario, text="Prioridade")
		label_prioridade.grid(row=1, column=0, padx = 5, pady=5, sticky="w")
		
		self.combo_prioridade =  ctk.CTkComboBox(frame_calendario, values=["Alta", "Média", "Baixa"], state="readonly")
		self.combo_prioridade.set("Baixa")
		self.combo_prioridade.grid(row=1, column=1, padx = 5, pady=5, sticky="w")

		label_grupo = ctk.CTkLabel(frame_calendario, text="Grupo")
		label_grupo.grid(row=2, column=0, padx = 5, pady=5, sticky="w")
		self.grupo = ctk.CTkComboBox(frame_calendario, values=Banco().buscar_grupo(), state="readonly")
		self.grupo.grid(row=2, column=1, padx = 5, pady=5, sticky="w")
		btn_novo_grupo = ctk.CTkButton(frame_calendario, text="Novo grupo", command=self.novo_grupo)
		btn_novo_grupo.grid(row=3, column=0, padx = 5, pady=5, sticky="we")

		frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
		frame_botoes.pack()
		
		btn_salvar = ctk.CTkButton(
			frame_botoes, 
			text="Salvar", 
			command= self.salvar_cadastro
			)
		btn_salvar.grid(row=0, column=0, padx = 5, pady=15)
		
		btn_cancelar = ctk.CTkButton(
			frame_botoes, 
			text="Voltar", 
			command=lambda: controller.controla_janela("Home")
			)
		btn_cancelar.grid(row=0, column=1, padx = 5, pady=15)
		
	def salvar_cadastro(self):
		self.linha_ativa = 0
		tarefa = self.nova_tarefa.get()
		prioridade = self.combo_prioridade.get()
		prazo = self.data_vencimento.get()
		
		if not tarefa:
			messagebox.showinfo("Atenção!", "Digite uma tarefa antes de salvar")
		else:
			try:
				self.nova_tarefa.delete(0, 'end')
				Banco().cadastrar(tarefa, prioridade, prazo, 1)
				messagebox.showinfo("Sucesso!", f"Tarefa {tarefa} salva")
			except Exception as e:
				messagebox.showinfo("Erro!", f"Tarefa {tarefa} nao foi salva {e}")

	def novo_grupo(self):
		
		self.nova_janela = ctk.CTkToplevel(self)
		self.nova_janela.grab_set()

		frame_grupo = ctk.CTkFrame(self.nova_janela)
		frame_grupo.pack(expand=True, side="top", anchor="n", fill="x", padx = 5, pady=5)

		label_grupo = ctk.CTkLabel(frame_grupo, text="Descrição")
		label_grupo.grid(row=0, column=0, padx = 5, pady=5)
		self.descricao_grupo = ctk.CTkEntry(frame_grupo, placeholder_text="Descrição do grupo")
		self.descricao_grupo.grid(row=0, column=1, sticky="we", padx = 5, pady=5)

		btn_salvar_grupo = ctk.CTkButton(frame_grupo, text="Salvar", command=self.salva_grupo)
		btn_salvar_grupo.grid(row=1, column=0,columnspan=2, sticky="we")

	def salva_grupo(self):
		descricao = self.descricao_grupo.get()
		try:
			Banco().cadastra_grupo(descricao)
			self.nova_janela.destroy()
			self.grupo.configure(values=Banco().buscar_grupo())
			messagebox.showinfo("Sucesso!", f"Grupo {descricao} salva")

		except Exception as e:
			messagebox.showinfo("Erro!", f"Grupo {descricao} nao foi salvo {e}")