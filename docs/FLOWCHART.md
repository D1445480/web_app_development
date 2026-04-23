# 系統流程圖與使用者流程 (Flowchart)

根據 PRD 與系統架構設計，以下為個人記帳簿系統的流程規劃。

## 1. 使用者流程圖（User Flow）

此流程圖展示了使用者在網站上可以執行的所有主要操作路徑，包含瀏覽總覽、新增、編輯、刪除收支紀錄等功能。

```mermaid
flowchart LR
    Start([使用者進入網站]) --> Dashboard[首頁 - 月度收支總覽與近期紀錄]
    Dashboard --> Action{選擇操作}
    
    Action -->|點擊「新增紀錄」| AddPage[新增收支頁面]
    AddPage --> FillForm[填寫金額、類別、日期與備註]
    FillForm --> SubmitAdd{送出表單}
    SubmitAdd -->|成功| Dashboard
    SubmitAdd -->|失敗/驗證錯誤| AddPage
    
    Action -->|點擊「檢視所有紀錄」| ListPage[歷史紀錄列表與搜尋頁面]
    ListPage --> Search[使用條件篩選或搜尋]
    Search --> ListPage
    
    ListPage --> RecordAction{對單筆紀錄操作}
    RecordAction -->|點擊「編輯」| EditPage[編輯收支頁面]
    EditPage --> UpdateForm[修改內容並送出]
    UpdateForm -->|成功| ListPage
    
    RecordAction -->|點擊「刪除」| DeleteConfirm[確認刪除視窗/提示]
    DeleteConfirm -->|確認| ListPage
```

## 2. 系統序列圖（Sequence Diagram）

此序列圖詳細描述了使用者執行「新增一筆收支紀錄」時，系統內部從前端瀏覽器、後端 Flask 路由、資料庫模型到 SQLite 的完整互動過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Database Model
    participant DB as SQLite
    
    User->>Browser: 進入「新增收支頁面」填寫表單並送出
    Browser->>Route: POST /add 帶有表單資料 (金額, 類別...)
    Route->>Route: 驗證資料格式與必填欄位
    alt 驗證失敗
        Route-->>Browser: 回傳錯誤訊息並重新渲染表單 (400 Bad Request)
        Browser-->>User: 顯示錯誤提示
    else 驗證成功
        Route->>Model: 呼叫新增紀錄的方法
        Model->>DB: 執行 INSERT INTO ...
        DB-->>Model: 寫入成功
        Model-->>Route: 回傳成功狀態
        Route-->>Browser: 302 重導向至首頁或列表頁 (GET /)
        Browser->>Route: GET /
        Route->>Model: 查詢當月總覽資料
        Model->>DB: 執行 SELECT ...
        DB-->>Model: 回傳資料
        Model-->>Route: 回傳紀錄列表
        Route-->>Browser: 渲染首頁 HTML (200 OK)
        Browser-->>User: 看到新增成功的最新狀態
    end
```

## 3. 功能清單對照表

以下為針對系統主要功能所規劃的對應 URL 路由結構：

| 功能描述 | URL 路徑 | HTTP 方法 | Controller 負責動作 | View (Jinja2) |
| :--- | :--- | :--- | :--- | :--- |
| **月度收支總覽/首頁** | `/` | `GET` | 取得當月總收支、預算狀態與近期紀錄，渲染首頁 | `index.html` |
| **新增收支紀錄 (頁面)** | `/add` | `GET` | 渲染新增表單頁面 | `add.html` |
| **新增收支紀錄 (送出)** | `/add` | `POST` | 接收表單資料，寫入資料庫，成功後重導向至首頁 | *(無，處理後重導向)* |
| **歷史紀錄列表** | `/transactions` | `GET` | 取得所有紀錄，處理搜尋與篩選條件，渲染列表 | `list.html` |
| **編輯收支紀錄 (頁面)** | `/edit/<id>` | `GET` | 依據 ID 取得單筆紀錄，渲染編輯表單 | `add.html` (共用) |
| **編輯收支紀錄 (送出)** | `/edit/<id>` | `POST` | 接收修改資料，更新資料庫，成功後重導向至列表 | *(無，處理後重導向)* |
| **刪除收支紀錄** | `/delete/<id>` | `POST` | 依據 ID 刪除該筆紀錄，成功後重導向至列表 | *(無，處理後重導向)* |
