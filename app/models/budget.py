import logging
from datetime import datetime
from . import db

class Budget(db.Model):
    __tablename__ = 'budget'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    month = db.Column(db.String(7), nullable=False, unique=True) # e.g., '2023-10'
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, data):
        """
        新增一筆月度預算記錄
        :param data: dict，包含 month, amount
        :return: Budget 物件 (成功) 或 None (失敗)
        """
        try:
            new_budget = cls(**data)
            db.session.add(new_budget)
            db.session.commit()
            return new_budget
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating Budget: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有月度預算記錄
        :return: Budget 物件的列表
        """
        try:
            return cls.query.all()
        except Exception as e:
            logging.error(f"Error fetching all Budgets: {e}")
            return []

    @classmethod
    def get_by_id(cls, budget_id):
        """
        取得單筆月度預算記錄
        :param budget_id: 預算 ID
        :return: Budget 物件 或 None
        """
        try:
            return cls.query.get(budget_id)
        except Exception as e:
            logging.error(f"Error fetching Budget by ID {budget_id}: {e}")
            return None

    @classmethod
    def update(cls, budget_id, data):
        """
        更新單筆月度預算記錄
        :param budget_id: 預算 ID
        :param data: dict，包含要更新的欄位與值
        :return: 更新後的 Budget 物件 (成功) 或 None (失敗)
        """
        try:
            budget = cls.query.get(budget_id)
            if not budget:
                return None
            for key, value in data.items():
                if hasattr(budget, key):
                    setattr(budget, key, value)
            db.session.commit()
            return budget
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating Budget {budget_id}: {e}")
            return None

    @classmethod
    def delete(cls, budget_id):
        """
        刪除單筆月度預算記錄
        :param budget_id: 預算 ID
        :return: True (成功) 或 False (失敗)
        """
        try:
            budget = cls.query.get(budget_id)
            if not budget:
                return False
            db.session.delete(budget)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting Budget {budget_id}: {e}")
            return False

    @classmethod
    def get_by_month(cls, month_str):
        """
        透過月份字串取得預算記錄
        :param month_str: 月份字串 (格式: YYYY-MM)
        :return: Budget 物件 或 None
        """
        try:
            return cls.query.filter_by(month=month_str).first()
        except Exception as e:
            logging.error(f"Error fetching Budget by month {month_str}: {e}")
            return None
