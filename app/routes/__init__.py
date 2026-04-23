from flask import Flask
from .main import main_bp
from .transaction import transaction_bp
from .category import category_bp
from .budget import budget_bp

def register_routes(app: Flask):
    """將所有 Blueprints 註冊到 Flask app"""
    app.register_blueprint(main_bp)
    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(budget_bp, url_prefix='/budget')
