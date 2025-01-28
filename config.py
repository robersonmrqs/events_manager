import os
import sys

# Obter o caminho base dependendo do modo (executável ou desenvolvimento)
if getattr(sys, 'frozen', False):  # Verifica se está rodando como executável
    BASE_DIR = sys._MEIPASS  # Caminho temporário usado pelo PyInstaller
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho para a pasta de recursos
RESOURCES_DIR = os.path.join(BASE_DIR, "static")