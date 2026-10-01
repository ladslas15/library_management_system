import tkinter as tk
from tkinter import messagebox
from database.db import initialize_database
from views.dashboard import Dashboard
from views.books import BooksView
from views.borrowers import BorrowersView
from views.issue_book import IssueBookView
from views.return_book import ReturnBookView
from views.reports import ReportsView

BG = "#f4f6f8"
SIDEBAR = "#1f2937"
ACCENT = "#2563eb"

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("1200x720")
        self.minsize(1050, 650)
        self.configure(bg=BG)
        initialize_database()
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text="LIBRARY", bg=SIDEBAR, fg="white",
                 font=("Segoe UI", 20, "bold")).pack(pady=(30, 0))
        tk.Label(self.sidebar, text="Management System", bg=SIDEBAR, fg="#cbd5e1",
                 font=("Segoe UI", 10)).pack(pady=(0, 30))
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="right", fill="both", expand=True)
        buttons = [
            ("Dashboard", Dashboard),
            ("Books", BooksView),
            ("Borrowers", BorrowersView),
            ("Issue Book", IssueBookView),
            ("Return Book", ReturnBookView),
            ("Reports", ReportsView),
        ]
        for text, view in buttons:
            tk.Button(self.sidebar, text=text, command=lambda v=view: self.show_view(v),
                      bg=SIDEBAR, fg="white", activebackground="#374151",
                      activeforeground="white", relief="flat", anchor="w",
                      font=("Segoe UI", 11), padx=25, pady=12, cursor="hand2").pack(fill="x")
        tk.Label(self.sidebar, text="Offline ", bg=SIDEBAR, fg="#94a3b8",
                 font=("Segoe UI", 9)).pack(side="bottom", pady=20)
        self.show_view(Dashboard)

    def show_view(self, view_class):
        for widget in self.content.winfo_children():
            widget.destroy()
        view_class(self.content, self).pack(fill="both", expand=True)

if __name__ == "__main__":
    LibraryApp().mainloop()
