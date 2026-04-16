from flask import Blueprint, render_template, request, flash
from datetime import datetime
from app.models.record import Record
from app.models.category import Category

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """
    GET /
    處理首頁月度收支總攬。
    - 處理邏輯：
      1. 取得當前月份
      2. 呼叫 Record.get_list_by_filter(month) 取得當月紀錄
      3. 計算總收入、總支出與結餘
      4. 預算提醒：稽查所有有預算限制的分類是否超支
    - 輸出：轉交給 templates/dashboard.html 並帶上計算好的資料
    """
    # 取得本月字串 (YYYY-MM)
    current_month = datetime.now().strftime('%Y-%m')
    target_month = request.args.get('month', current_month)
    
    # 撈取當月紀錄
    records = Record.get_list_by_filter(month=target_month)
    categories = Category.get_all()
    
    total_income = 0
    total_expense = 0
    category_expenses = {} # 存放 category_id -> int (方便計算預算與圖表)
    
    for r in records:
        if r['type'] == 'income':
            total_income += r['amount']
        else:
            total_expense += r['amount']
            cat_id = r['category_id']
            category_expenses[cat_id] = category_expenses.get(cat_id, 0) + r['amount']
            
    balance = total_income - total_expense
    
    # 預算提醒判定：找出有預算的分類，若目前開銷大於預算，塞入 Alert 陣列
    budget_alerts = []
    for c in categories:
        if c['budget'] and c['type'] == 'expense':
            spent = category_expenses.get(c['id'], 0)
            if spent >= c['budget']:
                budget_alerts.append(f"注意！「{c['name']}」的本月花費 (${spent}) 已經達到或超過您的預算上限 (${c['budget']})！")
    
    return render_template(
        'dashboard.html',
        month=target_month,
        records=records,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        alerts=budget_alerts,
        category_expenses=category_expenses
    )
