from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.category import Category

category_bp = Blueprint('category', __name__)

@category_bp.route('/')
def list_categories():
    """
    顯示所有類別列表。
    """
    categories = Category.get_all()
    return render_template('categories/list.html', categories=categories)

@category_bp.route('/new', methods=['GET'])
def new_category():
    """
    顯示新增類別的表單頁面。
    """
    return render_template('categories/form.html', category=None)

@category_bp.route('/', methods=['POST'])
def create_category():
    """
    處理新增類別的表單送出。
    """
    name = request.form.get('name')
    cat_type = request.form.get('type')

    if not name or not cat_type:
        flash('請填寫類別名稱與類型', 'danger')
        return redirect(url_for('category.new_category'))

    data = {
        'name': name,
        'type': cat_type,
        'is_default': False
    }

    cat = Category.create(data)
    if cat:
        flash('成功新增類別！', 'success')
        return redirect(url_for('category.list_categories'))
    else:
        flash('新增失敗，請稍後再試。', 'danger')
        return redirect(url_for('category.new_category'))

@category_bp.route('/<int:id>/edit', methods=['GET'])
def edit_category(id):
    """
    顯示編輯類別的表單頁面。
    """
    category = Category.get_by_id(id)
    if not category:
        flash('找不到該筆類別', 'warning')
        return redirect(url_for('category.list_categories'))
        
    return render_template('categories/form.html', category=category)

@category_bp.route('/<int:id>/update', methods=['POST'])
def update_category(id):
    """
    處理更新類別的表單送出。
    """
    name = request.form.get('name')
    cat_type = request.form.get('type')

    if not name or not cat_type:
        flash('請填寫類別名稱與類型', 'danger')
        return redirect(url_for('category.edit_category', id=id))

    data = {
        'name': name,
        'type': cat_type
    }

    cat = Category.update(id, data)
    if cat:
        flash('成功更新類別！', 'success')
        return redirect(url_for('category.list_categories'))
    else:
        flash('更新失敗，請稍後再試。', 'danger')
        return redirect(url_for('category.edit_category', id=id))

@category_bp.route('/<int:id>/delete', methods=['POST'])
def delete_category(id):
    """
    處理刪除類別的操作。
    """
    category = Category.get_by_id(id)
    if not category:
        flash('找不到該筆類別', 'danger')
        return redirect(url_for('category.list_categories'))
        
    if category.is_default:
        flash('預設類別無法刪除！', 'warning')
        return redirect(url_for('category.list_categories'))

    success = Category.delete(id)
    if success:
        flash('類別已成功刪除。', 'success')
    else:
        flash('刪除失敗，可能有收支紀錄正在使用此類別，因此無法刪除。', 'danger')
        
    return redirect(url_for('category.list_categories'))
