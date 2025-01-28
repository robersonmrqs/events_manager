import customtkinter as ctk
import os
import pandas as pd
from config import RESOURCES_DIR
from fpdf import FPDF, XPos, YPos
from models.database import fetch_events, get_event_statistics
from PIL import Image
from tkinter import messagebox, filedialog

class ReportView(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Relatório de Eventos")
        self.geometry("600x400")

        # Soma total de eventos e horas
        total_events, total_hours = get_event_statistics()  # Chamada centralizada

        # Carregar imagem de fundo usando CTkImage
        self.background_image = ctk.CTkImage(Image.open(os.path.join(RESOURCES_DIR, "images", "background_2.jpg")), size=(300, 400))
        self.bg_label = ctk.CTkLabel(self, image=self.background_image, text="")
        self.bg_label.place(x=0, y=0)

        # Labels para mostrar dados
        self.total_events_label = ctk.CTkLabel(self, text=f"Total de Eventos: {total_events}", font=("Arial", 18))
        self.total_events_label.place(x=370, y=20)

        self.total_hours_label = ctk.CTkLabel(self, text=f"Total de Horas: {total_hours}", font=("Arial", 18))
        self.total_hours_label.place(x=360, y=80)

        # Botões para exportação
        self.export_excel_button = ctk.CTkButton(self, text="Exportar para Excel", command=self.export_to_excel, width=200, height=40, font=("Arial", 16))
        self.export_excel_button.place(x=350, y=150)

        self.export_pdf_button = ctk.CTkButton(self, text="Exportar para PDF", command=self.export_to_pdf, width=200, height=40, font=("Arial", 16))
        self.export_pdf_button.place(x=350, y=220)

        self.back_button = ctk.CTkButton(self, text="Voltar", command=self.return_to_main, width=100, height=40, font=("Arial", 16), fg_color="#FF0000")
        self.back_button.place(x=400, y=350)

    def export_to_excel(self):
        events = fetch_events()  # Chamada centralizada
        df = pd.DataFrame(events, columns=["ID", "Data", "Título", "Horas", "Resumo"])  # Adapte as colunas conforme necessário

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Sucesso", "Relatório exportado para Excel com sucesso!")

    def export_to_pdf(self):
        eventos = fetch_events()  # Chamada centralizada

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Atualize a configuração da fonte:
            pdf.set_font("helvetica", size=12)  # "Arial" é substituído por "helvetica"

            # Atualize os parâmetros renomeados:
            pdf.cell(200, 10, text="Relatório de Eventos", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
            pdf.ln(10)

            for evento in eventos:
                pdf.cell(0, 10, text=f"ID: {evento[0]}, Data: {evento[1]}, Título: {evento[2]}, Horas: {evento[3]}, Resumo: {evento[4]}",
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            pdf.output(file_path)
            messagebox.showinfo("Sucesso", "Relatório exportado para PDF com sucesso!")

    def return_to_main(self):
        self.destroy()
        self.parent.show()