from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.models.record import Record
from app.models.category import Category
import datetime

record_bp = Blueprint('record', __name__, url_prefix='/records')

@record_bp.route('/', methods=['GET'])
def index():
    """
    GET /records
    顯示收支紀錄清單並支援條件篩選。
    """
    month = request.args.get('month')
    category_id = request.args.get('category_id')
    
    # 進行搜尋篩選功能
    records = Record.get_list_by_filter(month=month, category_id=category_id)
    categories = Category.get_all()
    return render_template('records.html', records=records, categories=categories, selected_month=month, selected_cat=category_id)

@record_bp.route('/new', methods=['GET', 'POST'])
def new():
    """
    GET /records/new - 顯示新增表單
    POST /records/new - 接收表單並寫入 Database (收支快速記錄)
    """
    if request.method == 'POST':
        amount = request.form.get('amount')
        type_val = request.form.get('type')
        category_id = request.form.get('category_id')
        date_str = request.form.get('date')
        note = request.form.get('note', '')
        
        # 基礎輸入防呆驗證
        if not amount or not date_str or not category_id:
            flash("請填寫所有必填欄位（金額、日期、分類）。", "error")
            return redirect(url_for('record.new'))
            
        try:
            Record.create({
                'amount': int(amount),
                'type': type_val,
                'category_id': int(category_id),
                'date': date_str,
                'note': note
            })
            flash("成功新增記錄！", "success")
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            flash(f"系統錯誤：{str(e)}", "error")
            
    categories = Category.get_all()
    today = datetime.date.today().strftime('%Y-%m-%d')
    return render_template('form_record.html', categories=categories, record=None, today=today)

@record_bp.route('/<int:record_id>/edit', methods=['GET', 'POST'])
def edit(record_id):
    """
    GET /records/<id>/edit - 顯示編輯表單
    POST /records/<id>/edit - 儲存更新資料
    """
    record = Record.get_by_id(record_id)
    if not record:
        flash("找不到該筆記錄", "error")
        return redirect(url_for('record.index'))

    if request.method == 'POST':
        amount = request.form.get('amount')
        type_val = request.form.get('type')
        category_id = request.form.get('category_id')
        date_str = request.form.get('date')
        note = request.form.get('note', '')
        
        if not amount or not date_str or not category_id:
            flash("請填寫所有必填欄位。", "error")
            return redirect(url_for('record.edit', record_id=record_id))
            
        Record.update(record_id, {
            'amount': int(amount),
            'type': type_val,
            'category_id': int(category_id),
            'date': date_str,
            'note': note
        })
        flash("記錄更新成功！", "success")
        return redirect(url_for('record.index'))
        
    categories = Category.get_all()
    return render_template('form_record.html', categories=categories, record=record, today=record['date'])

@record_bp.route('/<int:record_id>/delete', methods=['POST'])
def delete(record_id):
    """實行紀錄刪除操作"""
    Record.delete(record_id)
    flash("紀錄已成功刪除", "success")
    return redirect(url_for('record.index'))
