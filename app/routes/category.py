from flask import Blueprint, request, redirect, url_for, render_template

category_bp = Blueprint('category', __name__, url_prefix='/categories')

@category_bp.route('/', methods=['GET'])
def index():
    """
    GET /categories
    顯示所有收支類別與預算統計。
    - 處理邏輯：呼叫 Category.get_all()
    - 輸出：轉交給 templates/categories.html
    """
    pass

@category_bp.route('/new', methods=['GET', 'POST'])
def new():
    """
    GET /categories/new - 顯示新增分類表單
    POST /categories/new - 接收表單並建檔
    - 處理邏輯：呼叫 Category.create(...)
    - 輸出：成功後 redirect 到 /categories
    """
    pass

@category_bp.route('/<int:category_id>/edit', methods=['GET', 'POST'])
def edit(category_id):
    """
    GET /categories/<id>/edit - 顯示編輯表單
    POST /categories/<id>/edit - 儲存變更
    - 處理邏輯：呼叫 Category.update(...)
    - 輸出：成功後 redirect 到 /categories
    """
    pass

@category_bp.route('/<int:category_id>/delete', methods=['POST'])
def delete(category_id):
    """
    POST /categories/<id>/delete
    刪除分類，依據 db schema ON DELETE CASCADE 也會一併刪除對應的收支紀錄。
    - 處理邏輯：呼叫 Category.delete(category_id)
    - 輸出：成功後 redirect 到 /categories
    """
    pass

@category_bp.route('/<int:category_id>/budget', methods=['POST'])
def update_budget(category_id):
    """
    POST /categories/<id>/budget
    專門更新某分類的預算上限。
    - 處理邏輯：取得表單上的 budget 參數，併入 Category.update() 操作中。
    - 輸出：重新導向回 /categories
    """
    pass
