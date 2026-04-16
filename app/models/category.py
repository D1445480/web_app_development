from datetime import datetime
from .database import get_db_connection

class Category:
    @staticmethod
    def create(data):
        """
        新增一筆類別。
        :param data: list 或 tuple，例如 [name, type, budget] 或 dict 裡面取值
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                now = datetime.utcnow().isoformat()
                
                # 判斷傳入的是 dictionary 還是 tuple/list
                name = data.get('name') if isinstance(data, dict) else data[0]
                type_val = data.get('type') if isinstance(data, dict) else data[1]
                budget = data.get('budget') if isinstance(data, dict) else (data[2] if len(data)>2 else None)
                
                cursor.execute(
                    "INSERT INTO categories (name, type, budget, created_at) VALUES (?, ?, ?, ?)",
                    (name, type_val, budget, now)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error in Category.create: {e}")
            raise e
            
    @staticmethod
    def get_all():
        """獲取所有分類資料。"""
        try:
            with get_db_connection() as conn:
                cursor = conn.execute("SELECT * FROM categories ORDER BY name ASC")
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error in Category.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(category_id):
        """依據 id 獲取單筆分類資訊。"""
        try:
            with get_db_connection() as conn:
                cursor = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            print(f"Error in Category.get_by_id: {e}")
            return None

    @staticmethod
    def update(category_id, data):
        """
        更新特定分類的內容。
        :param category_id: 要更新的 id
        :param data: 含有 name, type, budget 的 dictionary
        """
        try:
            with get_db_connection() as conn:
                conn.execute(
                    "UPDATE categories SET name = ?, type = ?, budget = ? WHERE id = ?",
                    (data['name'], data['type'], data.get('budget'), category_id)
                )
                conn.commit()
        except Exception as e:
            print(f"Error in Category.update: {e}")
            raise e

    @staticmethod
    def delete(category_id):
        """刪除指定 id 的分類 (其對應 records 也將 cascading 刪除)。"""
        try:
            with get_db_connection() as conn:
                conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
                conn.commit()
        except Exception as e:
            print(f"Error in Category.delete: {e}")
            raise e
