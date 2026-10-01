import tkinter as tk
from database.db import get_connection
from datetime import date

class Dashboard(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f4f6f8")
        tk.Label(self, text="Dashboard", bg="#f4f6f8", fg="#111827",
                 font=("Segoe UI", 24, "bold")).pack(anchor="w", padx=30, pady=(25, 5))
        tk.Label(self, text="Library overview", bg="#f4f6f8", fg="#64748b",
                 font=("Segoe UI", 11)).pack(anchor="w", padx=30, pady=(0, 20))
        self.cards = tk.Frame(self, bg="#f4f6f8")
        self.cards.pack(fill="x", padx=30)
        self.refresh()

    def refresh(self):
        for w in self.cards.winfo_children(): w.destroy()
        with get_connection() as c:
            books = c.execute("SELECT COUNT(*), COALESCE(SUM(copies),0), COALESCE(SUM(available_copies),0) FROM books").fetchone()
            borrowers = c.execute("SELECT COUNT(*) FROM borrowers").fetchone()[0]
            issued = c.execute("SELECT COUNT(*) FROM transactions WHERE status='Issued'").fetchone()[0]
            overdue = c.execute("SELECT COUNT(*) FROM transactions WHERE status='Issued' AND due_date < ?", (date.today().isoformat(),)).fetchone()[0]
        data = [("Book Titles", books[0]), ("Total Copies", books[1]), ("Available Copies", books[2]),
                ("Borrowers", borrowers), ("Issued Transactions", issued), ("Overdue", overdue)]
        for i, (label, value) in enumerate(data):
            card = tk.Frame(self.cards, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
            card.grid(row=i//3, column=i%3, padx=7, pady=7, sticky="nsew")
            tk.Label(card, text=str(value), bg="white", fg="#2563eb", font=("Segoe UI", 25, "bold")).pack(pady=(18,2))
            tk.Label(card, text=label, bg="white", fg="#64748b", font=("Segoe UI", 10)).pack(pady=(0,18))
        for col in range(3): self.cards.columnconfigure(col, weight=1)
