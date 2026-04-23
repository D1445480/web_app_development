# 系統架構設計文件 (Architecture)

根據個人記帳簿系統 PRD，以下為本專案的系統架構設計。

## 1. 技術架構說明

本專案採用輕量化的後端渲染架構，適合快速開發個人工具：

*   **後端框架：Python + Flask**
    *   **原因**：Flask 輕量、靈活，學習曲線平緩，非常適合用來開發小型的個人記帳應用程式。
*   **模板引擎：Jinja2**
    *   **原因**：內建於 Flask，不需前後端分離的複雜設定，由伺服器端直接將資料渲染成 HTML 回傳給瀏覽器，可有效縮短開發時間。
*   **資料庫：SQLite (搭配 SQLAlchemy ORM)**
    *   **原因**：SQLite 是單一檔案形式的關聯式資料庫，無需額外安裝資料庫伺服器，部署極為方便。使用 SQLAlchemy 可以防止 SQL Injection，並以物件導向的方式操作資料庫，提升程式碼可讀性與安全性。

### Flask MVC 模式說明

*   **Model (模型)**：負責定義資料結構與資料庫互動邏輯（如：帳目、類別的資料表定義）。
*   **View (視圖)**：負責呈現使用者介面，使用 Jinja2 標籤來呈現動態資料。
*   **Controller (控制器)**：在 Flask 中由路由（Routes）擔任，負責接收 HTTP 請求、處理業務邏輯（如新增一筆帳目）、向 Model 存取資料，最後將結果丟給 View 渲染成 HTML。

---

## 2. 專案資料夾結構

為了保持程式碼整潔與易於維護，專案採用以下結構：

```text
web_app_development/
├── app/                  # Flask 應用程式主目錄
│   ├── __init__.py       # 應用程式工廠與初始化 (初始化 Flask, DB 等)
│   ├── models.py         # 資料庫模型定義 (Model)
│   ├── routes.py         # 路由與控制器邏輯 (Controller)
│   ├── templates/        # HTML 模板目錄 (View)
│   │   ├── base.html     # 共用的頁面佈局與導覽列
│   │   ├── index.html    # 首頁 / 總覽頁面
│   │   ├── add.html      # 新增/編輯收支紀錄頁面
│   │   └── list.html     # 歷史紀錄列表與搜尋結果頁面
│   └── static/           # 靜態資源目錄
│       ├── css/
│       │   └── style.css # 自訂樣式表
│       └── js/
│           └── main.js   # 前端互動邏輯 (如需)
├── instance/
│   └── database.db       # SQLite 資料庫檔案 (運行時自動產生)
├── docs/                 # 專案說明文件目錄
│   ├── PRD.md            # 產品需求文件
│   └── ARCHITECTURE.md   # 系統架構文件 (本文件)
├── config.py             # 系統設定檔 (如資料庫路徑、Secret Key)
├── requirements.txt      # 專案相依套件清單
└── run.py                # 應用程式啟動入口腳本
```

---

## 3. 元件關係圖

以下展示了系統中各個元件的互動流程：

```mermaid
graph TD
    Browser[瀏覽器 Browser]
    
    subgraph "Flask Application"
        Router[Flask Route<br/>(Controller)]
        View[Jinja2 Template<br/>(View)]
        Model[Database Model<br/>(Model)]
    end
    
    DB[(SQLite 資料庫)]
    
    Browser -- "1. HTTP Request<br/>(GET/POST)" --> Router
    Router -- "2. 查詢/寫入資料" --> Model
    Model -- "3. SQL/ORM 操作" --> DB
    DB -- "4. 回傳資料結果" --> Model
    Model -- "5. 資料物件" --> Router
    Router -- "6. 傳遞資料並請求渲染" --> View
    View -- "7. 渲染 HTML" --> Router
    Router -- "8. HTTP Response<br/>(HTML 頁面)" --> Browser
```

---

## 4. 關鍵設計決策

1.  **採用伺服器渲染 (SSR)**：
    *   **原因**：考慮到這是個人專案且為 MVP 範圍，不採用複雜的 React/Vue 前後端分離架構。使用 Flask + Jinja2 可以在單一專案內快速完成開發，且網頁載入速度可輕易達到「1秒內呈現」的需求。
2.  **導入 SQLAlchemy 作為 ORM**：
    *   **原因**：PRD 要求防止 SQL Injection。比起直接串接 `sqlite3` 寫原生的 SQL 語句，ORM 不僅天生具備防範 SQL Injection 的能力，也讓新增、修改、刪除（CRUD）的語法更直覺易懂。
3.  **使用應用程式工廠模式 (Application Factory)**：
    *   **原因**：將 `app` 初始化寫在 `app/__init__.py` 中，將設定、資料庫與路由分開。這樣不僅解決了後續如果專案變大容易發生「循環匯入 (Circular Import)」的問題，也利於未來擴展或撰寫單元測試。
4.  **精簡的靜態資源管理**：
    *   **原因**：考量到頁面互動需求較單純，暫不引入 Webpack 等前端打包工具。直接使用 `static` 目錄存放純 CSS 與 JavaScript 檔案，以保持架構輕量。
