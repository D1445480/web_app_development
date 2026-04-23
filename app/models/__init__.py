from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 匯入 models 讓 SQLAlchemy 註冊
from .category import Category
from .transaction import Transaction
from .budget import Budget
