from flask import Flask
from app.routes.dashboard import dashboard_bp
from app.routes.record import record_bp
from app.routes.category import category_bp

def create_app():
    app = Flask(__name__)
    # 在正式環境中，請使用 os.environ.get('SECRET_KEY') 來抓取安全性憑證
    app.secret_key = 'your_secret_key_here'

    # 註冊 Blueprints 藍圖
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(record_bp)
    app.register_blueprint(category_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
