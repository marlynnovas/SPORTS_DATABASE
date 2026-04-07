-- =========================
-- DATABASE: SPORTS CLUB
-- =========================

PRAGMA foreign_keys = ON;

-- =========================
-- MEMBERS
-- =========================
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT UNIQUE,
    join_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- =========================
-- PLANS
-- =========================
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    duration_days INTEGER NOT NULL CHECK(duration_days > 0),
    price REAL NOT NULL CHECK(price > 0)
);

-- =========================
-- MEMBERSHIPS
-- =========================
CREATE TABLE IF NOT EXISTS memberships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,

    status TEXT NOT NULL CHECK(
        status IN ('active', 'expired', 'suspended', 'pending')
    ),

    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY (plan_id) REFERENCES plans(id)
);

-- =========================
-- PAYMENTS
-- =========================
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    membership_id INTEGER,
    amount REAL NOT NULL CHECK(amount > 0),
    payment_date DATE NOT NULL DEFAULT CURRENT_DATE,

    payment_status TEXT NOT NULL CHECK(
        payment_status IN ('paid', 'pending', 'failed')
    ),

    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (membership_id) REFERENCES memberships(id)
);

-- =========================
-- ACCESS LOGS
-- =========================
CREATE TABLE IF NOT EXISTS access_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    access_date DATE NOT NULL DEFAULT CURRENT_DATE,
    access_time TIME NOT NULL DEFAULT CURRENT_TIME,

    result TEXT NOT NULL CHECK(
        result IN ('granted', 'denied')
    ),

    message TEXT,

    FOREIGN KEY (member_id) REFERENCES members(id)
);