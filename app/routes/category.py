from flask import Blueprint, render_template, request, redirect, url_for

category_bp = Blueprint('category', __name__)

@category_bp.route('/')
def list_categories():
    """
    顯示所有類別列表。
    - 從資料庫查詢所有類別
    - 渲染 categories/list.html
    """
    pass

@category_bp.route('/new', methods=['GET'])
def new_category():
    """
    顯示新增類別的表單頁面。
    - 渲染 categories/form.html
    """
    pass

@category_bp.route('/', methods=['POST'])
def create_category():
    """
    處理新增類別的表單送出。
    - 接收表單資料
    - 驗證並存入資料庫
    - 重導向到類別列表
    """
    pass
