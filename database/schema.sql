CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    budget INTEGER,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER NOT NULL CHECK(amount >= 0),
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    category_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    note TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
