import customtkinter as ctk
from tkinter import messagebox
from funcoes import Banco

class Pomodoro(ctk.CTkFrame):
	def __init__(self, janela, controller):
		super().__init__(janela)
		self.hora = 0
		self.minuto = 0
		self.segundo = 0
		self.limite = 25
		self.valor_circulo = 0
		self.calculo_circulo = 360 / (60 * 60)
		self.situacao_atual = "Comece sua atividade"
		self.controller = controller
		
		self.titulo = ctk.CTkLabel(
			self, 
			text=f"00:00:00", 
			font=(
				"Segoe UI", 
				20, 
				"bold"
				)
			)
		self.titulo.pack(side="top", anchor="n", fill="x", pady=7)
		self.btn_incio = ctk.CTkButton(self, text="iniciar", command=self.inicio)
		self.btn_incio.pack(pady=2, padx=2)
		self.btn_voltar = ctk.CTkButton(self, text="Voltar", command=lambda: controller.controla_janela("Listar"))
		self.btn_voltar.pack(pady=2, padx=2)
		
		frame_contagem = ctk.CTkFrame(self)
		frame_contagem.pack(anchor="center")

		self.label_momento = ctk.CTkLabel(frame_contagem, text=self.situacao_atual )
		self.label_momento.pack(anchor="center")

		self.canvas = ctk.CTkCanvas(frame_contagem, width=250, height=300, bg="#2E2E2E",highlightthickness=0)
		self.canvas.pack(anchor="center")

		bbox = (
			25, 25,
			250 - 25,
			250 - 25
		)

		self.arco_id = self.canvas.create_arc(
			*bbox,
			start=90,
			extent=0,
			style="pieslice",
			outline="#216EAB",
			fill="#216EAB",
			width=4
		)

        
    
	def inicio(self):
		self.situacao_atual = "Hora de trabalhar!"
		self.label_momento.configure(text=self.situacao_atual)
		self.atualizar_tempo()
		self.btn_incio.configure(state="disabled")
		self.btn_voltar.configure(state="disabled")
	
	def atualizar_tempo(self):
		if self.minuto != self.limite:
			if self.segundo == 60:
				self.segundo = 0
				self.minuto +=1
			self.segundo += 1
			self.titulo.configure(text=f"{self.hora:02}:{self.minuto:02}:{self.segundo:02}")
			self.valor_circulo += self.calculo_circulo
			self.canvas.itemconfig(self.arco_id, extent=self.valor_circulo)
			self.after(1, self.atualizar_tempo)
		elif self.minuto == 60:
			verifica = messagebox.askyesno("Atenção!", """Você chegou ao final do ciclo! Deseja concluir a tarefa?
Ao negar você poderá inciar um novo ciclo.""")
			if verifica:
				id = Banco().busca_id()
				Banco().editar(id)
				self.controller.controla_janela("Listar")
			else:
				self.segundo = 0
				self.minuto = 0
				self.valor_circulo = 0
				self.btn_incio.configure(state="normal")
				self.btn_voltar.configure(state="normal")
		else:
			self.define_momento()
	
	def define_momento(self):
		if self.situacao_atual == "Hora de trabalhar!":
			messagebox.showinfo("Atenção!", "Hora de fazer uma pausa")
			self.limite += 5
			self.situacao_atual = "Hora de descansar!"
			self.label_momento.configure(text=self.situacao_atual)
			self.atualizar_tempo()
		else:
			messagebox.showinfo("Atenção!", "Hora de voltar ao trabalho")
			self.limite += 25
			self.situacao_atual = "Hora de trabalhar!"
			self.label_momento.configure(text=self.situacao_atual)
			self.atualizar_tempo()
		
		