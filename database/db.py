import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "spendly.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    with conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                email         TEXT    UNIQUE NOT NULL,
                password_hash TEXT    NOT NULL,
                created_at    TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                amount      REAL    NOT NULL,
                category    TEXT    NOT NULL,
                date        TEXT    NOT NULL,
                description TEXT,
                created_at  TEXT    DEFAULT (datetime('now'))
            );
        """)
    conn.close()


def seed_db():
    conn = get_db()
    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    with conn:
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
        )
        uid = conn.execute(
            "SELECT id FROM users WHERE email = 'demo@spendly.com'"
        ).fetchone()["id"]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?,?,?,?,?)",
            [
                (uid, 12.50,  "Food",          "2026-05-20", "Coffee and bagel"),
                (uid, 65.00,  "Other",         "2026-05-19", "Weekly groceries"),
                (uid,  9.99,  "Entertainment", "2026-05-18", "Spotify subscription"),
                (uid, 42.00,  "Transport",     "2026-05-17", "Gas fill-up"),
                (uid, 120.00, "Bills",         "2026-05-15", "Electric bill"),
                (uid,  8.75,  "Food",          "2026-05-14", "Lunch"),
                (uid, 29.99,  "Shopping",      "2026-05-12", "New phone case"),
                (uid, 55.00,  "Health",        "2026-05-10", "Pharmacy"),
            ],
        )
    conn.close()
