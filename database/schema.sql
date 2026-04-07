-- Sports Club Membership System Schema

-- Members Table
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Plans Table (e.g. Monthly, Quarterly, Yearly)
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    duration_months INTEGER NOT NULL
);

-- Memberships Table (Links Member to Plan)
CREATE TABLE IF NOT EXISTS memberships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'active', -- active, expired, canceled
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (plan_id) REFERENCES plans(id)
);

-- Payments Table
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    membership_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending', -- pending, completed, failed
    FOREIGN KEY (membership_id) REFERENCES memberships(id)
);

-- Access Logs Table
CREATE TABLE IF NOT EXISTS access_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted BOOLEAN NOT NULL,
    message TEXT,
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- VIEW for Active Members with Membership Status
CREATE VIEW IF NOT EXISTS active_members_view AS
SELECT 
    m.id, 
    m.first_name, 
    m.last_name, 
    ms.status as membership_status,
    ms.end_date,
    CASE 
        WHEN ms.end_date >= date('now') AND ms.status = 'active' THEN 'Access Allowed'
        ELSE 'Access Denied'
    END as access_status
FROM members m
JOIN memberships ms ON m.id = ms.member_id;
