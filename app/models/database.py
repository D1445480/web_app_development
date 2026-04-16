import sqlite3
import os

# Assume database is stored at instance/database.db relative to project root
DB_URL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db():
    # Make sure instance folder exists
    os.makedirs(os.path.dirname(DB_URL), exist_ok=True)
    conn = sqlite3.connect(DB_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    with get_db() as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
