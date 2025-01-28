import customtkinter as ctk
import sqlite3
from models.database import search_events, delete_event
from tkinter import messagebox

class HistoryView(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.title("Histórico de Eventos")
        self.geometry("600x590")

        self.label = ctk.CTkLabel(self, text="Histórico de Eventos", font=("Arial", 18))
        self.label.pack(pady=10)

        # Caixa de busca
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Buscar por palavra-chave", width=300, height=40, font=("Arial", 16), justify="center")
        self.search_entry.pack(pady=10)

        self.search_button = ctk.CTkButton(self, text="Buscar", command=self.search_events, width=200, height=40, font=("Arial", 16))
        self.search_button.pack(pady=15)

        # Área de exibição
        self.result_box = ctk.CTkTextbox(self, width=500, height=200, font=("Arial", 14))
        self.result_box.pack(pady=10)

        # Botões para ações adicionais (inicialmente ocultos)
        self.delete_button = ctk.CTkButton(self, text="Excluir Evento", command=None, width=200, height=40, font=("Arial", 16))
        self.return_button = ctk.CTkButton(self, text="Nova Busca", command=self.return_to_search, width=200, height=40, font=("Arial", 16))

        # Botão para voltar
        self.back_button = ctk.CTkButton(self, text="Voltar", command=self.return_to_main, width=100, height=40, font=("Arial", 16), fg_color="#FF0000")
        self.back_button.place(x=250, y=540)

        # Variável para armazenar o evento selecionado
        self.selected_event = None

    def search_events(self):
        keyword = self.search_entry.get()
        if not keyword:
            messagebox.showwarning("Busca Inválida", "Por favor, insira uma palavra-chave para buscar!")
            return

        try:
            results = search_events(keyword)

            # Limpar a exibição anterior
            self.result_box.delete("1.0", "end")

            # Ocultar botões adicionais
            self.delete_button.pack_forget()
            self.return_button.pack_forget()

            if results:
                for event in results:
                    event_id, data, titulo, horas, resumo = event
                    short_summary = resumo.split("\n")[0][:50] + ("..." if len(resumo) > 50 else "")
                    link_text = f"Data: {data}\nTítulo: {titulo}\nHoras: {horas}\nResumo: {short_summary}\n\n"
                    self.result_box.insert("end", link_text)

                    # Adicionar funcionalidade de clique para selecionar o evento
                    tag_name = str(event_id)
                    start_idx = self.result_box.index("end-6l")  # Pega linha inicial do bloco
                    end_idx = self.result_box.index("end-2l")  # Pega linha final do bloco

                    self.result_box.tag_add(tag_name, start_idx, end_idx)
                    self.result_box.tag_config(tag_name, foreground="blue", underline=True)
                    self.result_box.tag_bind(tag_name, "<Button-1>", lambda e, ev=event: self.show_event_details(ev))
                    self.result_box.tag_bind(tag_name, "<Enter>", lambda e: self.result_box.configure(cursor="hand2"))
                    self.result_box.tag_bind(tag_name, "<Leave>", lambda e: self.result_box.configure(cursor=""))
            else:
                self.result_box.insert("end", "Nenhum evento encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar eventos: {e}")

    def show_event_details(self, event):
        event_id, data, titulo, horas, resumo = event

        # Limpar a exibição anterior
        self.result_box.delete("1.0", "end")

        # Exibir detalhes do evento com separação adicional
        self.result_box.insert("end", f"Data: {data}\n\n")
        self.result_box.insert("end", f"Título: {titulo}\n\n")
        self.result_box.insert("end", f"Horas: {horas}\n\n")
        self.result_box.insert("end", f"Resumo:\n{resumo}\n\n")

        # Atualizar o botão excluir com o evento correto
        self.delete_button.configure(command=lambda: self.delete_event(event_id))
        self.delete_button.place(x=200, y=410)

        # Mostrar o botão voltar
        self.return_button.place(x=200, y=470)

    def delete_event(self, event_id):
        try:
            delete_event(event_id)

            messagebox.showinfo("Sucesso", "Evento excluído com sucesso!")
            self.return_to_search()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir o evento: {e}")

    def return_to_search(self):
        self.result_box.delete("1.0", "end")
        self.delete_button.place_forget()
        self.return_button.place_forget()

    def return_to_main(self):
        self.destroy()
        self.parent.show()