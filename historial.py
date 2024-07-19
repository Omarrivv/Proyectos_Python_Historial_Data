import sqlite3
import os
import shutil
from datetime import datetime
def get_chrome_history():
    try:
        # Obtener la ruta de la base de datos
        chrome_profile_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default")
        database_path = os.path.join(chrome_profile_path, "History")
        # Verificar si la base de datos existe
        if not os.path.isfile(database_path):
            print("No se encontró la base de datos de historial de Chrome.")
            return None
        # Copiar la base de datos a un directorio temporal
        temp_path = "temp_history.db"
        shutil.copyfile(database_path, temp_path)
        # Conectarse a la base de datos
        conn = sqlite3.connect(temp_path)
        # Crear un cursor
        cursor = conn.cursor()
        # Ejecutar la consulta
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")
        # Leer los resultados
        results = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        # Eliminar la copia temporal de la base de datos
        os.remove(temp_path)
        return results
    except sqlite3.Error as e:
        print(f"Error al obtener el historial de Chrome: {e}")
        return None
def format_time(timestamp):
    """
    Función para formatear la marca de tiempo UNIX a una cadena de fecha y hora legible.
    """
    try:
        formatted_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time
    except OSError as e:
        print(f"Error al formatear el tiempo: {e}")
        return "Tiempo no disponible"
def print_history(history):
    """
    Función para imprimir el historial de Chrome de forma ordenada.
    """
    if history:
        print("Historial de Chrome:")
        print("-------------------")
        for index, (url, title, last_visit_time) in enumerate(history, start=1):
            print(f"{index}. URL: {url}")
            print(f"   Título: {title}")
            print(f"   Última visita: {format_time(last_visit_time)}")
            print("-------------------")
    else:
        print("No se encontró historial de Chrome.")
if __name__ == "__main__":
    # Obtener el historial
    history = get_chrome_history()
    # Imprimir el historial
    print_history(history)