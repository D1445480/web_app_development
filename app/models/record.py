from datetime import datetime
from .database import get_db

class Record:
    @staticmethod
    def create(amount, type, category_id, date, note=""):
        with get_db() as conn:
            cursor = conn.cursor()
            now = datetime.utcnow().isoformat()
            cursor.execute(
                "INSERT INTO records (amount, type, category_id, date, note, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (amount, type, category_id, date, note, now)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all(month=None, category_id=None):
        query = '''
            SELECT r.*, c.name as category_name
            FROM records r
            JOIN categories c ON r.category_id = c.id
            WHERE 1=1
        '''
        params = []
        if month:
            query += " AND r.date LIKE ?"
            params.append(f"{month}-%")
        if category_id:
            query += " AND r.category_id = ?"
            params.append(category_id)
            
        query += " ORDER BY r.date DESC, r.created_at DESC"
        
        with get_db() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(record_id):
        with get_db() as conn:
            query = '''
                SELECT r.*, c.name as category_name
                FROM records r
                JOIN categories c ON r.category_id = c.id
                WHERE r.id = ?
            '''
            cursor = conn.execute(query, (record_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def update(record_id, amount, type, category_id, date, note=""):
        with get_db() as conn:
            conn.execute(
                "UPDATE records SET amount = ?, type = ?, category_id = ?, date = ?, note = ? WHERE id = ?",
                (amount, type, category_id, date, note, record_id)
            )
            conn.commit()

    @staticmethod
    def delete(record_id):
        with get_db() as conn:
            conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
            conn.commit()
