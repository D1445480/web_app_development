import logging
from datetime import datetime
from . import db

class Transaction(db.Model):
    __tablename__ = 'transaction'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'income' or 'expense'
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, data):
        """
        新增一筆收支記錄
        :param data: dict，包含 amount, type, date, description, category_id
        :return: Transaction 物件 (成功) 或 None (失敗)
        """
        try:
            new_transaction = cls(**data)
            db.session.add(new_transaction)
            db.session.commit()
            return new_transaction
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating Transaction: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有收支記錄 (依日期與建立時間降冪排序)
        :return: Transaction 物件的列表
        """
        try:
            return cls.query.order_by(cls.date.desc(), cls.created_at.desc()).all()
        except Exception as e:
            logging.error(f"Error fetching all Transactions: {e}")
            return []

    @classmethod
    def get_by_id(cls, transaction_id):
        """
        取得單筆收支記錄
        :param transaction_id: 收支紀錄 ID
        :return: Transaction 物件 或 None
        """
        try:
            return cls.query.get(transaction_id)
        except Exception as e:
            logging.error(f"Error fetching Transaction by ID {transaction_id}: {e}")
            return None

    @classmethod
    def update(cls, transaction_id, data):
        """
        更新單筆收支記錄
        :param transaction_id: 收支紀錄 ID
        :param data: dict，包含要更新的欄位與值
        :return: 更新後的 Transaction 物件 (成功) 或 None (失敗)
        """
        try:
            transaction = cls.query.get(transaction_id)
            if not transaction:
                return None
            for key, value in data.items():
                if hasattr(transaction, key):
                    setattr(transaction, key, value)
            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating Transaction {transaction_id}: {e}")
            return None

    @classmethod
    def delete(cls, transaction_id):
        """
        刪除單筆收支記錄
        :param transaction_id: 收支紀錄 ID
        :return: True (成功) 或 False (失敗)
        """
        try:
            transaction = cls.query.get(transaction_id)
            if not transaction:
                return False
            db.session.delete(transaction)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting Transaction {transaction_id}: {e}")
            return False
