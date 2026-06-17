import sqlite3
import os

DB_NAME = "crime_intelligence.db"
DB_PATH = os.path.join(os.path.dirname(__file__), '..', DB_NAME)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
