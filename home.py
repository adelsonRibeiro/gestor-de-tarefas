import customtkinter as ctk

class Home(ctk.CTkFrame):
	def __init__(self, janela, controller):
		super().__init__(janela)
		
		
		titulo = ctk.CTkLabel(
			self, 
			text="Bem Vindo ao gestor de tarefas", 
			font=(
				"Segoe UI", 
				20, 
				"bold"
				)
			)
		titulo.pack(side="top", anchor="n", fill="x", pady=7)
		
		frame_botoes = ctk.CTkFrame(self)
		frame_botoes.pack(anchor="center")
		
		btn_adicionar = ctk.CTkButton(
			frame_botoes, 
			text="Adicionar", 
			command= lambda: controller.controla_janela("Cadastro")
			)
		btn_adicionar.grid(row=0, column=0)
		
		btn_listar = ctk.CTkButton(
			frame_botoes, 
			text="Listar", 
			command=lambda: controller.controla_janela("Listar")
			)
		btn_listar.grid(row=0, column=1, padx=5)