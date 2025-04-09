import customtkinter as ctk
from funcoes import Banco
from tkinter import messagebox

class Listar(ctk.CTkFrame):
	def __init__(self, janela, controller):
		super().__init__(janela)
		self.linha_ativa = 0
			
		self.frame_lista = ctk.CTkScrollableFrame(self)
		self.frame_lista.pack(expand=True, fill="both", pady=4, padx=4)
		self.frame_lista.columnconfigure(0, weight=1)
		self.contruir_tabela()
		def abre_pomodoro():
			if self.linha_ativa == 0:
				messagebox.showinfo("Atenção!", "Selecione a tarefa que deseja trabalhar")
			else:
				Banco().pomodoro(self.linha_ativa)
				controller.controla_janela("Pomodoro")
		
		frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
		frame_botoes.pack(expand=True)
		
		btn_pomodoro = ctk.CTkButton(
			frame_botoes, 
			text="Concluir com pomodoro",
			command=abre_pomodoro
			)
		btn_pomodoro.grid(row=0, column=0, columnspan=2, sticky="ew", pady=4, padx=4)

		btn_concluir = ctk.CTkButton(
			frame_botoes, 
			text="Tarefa concluida",
			command=self.concluir_tarefa
			)
		btn_concluir.grid(row=1, column=0, pady=4, padx=4)
		
		btn_remover = ctk.CTkButton(
			frame_botoes, 
			text="Remover tarefa",
			command=self.remover_tarefa
			)
		btn_remover.grid(row=1, column=1, pady=4, padx=4)
		
		btn_cancelar = ctk.CTkButton(
			frame_botoes, 
			text="Voltar", 
			command=lambda: controller.controla_janela("Home")
			)
		btn_cancelar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=4, padx=4)
		
	def contruir_tabela(self):
		for widget in self.frame_lista.winfo_children():
			widget.destroy()
		frame_cab = ctk.CTkFrame(self.frame_lista)
		frame_cab.columnconfigure(0, weight=0)
		frame_cab.columnconfigure(1, weight=1)
		frame_cab.columnconfigure(2, weight=1)
		frame_cab.columnconfigure(3, weight=1)
		frame_cab.columnconfigure(4, weight=1)
		frame_cab.columnconfigure(5, weight=1)
		frame_cab.grid(row=0, column=0, sticky='nswe')
		cabecalho = ["ID","Descrição", "Status", "prioridade", "Prazo", "Grupo"]
		tarefas = Banco().buscar()
		
		for item in cabecalho:
			if cabecalho.index(item) == 0:
					tamanho = 10
			elif cabecalho.index(item) == 1:
				tamanho = 200
			else: 
				tamanho = 10
			label_cab = ctk.CTkLabel(
				frame_cab, 
				text=item,
				font=("Segoe UI", 16),
				fg_color="#3b657a",
				text_color="white",
				justify="left",
				width=tamanho
				)
			label_cab.grid(
				row=0, 
				column=cabecalho.index(item),
				pady=0,
				padx=0,
				sticky='nswe'
				)
		contador = 1
		for tarefa in tarefas:
			if self.linha_ativa == tarefa[0]:
				cor = "#2A9D8F"
				cor_texto = "#20130a"
			else:
				cor = "#123142" if contador % 2 == 0 else "#142026"
				cor_texto = "white"
			frame_linha = ctk.CTkFrame(self.frame_lista)
			frame_linha.columnconfigure(0, weight=0)
			frame_linha.columnconfigure(1, weight=2)
			frame_linha.columnconfigure(2, weight=1)
			frame_linha.columnconfigure(3, weight=1)
			frame_linha.columnconfigure(4, weight=2)
			frame_linha.columnconfigure(5, weight=1)
			for item in tarefa:
				if tarefa.index(item) == 0:
					tamanho = 10
				elif tarefa.index(item) == 1:
					tamanho = 300
				else: 
					tamanho = 150
				label_tarefa = ctk.CTkLabel(
					frame_linha, 
					text=item,
					font=("Segoe UI", 16),
					fg_color=cor,
					text_color=cor_texto,
					justify="left",
					width=tamanho
					)
				label_tarefa.grid(
					row=0, 
					column=tarefa.index(item),
					sticky='nswe'
					)
				label_tarefa.bind("<Button-1>",lambda e, t=tarefa: self.identifica_id(t))
			
					
					
			frame_linha.grid(
				row=contador, 
				column=0,
				pady=0,
				padx=0,
				sticky='nswe'
				)
			contador += 1
	
	def identifica_id(self, tarefa):
		self.linha_ativa = tarefa[0]
		self.contruir_tabela()
		print("tarefa: ", tarefa[0])

		
	def remover_tarefa(self):
		if self.linha_ativa == 0:
			messagebox.showinfo("Atenção!", "Selecione a tarefa que deseja remover")
		else:
			verifica = messagebox.askyesno("Atenção!", "Deseja realmente remover esta tarefa?")
			if verifica:
				Banco().apagar(self.linha_ativa)

				self.linha_ativa = 0
				self.recarregar_tela()
				
	def concluir_tarefa(self):
		if self.linha_ativa == 0:
			messagebox.showinfo("Atenção!", "Selecione a tarefa que deseja modificar o status")
		else:
			verifica = messagebox.askyesno("Atenção!", "Deseja realmente marcar esta tarefa como conluida?")
			if verifica:
				Banco().editar(self.linha_ativa)

				self.linha_ativa = 0
				self.recarregar_tela()
				
	def recarregar_tela(self):
		self.linha_ativa = 0 
		self.contruir_tabela()
		self.update_idletasks()
		