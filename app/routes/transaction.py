from flask import Blueprint, render_template, request, redirect, url_for

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/')
def list_transactions():
    """
    顯示所有收支紀錄列表，並處理搜尋與篩選條件。
    - 接收 Query String 中的搜尋條件
    - 從資料庫查詢符合的紀錄
    - 渲染 transactions/list.html
    """
    pass

@transaction_bp.route('/new', methods=['GET'])
def new_transaction():
    """
    顯示新增收支紀錄的表單頁面。
    - 從資料庫取得所有可用的類別清單
    - 渲染 transactions/form.html
    """
    pass

@transaction_bp.route('/', methods=['POST'])
def create_transaction():
    """
    處理新增收支紀錄的表單送出。
    - 接收表單資料
    - 驗證必填欄位與格式
    - 存入資料庫
    - 重導向到首頁或列表頁
    """
    pass

@transaction_bp.route('/<int:id>/edit', methods=['GET'])
def edit_transaction(id):
    """
    顯示編輯收支紀錄的表單頁面。
    - 根據 ID 查詢該筆紀錄 (若無則 404)
    - 將紀錄資料傳入表單作為預設值
    - 渲染 transactions/form.html
    """
    pass

@transaction_bp.route('/<int:id>/update', methods=['POST'])
def update_transaction(id):
    """
    處理更新收支紀錄的表單送出。
    - 根據 ID 查詢該筆紀錄 (若無則 404)
    - 接收並驗證新的表單資料
    - 更新資料庫中的紀錄
    - 重導向到列表頁
    """
    pass

@transaction_bp.route('/<int:id>/delete', methods=['POST'])
def delete_transaction(id):
    """
    處理刪除收支紀錄的操作。
    - 根據 ID 刪除該筆紀錄
    - 重導向到列表頁
    """
    pass
