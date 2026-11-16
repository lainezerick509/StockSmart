import sqlite3
import os

# Ubicación de la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_DIR = os.path.join(BASE_DIR, "database")

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "stocksmart.db"
)


# Conectar con SQLite
def get_db_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# Crear las tablas
def init_db():

    os.makedirs(DATABASE_DIR, exist_ok=True)

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS productos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT NOT NULL,

            categoria TEXT NOT NULL,

            precio REAL NOT NULL,

            cantidad INTEGER NOT NULL DEFAULT 0,

            stock_minimo INTEGER NOT NULL DEFAULT 5,

            fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()