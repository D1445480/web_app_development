# 系統流程圖與使用者流程 (FLOWCHART) - 個人記帳簿系統

## 1. 使用者流程圖 (User Flow)

這份流程圖展示了使用者造訪網站後，可以採取的主要行動路徑。

```mermaid
flowchart LR
    A([使用者造訪網頁]) --> B[首頁 - 月度收支總覽]
    B --> C{要執行什麼操作？}
    
    C -->|查看明細| D[記帳紀錄清單]
    C -->|點擊「新增」| E[填寫收支表單]
    C -->|管理分類| F[類別與統計頁面]
    
    D -->|利用條件篩選| D
    D -->|選取單筆編輯| G[修改記帳紀錄]
    D -->|選取單筆刪除| H[確認刪除對話方塊]
    
    H -->|確定刪除| D
    G -->|儲存變更| D
    
    E -->|送出表單| B
    
    F -->|新增自訂類別| I[分類管理表單]
    F -->|設定預算| J[預算設定對話框]
    I -->|儲存| F
    J -->|儲存| F
```

## 2. 系統序列圖 (Sequence Diagram)

這份序列圖描述了核心功能：「使用者點擊新增一筆支出」到「資料成功存入資料庫」的完整技術流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask (Controller)
    participant Model as 資料模型 (Model)
    participant DB as SQLite資料庫
    
    User->>Browser: 填妥支出表單 (金額, 類別, 日期) 後送出
    Browser->>Flask: 發送 HTTP POST /records/new
    Flask->>Flask: Controller 進行參數驗證 (避免金額格式錯誤)
    
    alt 驗證失敗
        Flask-->>Browser: 重新渲染表單 (GET /records/new) 並帶上錯誤提示
    else 驗證成功
        Flask->>Model: 將驗證過濾後的資料交給 Model
        Model->>DB: 執行 SQL (INSERT INTO records ...)
        DB-->>Model: 回傳執行結果 (Success)
        Model-->>Flask: 回傳建立成功狀態
        Flask-->>Browser: HTTP 302 重新導向 (Redirect) 至首頁
        Browser->>Flask: 發送 GET / (請求首頁資料)
        Flask-->>Browser: 渲染包含最新紀錄的首頁 HTML
        Browser->>User: 顯示已更新的首頁與成功訊息
    end
```

## 3. 功能清單對照表

將上述的使用者體驗與系統操作轉化為對應的 URL 路徑與 HTTP 方法清單。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| 月度收支總覽 | `/` 或 `/dashboard` | GET | 網站首頁，顯示當月總收支、餘額與預算概況 |
| 記帳紀錄清單 | `/records` | GET | 顯示所有紀錄明細，可使用 URL Query String 進行搜尋篩選 (例: `?month=2024-05`) |
| 新增收支紀錄 | `/records/new` | GET, POST | GET: 取得並渲染空白表單<br>POST: 接收表單欄位進資料庫 |
| 編輯單筆紀錄 | `/records/<id>/edit` | GET, POST | GET: 取得欲修改的資料並填入表單<br>POST: 儲存修改過的新資料 |
| 刪除單筆紀錄 | `/records/<id>/delete`| POST | 以發送表單的方式對系統請求刪除該筆資料 |
| 類別清單與統計 | `/categories` | GET | 列出消費分類並顯示占比圓餅圖 |
| 新增自訂類別 | `/categories/new` | GET, POST | GET: 渲染建立類別表單<br>POST: 將新類別存入資料庫 |
| 設定類別預算 | `/categories/<id>/budget`| POST | 提交表單以更新對應分類的預算上限 |
