import customtkinter as ctk
import os
from config import RESOURCES_DIR
from gui.event_form import EventForm
from gui.history_view import HistoryView
from gui.report_view import ReportView
from PIL import Image
from tkinter import messagebox
from controllers.validar_data import validar_data

class CalendarView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciador de Eventos")
        self.geometry("600x400")

        self.iconbitmap(os.path.join(RESOURCES_DIR, "icons", "favicon.ico"))

        # Carregar imagem de fundo usando CTkImage
        self.background_image = ctk.CTkImage(Image.open(os.path.join(RESOURCES_DIR, "images", "background.jpg")), size=(300, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.background_image, text="")
        self.bg_label.place(x=0, y=0)

        # Elementos da interface
        self.calendar_label = ctk.CTkLabel(self, text="Selecione uma data:", font=("Arial", 18))
        self.calendar_label.place(x=370, y=30)

        self.date_entry = ctk.CTkEntry(self, placeholder_text="DD/MM/AAAA", width=200, height=40, font=("Arial", 16), justify="center")
        self.date_entry.place(x=350, y=90)

        self.select_date_button = ctk.CTkButton(self, text="Selecionar Data", command=self.open_event_form, width=200, height=40, font=("Arial", 16))
        self.select_date_button.place(x=350, y=160)

        self.history_button = ctk.CTkButton(self, text="Visualizar Histórico", command=self.open_history, width=200, height=40, font=("Arial", 16))
        self.history_button.place(x=350, y=220)

        self.report_button = ctk.CTkButton(self, text="Gerar Relatório", command=self.open_report, width=200, height=40, font=("Arial", 16))
        self.report_button.place(x=350, y=280)

        self.exit_button = ctk.CTkButton(self, text="Sair", command=self.quit, width=100, height=40, font=("Arial", 16), fg_color="#FF0000")
        self.exit_button.place(x=400, y=350)

    def open_event_form(self):
        selected_date = self.date_entry.get()
        if not validar_data(selected_date):
            messagebox.showwarning("Data Inválida", "Por favor, insira uma data válida no formato DD/MM/AAAA!")
            return

        self.withdraw()  # Esconde a tela principal
        EventForm(self, selected_date)

    def clear_date(self):
        """
        Limpa o campo de data.
        """
        self.date_entry.delete(0, "end")

    def open_history(self):
        self.withdraw()  # Esconde a tela principal
        HistoryView(self)

    def open_report(self):
        self.withdraw()  # Esconde a tela principal
        ReportView(self)

    def show(self):
        self.deiconify()  # Mostra a tela principal