from flask import Blueprint, request, redirect, url_for, render_template

record_bp = Blueprint('record', __name__, url_prefix='/records')

@record_bp.route('/', methods=['GET'])
def index():
    """
    GET /records
    顯示收支紀錄清單並支援條件篩選。
    - 處理邏輯：接收 query string (month, category_id)，呼叫 Record.get_all(...)
    - 輸出：轉交給 templates/records.html
    """
    pass

@record_bp.route('/new', methods=['GET', 'POST'])
def new():
    """
    GET /records/new - 顯示新增表單
    POST /records/new - 接收表單並寫入 Database
    - 處理邏輯：
      GET: 取出 Category.get_all() 供選單使用。
      POST: 讀取表單，呼叫 Record.create(...)。
    - 輸出：成功後 redirect 到 dashboard 或 /records。
    """
    pass

@record_bp.route('/<int:record_id>/edit', methods=['GET', 'POST'])
def edit(record_id):
    """
    GET /records/<id>/edit - 顯示編輯表單並帶入既有資料
    POST /records/<id>/edit - 儲存更新資料
    - 處理邏輯：
      GET: 透過 Record.get_by_id(record_id) 與 Category.get_all() 渲染表單。
      POST: 呼叫 Record.update(...)。
    - 輸出：成功後 redirect 到 /records。
    """
    pass

@record_bp.route('/<int:record_id>/delete', methods=['POST'])
def delete(record_id):
    """
    POST /records/<id>/delete
    實行紀錄刪除操作。
    - 處理邏輯：呼叫 Record.delete(record_id)
    - 輸出：刪除成功後 redirect 到 /records。
    """
    pass
