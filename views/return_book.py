import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_connection, return_book
from utils.helpers import clear_tree

class ReturnBookView(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg="#f4f6f8");self.selected=None
        tk.Label(self,text="Return Book",bg="#f4f6f8",font=("Segoe UI",22,"bold")).pack(anchor="w",padx=25,pady=20)
        tk.Label(self,text="Select an active transaction and process the return.",bg="#f4f6f8",fg="#64748b").pack(anchor="w",padx=25,pady=(0,12))
        self.tree=ttk.Treeview(self,columns=("id","book","borrower","issue","due"),show="headings")
        for c,h in zip(("id","book","borrower","issue","due"),("ID","Book","Borrower","Issue Date","Due Date")):self.tree.heading(c,text=h)
        self.tree.pack(fill="both",expand=True,padx=25,pady=10);self.tree.bind("<<TreeviewSelect>>",self.select)
        tk.Button(self,text="Process Return",command=self.process,bg="#2563eb",fg="white",relief="flat",padx=20,pady=9).pack(anchor="w",padx=25,pady=15)
        self.load()
    def load(self):
        clear_tree(self.tree)
        with get_connection() as c:
            rows=c.execute("""SELECT t.id,b.title,br.name,t.issue_date,t.due_date FROM transactions t
                              JOIN books b ON b.id=t.book_id JOIN borrowers br ON br.id=t.borrower_id
                              WHERE t.status='Issued' ORDER BY t.due_date""").fetchall()
        for r in rows:self.tree.insert("","end",values=tuple(r))
    def select(self,_):
        s=self.tree.selection();self.selected=self.tree.item(s[0])["values"][0] if s else None
    def process(self):
        if not self.selected:return messagebox.showwarning("Select Transaction","Select a transaction first.")
        try:
            fine=return_book(self.selected);self.load()
            messagebox.showinfo("Return Complete",f"Book returned successfully.\nFine: UGX {fine:,.0f}")
        except Exception as e:messagebox.showerror("Error",str(e))
