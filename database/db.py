import os
import sqlite3
from datetime import date, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "library.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publisher TEXT,
            year INTEGER,
            copies INTEGER NOT NULL DEFAULT 1 CHECK(copies >= 0),
            available_copies INTEGER NOT NULL DEFAULT 1 CHECK(available_copies >= 0),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS borrowers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            email TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            borrower_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            fine REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Issued',
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(borrower_id) REFERENCES borrowers(id)
        );
        """)

def seed_demo_data():
    with get_connection() as conn:
        if conn.execute("SELECT COUNT(*) FROM books").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO books(title,author,publisher,year,copies,available_copies) VALUES(?,?,?,?,?,?)",
                [
                    ("Introduction to Python", "Mark Lutz", "O'Reilly", 2022, 5, 5),
                    ("Database Systems", "Thomas Connolly", "Pearson", 2021, 3, 3),
                    ("Computer Networks", "Andrew S. Tanenbaum", "Pearson", 2020, 4, 4),
                ])
        if conn.execute("SELECT COUNT(*) FROM borrowers").fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO borrowers(name,contact,email) VALUES(?,?,?)",
                [("Demo Student", "0700000000", "student@example.com"),
                 ("Library Member", "0711111111", "member@example.com")])

def issue_book(book_id, borrower_id, days=14):
    with get_connection() as conn:
        book = conn.execute("SELECT available_copies FROM books WHERE id=?", (book_id,)).fetchone()
        if not book:
            raise ValueError("Book not found.")
        if book["available_copies"] < 1:
            raise ValueError("No available copy of this book.")
        issue = date.today()
        due = issue + timedelta(days=days)
        conn.execute("UPDATE books SET available_copies=available_copies-1 WHERE id=?", (book_id,))
        conn.execute("""INSERT INTO transactions
                        (book_id,borrower_id,issue_date,due_date,status)
                        VALUES(?,?,?,?, 'Issued')""",
                     (book_id, borrower_id, issue.isoformat(), due.isoformat()))

def return_book(transaction_id):
    with get_connection() as conn:
        row = conn.execute("""SELECT * FROM transactions
                              WHERE id=? AND status='Issued'""", (transaction_id,)).fetchone()
        if not row:
            raise ValueError("Active transaction not found.")
        today = date.today()
        due = date.fromisoformat(row["due_date"])
        late_days = max(0, (today - due).days)
        fine = late_days * 500
        conn.execute("""UPDATE transactions
                        SET return_date=?, fine=?, status='Returned'
                        WHERE id=?""", (today.isoformat(), fine, transaction_id))
        conn.execute("UPDATE books SET available_copies=available_copies+1 WHERE id=?", (row["book_id"],))
        return fine
