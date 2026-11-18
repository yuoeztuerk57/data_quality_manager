import os
import sqlite3

DEFAULT_DB_PATH = "data/dataquality.db"
DEFAULT_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection(db_path=DEFAULT_DB_PATH):
    folder = os.path.dirname(db_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

def init_db(connection, schema_path=DEFAULT_SCHEMA_PATH):
    with open(schema_path, "r", encoding="utf-8") as file:
        schema_sql = file.read()
    connection.executescript(schema_sql)
    connection.commit()