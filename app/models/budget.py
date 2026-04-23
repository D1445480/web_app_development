from datetime import datetime
from . import db

class Budget(db.Model):
    __tablename__ = 'budget'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    month = db.Column(db.String(7), nullable=False, unique=True) # e.g., '2023-10'
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_by_month(cls, month_str):
        return cls.query.filter_by(month=month_str).first()
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
