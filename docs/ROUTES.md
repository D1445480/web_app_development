# 路由設計文件 (ROUTES) - 個人記帳簿系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 月度收支總攬 | GET | `/` | `templates/dashboard.html` | 首頁：顯示當月總結與預定圖表 |
| 記帳紀錄列表 | GET | `/records` | `templates/records.html` | 顯示所有收支明細，支援參數搜尋 |
| 新增收支紀錄 | GET, POST | `/records/new` | `templates/form_record.html` | GET: 顯示表格<br>POST: 接收表單寫入資料庫 |
| 編輯單筆紀錄 | GET, POST | `/records/<id>/edit` | `templates/form_record.html` | GET: 取出資料供修改<br>POST: 存入修改值 |
| 刪除單筆紀錄 | POST | `/records/<id>/delete`| — | 執行刪除並重導向 |
| 分類與預算列表| GET | `/categories` | `templates/categories.html` | 條列分類清單與其預算設定 |
| 建立新分類 | GET, POST | `/categories/new` | `templates/form_category.html` | GET: 顯示表格<br>POST: 建立分類 |
| 編輯分類設定 | GET, POST | `/categories/<id>/edit`| `templates/form_category.html` | 修改名稱或類別屬性 |
| 刪除指定分類 | POST | `/categories/<id>/delete`| — | 刪除分類（連動刪除隸屬明細） |
| 設定單一預算 | POST | `/categories/<id>/budget`| — | 於列表頁更新預算後發送此操作 |

## 2. 每個路由的詳細說明

請參考 `app/routes/` 裡的 python 檔案所標示之 Docstring 註解，裡面詳細記載了各個路由：
- 會被傳入哪些 URL 參數
- 將要呼叫哪些 Model API 例如 `Record.get_all()` 或 `Category.update()`
- 最終是 Redirect 還是呼叫 `render_template` 轉換畫面。

## 3. Jinja2 模板清單

所有的網頁模板都會被集中收納於 `app/templates/` 當中。

- `base.html` (骨架)：系統整體的共用外觀，包含 Navbar，以及資源 CSS/JS 的匯入。以下所有頁面皆會繼承此底層。
- `dashboard.html`：顯示給使用者的第一站，大數字的收支總攬。
- `records.html`：以表格條列化所有明細。
- `form_record.html`：新增或編輯任一記帳明細的共用表單網頁。
- `categories.html`：列出類別並可以針對每個項目直接輸入新預算。
- `form_category.html`：新增或編輯分類的共用表單網頁。
