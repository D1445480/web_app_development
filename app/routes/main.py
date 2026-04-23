from flask import Blueprint, render_template, request
from datetime import datetime
from app.models.transaction import Transaction
from app.models.budget import Budget
from sqlalchemy import extract

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示月度收支總覽與近期紀錄 (含類別統計)。
    - 取得指定月份或當月所有交易紀錄
    - 計算總收入、總支出、結餘
    - 取得預算狀態
    - 計算圓餅圖所需的類別統計資料
    - 渲染 index.html
    """
    # 處理 month 參數，格式為 'YYYY-MM'
    month_param = request.args.get('month')
    if month_param:
        try:
            target_date = datetime.strptime(month_param, '%Y-%m')
            target_year = target_date.year
            target_month = target_date.month
        except ValueError:
            now = datetime.now()
            target_year = now.year
            target_month = now.month
            month_param = f"{target_year}-{target_month:02d}"
    else:
        now = datetime.now()
        target_year = now.year
        target_month = now.month
        month_param = f"{target_year}-{target_month:02d}"

    # 取得目標月份的所有紀錄
    all_transactions = Transaction.query.filter(
        extract('year', Transaction.date) == target_year,
        extract('month', Transaction.date) == target_month
    ).order_by(Transaction.date.desc(), Transaction.created_at.desc()).all()

    # 計算本月總收入、總支出與結餘
    total_income = sum(t.amount for t in all_transactions if t.type == 'income')
    total_expense = sum(t.amount for t in all_transactions if t.type == 'expense')
    balance = total_income - total_expense

    # 取得預算狀態
    budget = Budget.get_by_month(month_param)
    budget_amount = budget.amount if budget else 0
    remaining_budget = budget_amount - total_expense if budget else None

    # 類別統計 (用於儀表板的圓餅圖)
    category_stats = {}
    for t in all_transactions:
        if t.type == 'expense':
            cat_name = t.category.name if t.category else '未分類'
            category_stats[cat_name] = category_stats.get(cat_name, 0) + t.amount

    return render_template(
        'index.html',
        transactions=all_transactions[:5],  # 僅顯示近期 5 筆紀錄
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        budget_amount=budget_amount,
        remaining_budget=remaining_budget,
        category_stats=category_stats,
        current_year=target_year,
        current_month=target_month,
        current_month_str=month_param
    )
