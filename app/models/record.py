from datetime import datetime
from .database import get_db_connection

class Record:
    @staticmethod
    def create(data):
        """
        新增一筆記帳紀錄。
        :param data: 含有 amount, type, category_id, date, note 的 dictionary (或 tuple)
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                now = datetime.utcnow().isoformat()
                
                amount = data.get('amount') if isinstance(data, dict) else data[0]
                type_val = data.get('type') if isinstance(data, dict) else data[1]
                category_id = data.get('category_id') if isinstance(data, dict) else data[2]
                date_val = data.get('date') if isinstance(data, dict) else data[3]
                note = data.get('note', '') if isinstance(data, dict) else (data[4] if len(data)>4 else '')
                
                cursor.execute(
                    "INSERT INTO records (amount, type, category_id, date, note, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (amount, type_val, category_id, date_val, note, now)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error in Record.create: {e}")
            raise e

    @staticmethod
    def get_all():
        """
        取得所有的記帳紀錄，並包含相應的類別名稱 (category_name)。
        如果需要根據特定條件過濾，建議在 Controllers 裡過濾，
        或者日後擴展為 get_all(month=None, category_id=None)。
        這裡實作為取出全部。
        """
        try:
            query = '''
                SELECT r.*, c.name as category_name
                FROM records r
                JOIN categories c ON r.category_id = c.id
                ORDER BY r.date DESC, r.created_at DESC
            '''
            with get_db_connection() as conn:
                cursor = conn.execute(query)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error in Record.get_all: {e}")
            return []

    @staticmethod
    def get_list_by_filter(month=None, category_id=None):
        """
        支援搜尋過濾的進階 get_all() 函式 (由於設計需求包含特定月份與類別的條件篩選)。
        """
        try:
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
            
            with get_db_connection() as conn:
                cursor = conn.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error in Record.get_list_by_filter: {e}")
            return []

    @staticmethod
    def get_by_id(record_id):
        """依據 id 回傳單筆記帳紀錄。"""
        try:
            with get_db_connection() as conn:
                query = '''
                    SELECT r.*, c.name as category_name
                    FROM records r
                    JOIN categories c ON r.category_id = c.id
                    WHERE r.id = ?
                '''
                cursor = conn.execute(query, (record_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error in Record.get_by_id: {e}")
            return None

    @staticmethod
    def update(record_id, data):
        """
        更新特定記帳紀錄。
        :param record_id: 要更新的紀錄 id
        :param data: 含有 amount, type, category_id, date, note 的 dictionary
        """
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "UPDATE records SET amount = ?, type = ?, category_id = ?, date = ?, note = ? WHERE id = ?",
                    (data['amount'], data['type'], data['category_id'], data['date'], data.get('note', ''), record_id)
                )
                conn.commit()
        except Exception as e:
            print(f"Error in Record.update: {e}")
            raise e

    @staticmethod
    def delete(record_id):
        """刪除指定 id 的記帳紀錄。"""
        try:
            with get_db_connection() as conn:
                conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
                conn.commit()
        except Exception as e:
            print(f"Error in Record.delete: {e}")
            raise e
