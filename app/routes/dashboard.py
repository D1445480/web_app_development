from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """
    GET /
    處理首頁月度收支總攬。
    - 處理邏輯：
      1. 取得當前月份
      2. 呼叫 Record.get_all(month) 取得當月紀錄
      3. 計算總收入、總支出與結餘
    - 輸出：轉交給 templates/dashboard.html 並帶上計算好的資料
    """
    pass
