from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.models.category import Category
from app.models.record import Record
import datetime

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/', methods=['GET'])
def index():
    """
    GET /categories
    顯示所有收支類別與預算統計。
    """
    categories = Category.get_all()
    
    # 計算當月類別花費供前端畫圓餅圖統計使用
    current_month = datetime.datetime.now().strftime('%Y-%m')
    records = Record.get_list_by_filter(month=current_month)
    
    # 統計當月每個分類的支出總額
    cat_expenses = {}
    for r in records:
        if r['type'] == 'expense':
            c_id = r['category_id']
            cat_expenses[c_id] = cat_expenses.get(c_id, 0) + r['amount']
            
    # 將結算得出的花費塞進類別字典內，供後續取用
    for c in categories:
        c['current_spent'] = cat_expenses.get(c['id'], 0)
        
    return render_template('categories.html', categories=categories, current_month=current_month)

@category_bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        name = request.form.get('name')
        type_val = request.form.get('type')
        budget = request.form.get('budget')
        
        if not name or not type_val:
            flash("請輸入類別名稱與類型", "error")
            return redirect(url_for('category.new'))
            
        budget_val = int(budget) if budget else None
        
        Category.create({
            'name': name,
            'type': type_val,
            'budget': budget_val
        })
        flash("新類別建立成功", "success")
        return redirect(url_for('category.index'))
        
    return render_template('form_category.html', category=None)

@category_bp.route('/<int:category_id>/edit', methods=['GET', 'POST'])
def edit(category_id):
    category = Category.get_by_id(category_id)
    if not category:
        flash("找不到類別資料", "error")
        return redirect(url_for('category.index'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        type_val = request.form.get('type')
        budget = request.form.get('budget')
        
        if not name or not type_val:
            flash("請確認必填欄位", "error")
            return redirect(url_for('category.edit', category_id=category_id))
            
        budget_val = int(budget) if budget else None
        
        Category.update(category_id, {
            'name': name,
            'type': type_val,
            'budget': budget_val
        })
        flash("類別資料已更新", "success")
        return redirect(url_for('category.index'))
        
    return render_template('form_category.html', category=category)

@category_bp.route('/<int:category_id>/delete', methods=['POST'])
def delete(category_id):
    Category.delete(category_id)
    flash("該分類已順利移除", "success")
    return redirect(url_for('category.index'))

@category_bp.route('/<int:category_id>/budget', methods=['POST'])
def update_budget(category_id):
    """快速操作：專門藉由 Ajax 或獨立小表單更新某分類的預算上限。"""
    budget = request.form.get('budget')
    category = Category.get_by_id(category_id)
    if category:
        budget_val = int(budget) if budget else None
        Category.update(category_id, {
            'name': category['name'],
            'type': category['type'],
            'budget': budget_val
        })
        flash(f"已更新「{category['name']}」的預算", "success")
    return redirect(url_for('category.index'))
