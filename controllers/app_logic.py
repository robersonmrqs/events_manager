from gui.calendar_view import CalendarView
from models.database import initialize_database

class EventManagerApp:
    def __init__(self):
        # Inicialização do banco de dados
        initialize_database()

        # Configuração das interfaces gráficas
        self.calendar = CalendarView()

    def run(self):
        self.calendar.mainloop()

def initialize_app():
    app = EventManagerApp()
    app.run()