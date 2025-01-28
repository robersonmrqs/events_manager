import customtkinter as ctk
import os
from config import RESOURCES_DIR
from controllers.transcription import transcribe_audio, transcribe_live_audio
from models.database import insert_event
from PIL import Image
from tkinter import messagebox, filedialog

class EventForm(ctk.CTkToplevel):
    def __init__(self, parent, selected_date):
        super().__init__(parent)

        self.parent = parent
        self.title("Cadastro de Evento")
        self.geometry("400x520")

        self.selected_date = selected_date

        self.label = ctk.CTkLabel(self, text=f"Data Selecionada: {self.selected_date}", font=("Arial", 18))
        self.label.pack(pady=20)

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Título do Evento", width=200, height=40, font=("Arial", 16), justify="center")
        self.title_entry.pack(pady=10)

        self.hours_entry = ctk.CTkEntry(self, placeholder_text="Horas Dispendidas", width=200, height=40, font=("Arial", 16), justify="center")
        self.hours_entry.pack(pady=10)

        # Campo de texto com ícones posicionados verticalmente
        self.summary_frame = ctk.CTkFrame(self, width=350, height=200)
        self.summary_frame.pack(pady=10)

        self.summary_entry = ctk.CTkTextbox(self.summary_frame, width=300, height=150, font=("Arial", 16))
        self.summary_entry.grid(row=0, column=0, rowspan=2, padx=(0, 10))

        # Ícone de transcrição de áudio ao vivo
        microphone_icon = ctk.CTkImage(Image.open(os.path.join(RESOURCES_DIR, "icons", "microfone.png")).resize((24, 24)))

        self.transcribe_button = ctk.CTkButton(
            self.summary_frame,
            image=microphone_icon,
            text="",
            width=40,
            height=40,
            command=self.start_microphone_timer
        )
        self.transcribe_button.grid(row=0, column=1, pady=(0, 10))

        # Ícone de upload de áudio
        upload_icon = ctk.CTkImage(Image.open(os.path.join(RESOURCES_DIR, "icons", "anexo.png")).resize((24, 24)))

        self.upload_audio_button = ctk.CTkButton(
            self.summary_frame,
            image=upload_icon,
            text="",
            width=40,
            height=40,
            command=self.upload_audio
        )
        self.upload_audio_button.grid(row=1, column=1)

        self.save_button = ctk.CTkButton(self, text="Salvar Evento", command=self.save_event, width=200, height=40, font=("Arial", 16))
        self.save_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self, text="Voltar", command=self.return_to_main, width=100, height=40, font=("Arial", 16), fg_color="#FF0000")
        self.back_button.pack(pady=20)

    def start_microphone_timer(self):
        self.timer_label = ctk.CTkLabel(self, text="Prepare-se para falar em 3 segundos", font=("Arial", 12))
        self.timer_label.place(x=100, y=320)
        self.after(1000, lambda: self.timer_label.configure(text="2 segundos"))
        self.after(2000, lambda: self.timer_label.configure(text="1 segundo"))
        self.after(3000, self.transcribe_audio_live)

    def transcribe_audio_live(self):
        if hasattr(self, 'timer_label'):
            self.timer_label.place_forget()
        transcription = transcribe_live_audio()
        if transcription:
            self.summary_entry.insert("end", transcription)

    def upload_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos de áudio", "*.wav *.mp3 *.ogg *.flac *.dat")])
        if file_path:
            transcription = transcribe_audio(file_path)
            if transcription:
                self.summary_entry.insert("end", transcription)

    def save_event(self):
        title = self.title_entry.get()
        hours = self.hours_entry.get()
        summary = self.summary_entry.get("1.0", "end").strip()

        if not title or not hours or not summary:
            messagebox.showwarning("Campos Vazios", "Preencha todos os campos antes de salvar!")
            return

        try:
            insert_event(self.selected_date, title, float(hours), summary)

            messagebox.showinfo("Sucesso", "Evento salvo com sucesso!")
            self.destroy()
            self.parent.show()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o evento: {e}")

    def return_to_main(self):
        self.destroy()
        self.parent.clear_date()  # Limpa a data ao retornar para a tela principal
        self.parent.show()