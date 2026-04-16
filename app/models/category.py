from datetime import datetime
from .database import get_db

class Category:
    @staticmethod
    def create(name, type, budget=None):
        with get_db() as conn:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute(
                "INSERT INTO categories (name, type, budget, created_at) VALUES (?, ?, ?, ?)",
                (name, type, budget, now)
            )
            conn.commit()
            return cursor.lastrowid
            
    @staticmethod
    def get_all():
        with get_db() as conn:
            cursor = conn.execute("SELECT * FROM categories ORDER BY name ASC")
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(category_id):
        with get_db() as conn:
            cursor = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def update(category_id, name, type, budget=None):
        with get_db() as conn:
            conn.execute(
                "UPDATE categories SET name = ?, type = ?, budget = ? WHERE id = ?",
                (name, type, budget, category_id)
            )
            conn.commit()

    @staticmethod
    def delete(category_id):
        with get_db() as conn:
            conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            conn.commit()
