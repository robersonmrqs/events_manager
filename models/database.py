import os
import sqlite3
from config import RESOURCES_DIR

DB_PATH = os.path.join(RESOURCES_DIR, "event_manager.db")

def initialize_database():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Criação da tabela de eventos, caso não exista
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY,
        data TEXT,
        titulo TEXT,
        horas TEXT,
        resumo TEXT
    )
    """)
    connection.commit()
    connection.close()

def insert_event(date, title, hours, description):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO eventos (data, titulo, horas, resumo)
    VALUES (?, ?, ?, ?)
    """, (date, title, hours, description))

    connection.commit()
    connection.close()

def search_events(keyword):
    """
    Busca eventos no banco de dados com base em uma palavra-chave.
    Retorna eventos cujo título ou resumo correspondam ao termo buscado.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, data, titulo, horas, resumo FROM eventos WHERE titulo LIKE ? OR resumo LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")
    )

    results = cursor.fetchall()
    connection.close()
    return results


def fetch_events():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM eventos")
    events = cursor.fetchall()

    connection.close()
    return events

def get_event_statistics():
    """
    Retorna o total de eventos e a soma das horas dispendidas.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*), SUM(horas) FROM eventos")
    total_events, total_hours = cursor.fetchone()
    connection.close()

    return total_events, total_hours


def delete_event(event_id):
    """
    Exclui um evento pelo ID.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM eventos WHERE id = ?", (event_id,))
    connection.commit()
    connection.close()