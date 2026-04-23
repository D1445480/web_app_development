from flask import Blueprint, request, redirect, url_for, flash
from app.models.budget import Budget

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/set', methods=['POST'])
def set_budget():
    """
    設定或更新指定月份的預算
    """
    month_str = request.form.get('month') # 格式: YYYY-MM
    amount_str = request.form.get('amount')

    if not month_str or not amount_str:
        flash('請提供月份與預算金額', 'danger')
        return redirect(url_for('main.index', month=month_str))

    try:
        amount = float(amount_str)
        if amount < 0:
            raise ValueError
    except ValueError:
        flash('預算金額必須為有效的正數', 'danger')
        return redirect(url_for('main.index', month=month_str))

    # 檢查是否已經有該月的預算
    existing_budget = Budget.get_by_month(month_str)
    
    if existing_budget:
        # 更新
        updated = Budget.update(existing_budget.id, {'amount': amount})
        if updated:
            flash(f'成功更新 {month_str} 月預算為 ${amount:.2f}', 'success')
        else:
            flash('更新預算失敗，請稍後再試', 'danger')
    else:
        # 新增
        data = {'month': month_str, 'amount': amount}
        created = Budget.create(data)
        if created:
            flash(f'成功設定 {month_str} 月預算為 ${amount:.2f}', 'success')
        else:
            flash('設定預算失敗，請稍後再試', 'danger')

    return redirect(url_for('main.index', month=month_str))
