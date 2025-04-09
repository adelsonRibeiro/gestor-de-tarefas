import customtkinter as ctk
from home import Home
from cadastro import Cadastro
from listar import Listar
from pomodoro import Pomodoro

class Janela(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.geometry("700x420")
		self.lista_frames = {}
		ctk.set_appearance_mode("dark")
		
		self.frame_principal = ctk.CTkFrame(self)
		self.frame_principal.pack(fill="both", expand=True)
		self.frame_principal.columnconfigure(0, weight=1)
		
			
		self.controla_janela("Home")
		
		
	def controla_janela(self, frame):
		for widget in self.frame_principal.winfo_children():
			widget.destroy()
		for Frame in (Home, Cadastro, Listar, Pomodoro):
			frame_config = Frame(self.frame_principal, self)
			nome_frame = Frame.__name__
			self.lista_frames[nome_frame] = frame_config
			frame_config.grid(row=0, column=0, sticky="nswe")
		frame = self.lista_frames[frame]
		frame.tkraise()


		
	

if __name__ == "__main__":
	app = Janela()
	app.mainloop()