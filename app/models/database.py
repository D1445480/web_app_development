import sqlite3
import os

# Assume database is stored at instance/database.db relative to project root
DB_URL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """
    建立並回傳一個對 SQLite 的資料庫連線。
    預設啟用了 sqlite3.Row，使得查詢結果能像 dictionary 般以欄位名稱取值。
    """
    try:
        os.makedirs(os.path.dirname(DB_URL), exist_ok=True)
        conn = sqlite3.connect(DB_URL)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def init_db():
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    try:
        with get_db_connection() as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
        raise
