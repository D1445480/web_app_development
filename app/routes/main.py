from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示月度收支總覽與近期紀錄。
    - 取得當月所有交易紀錄
    - 計算總收入、總支出
    - 取得預算狀態
    - 渲染 index.html
    """
    pass
