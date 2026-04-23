from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models.transaction import Transaction
from app.models.category import Category

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/')
def list_transactions():
    """
    顯示所有收支紀錄列表，並處理搜尋與篩選條件。
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category_id = request.args.get('category_id')
    keyword = request.args.get('keyword')

    query = Transaction.query

    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Transaction.date >= start_date_obj)
        except ValueError:
            pass

    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Transaction.date <= end_date_obj)
        except ValueError:
            pass

    if category_id and category_id.isdigit():
        query = query.filter(Transaction.category_id == int(category_id))

    if keyword:
        query = query.filter(Transaction.description.ilike(f'%{keyword}%'))

    transactions = query.order_by(Transaction.date.desc(), Transaction.created_at.desc()).all()
    categories = Category.get_all()
    
    return render_template('transactions/list.html', 
                           transactions=transactions, 
                           categories=categories,
                           start_date=start_date,
                           end_date=end_date,
                           selected_category_id=category_id,
                           keyword=keyword)

@transaction_bp.route('/new', methods=['GET'])
def new_transaction():
    """
    顯示新增收支紀錄的表單頁面。
    """
    categories = Category.get_all()
    return render_template('transactions/form.html', categories=categories, transaction=None)

@transaction_bp.route('/', methods=['POST'])
def create_transaction():
    """
    處理新增收支紀錄的表單送出。
    """
    amount = request.form.get('amount')
    txn_type = request.form.get('type')
    date_str = request.form.get('date')
    category_id = request.form.get('category_id')
    description = request.form.get('description', '')

    if not amount or not txn_type or not date_str or not category_id:
        flash('請填寫所有必填欄位 (金額、類型、日期、類別)', 'danger')
        return redirect(url_for('transaction.new_transaction'))

    try:
        amount = float(amount)
        txn_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        category_id = int(category_id)
    except ValueError:
        flash('資料格式錯誤', 'danger')
        return redirect(url_for('transaction.new_transaction'))

    data = {
        'amount': amount,
        'type': txn_type,
        'date': txn_date,
        'category_id': category_id,
        'description': description
    }

    txn = Transaction.create(data)
    if txn:
        flash('成功新增紀錄！', 'success')
        # 成功後導回列表頁
        return redirect(url_for('transaction.list_transactions')) 
    else:
        flash('新增失敗，請稍後再試。', 'danger')
        return redirect(url_for('transaction.new_transaction'))

@transaction_bp.route('/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    """
    顯示編輯收支紀錄的表單頁面。
    """
    transaction = Transaction.get_by_id(id)
    if not transaction:
        flash('找不到該筆紀錄', 'warning')
        return redirect(url_for('transaction.list_transactions'))
        
    categories = Category.get_all()
    return render_template('transactions/form.html', categories=categories, transaction=transaction)

@transaction_bp.route('/<int:id>/update', methods=['POST'])
def update_transaction(id):
    """
    處理更新收支紀錄的表單送出。
    """
    amount = request.form.get('amount')
    txn_type = request.form.get('type')
    date_str = request.form.get('date')
    category_id = request.form.get('category_id')
    description = request.form.get('description', '')

    if not amount or not txn_type or not date_str or not category_id:
        flash('請填寫所有必填欄位 (金額、類型、日期、類別)', 'danger')
        return redirect(url_for('transaction.edit_transaction', id=id))

    try:
        amount = float(amount)
        txn_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        category_id = int(category_id)
    except ValueError:
        flash('資料格式錯誤', 'danger')
        return redirect(url_for('transaction.edit_transaction', id=id))

    data = {
        'amount': amount,
        'type': txn_type,
        'date': txn_date,
        'category_id': category_id,
        'description': description
    }

    txn = Transaction.update(id, data)
    if txn:
        flash('成功更新紀錄！', 'success')
        return redirect(url_for('transaction.list_transactions'))
    else:
        flash('更新失敗，請稍後再試。', 'danger')
        return redirect(url_for('transaction.edit_transaction', id=id))

@transaction_bp.route('/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    處理刪除收支紀錄的操作。
    """
    success = Transaction.delete(id)
    if success:
        flash('紀錄已成功刪除。', 'success')
    else:
        flash('刪除失敗，找不到紀錄或系統發生錯誤。', 'danger')
        
    return redirect(url_for('transaction.list_transactions'))
