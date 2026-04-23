import logging
from datetime import datetime
from . import db

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'income' or 'expense'
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯
    transactions = db.relationship('Transaction', backref='category', lazy=True)

    @classmethod
    def create(cls, data):
        """
        新增一筆類別記錄
        :param data: dict，包含 name, type, is_default 等資料
        :return: Category 物件 (成功) 或 None (失敗)
        """
        try:
            new_category = cls(**data)
            db.session.add(new_category)
            db.session.commit()
            return new_category
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating Category: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有類別記錄
        :return: Category 物件的列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error fetching all Categories: {e}")
            return []

    @classmethod
    def get_by_id(cls, category_id):
        """
        取得單筆類別記錄
        :param category_id: 類別 ID
        :return: Category 物件 或 None
        """
        try:
            return cls.query.get(category_id)
        except Exception as e:
            logging.error(f"Error fetching Category by ID {category_id}: {e}")
            return None

    @classmethod
    def update(cls, category_id, data):
        """
        更新單筆類別記錄
        :param category_id: 類別 ID
        :param data: dict，包含要更新的欄位與值
        :return: 更新後的 Category 物件 (成功) 或 None (失敗)
        """
        try:
            category = cls.query.get(category_id)
            if not category:
                return None
            for key, value in data.items():
                if hasattr(category, key):
                    setattr(category, key, value)
            db.session.commit()
            return category
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating Category {category_id}: {e}")
            return None

    @classmethod
    def delete(cls, category_id):
        """
        刪除單筆類別記錄
        :param category_id: 類別 ID
        :return: True (成功) 或 False (失敗)
        """
        try:
            category = cls.query.get(category_id)
            if not category:
                return False
            db.session.delete(category)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting Category {category_id}: {e}")
            return False
