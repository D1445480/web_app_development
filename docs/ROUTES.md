# 路由設計文件 (Routes Design)

根據 PRD 與資料庫設計，以下為系統的路由規劃。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **總覽首頁** | `GET` | `/` | `index.html` | 顯示當月總收支、預算狀態與近期紀錄 |
| **紀錄列表** | `GET` | `/transactions` | `transactions/list.html` | 顯示所有收支紀錄，支援條件篩選與搜尋 |
| **新增紀錄頁面** | `GET` | `/transactions/new` | `transactions/form.html` | 顯示新增收支的表單 |
| **建立紀錄** | `POST` | `/transactions` | — | 接收表單資料，寫入 DB 並重導向至首頁或列表 |
| **編輯紀錄頁面** | `GET` | `/transactions/<id>/edit` | `transactions/form.html` | 顯示單筆收支的編輯表單 (帶有預設值) |
| **更新紀錄** | `POST` | `/transactions/<id>/update` | — | 接收表單資料，更新該筆紀錄，重導向至列表 |
| **刪除紀錄** | `POST` | `/transactions/<id>/delete` | — | 刪除單筆紀錄，重導向至列表 |
| **類別列表** | `GET` | `/categories` | `categories/list.html` | (Nice to Have) 顯示自訂類別列表 |
| **新增類別頁面** | `GET` | `/categories/new` | `categories/form.html` | (Nice to Have) 顯示新增類別表單 |
| **建立類別** | `POST` | `/categories` | — | (Nice to Have) 接收表單，寫入 DB，重導向至類別列表 |

## 2. 每個路由的詳細說明

### 2.1 總覽首頁 (`/`)
- **輸入**: 無參數 (可選：`month` 參數篩選特定月份)
- **處理邏輯**: 查詢當月所有的 `Transaction`，計算總收入與總支出；若有設定 `Budget` 則一併計算剩餘預算。
- **輸出**: 渲染 `index.html`，傳遞 `total_income`, `total_expense`, `recent_transactions`, `budget` 等變數。
- **錯誤處理**: 查詢異常時紀錄 log 並回傳通用錯誤訊息。

### 2.2 收支紀錄相關 (`/transactions/...`)
- **列表 (`GET /transactions`)**
  - **輸入**: 搜尋條件 (`start_date`, `end_date`, `category_id`, `keyword` 等)。
  - **處理邏輯**: 根據條件呼叫 `Transaction` Model 篩選資料。
  - **輸出**: 渲染 `transactions/list.html`。
- **新增 (`POST /transactions`)**
  - **輸入**: 表單資料 (`amount`, `type`, `date`, `category_id`, `description`)。
  - **處理邏輯**: 驗證必填欄位，呼叫 `Transaction(…).save()` 寫入。
  - **輸出**: 成功則 `redirect('/')`。
  - **錯誤處理**: 驗證失敗則 `render_template` 回表單並附帶錯誤訊息。
- **更新 (`POST /transactions/<id>/update`)**
  - **輸入**: 表單資料與紀錄 ID。
  - **處理邏輯**: `Transaction.get_by_id(id)`，更新屬性後呼叫 `save()`。
  - **輸出**: 成功則 `redirect('/transactions')`。
  - **錯誤處理**: 找不到 ID 回傳 404，驗證失敗重繪表單。
- **刪除 (`POST /transactions/<id>/delete`)**
  - **輸入**: 紀錄 ID。
  - **處理邏輯**: `Transaction.get_by_id(id).delete()`。
  - **輸出**: `redirect('/transactions')`。

## 3. Jinja2 模板清單

所有的 HTML 檔案皆放於 `app/templates/` 目錄底下，並繼承共用的基礎版型 `base.html`。

- `base.html`: 共用外觀、導覽列 (Navbar) 與引入 CSS/JS。
- `index.html`: 首頁，繼承自 `base.html`，顯示儀表板。
- `transactions/list.html`: 紀錄列表與搜尋介面。
- `transactions/form.html`: 共用於新增與編輯收支紀錄的表單頁面。
- `categories/list.html`: 類別管理列表 (Nice to have)。
- `categories/form.html`: 類別新增表單 (Nice to have)。

## 4. 路由骨架程式碼
已在 `app/routes/` 中建立各個模組 (Blueprints)：
- `__init__.py`: 用於註冊所有 Blueprints。
- `main.py`: 首頁等共用路由。
- `transaction.py`: 處理收支紀錄 CRUD 的路由。
- `category.py`: 處理類別管理的路由。
