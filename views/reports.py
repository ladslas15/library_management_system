import tkinter as tk
from tkinter import ttk
from database.db import get_connection
from datetime import date

class ReportsView(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg="#f4f6f8")
        tk.Label(self,text="Reports",bg="#f4f6f8",font=("Segoe UI",22,"bold")).pack(anchor="w",padx=25,pady=20)
        bar=tk.Frame(self,bg="#f4f6f8");bar.pack(fill="x",padx=25,pady=5)
        self.type=tk.StringVar(value="Overdue Books")
        cb=ttk.Combobox(bar,textvariable=self.type,state="readonly",values=["Overdue Books","Issued Books","All Transactions"],width=25);cb.pack(side="left")
        tk.Button(bar,text="Generate",command=self.load,bg="#2563eb",fg="white",relief="flat",padx=15,pady=6).pack(side="left",padx=8)
        self.tree=ttk.Treeview(self,columns=("id","book","borrower","issue","due","return","fine","status"),show="headings")
        for c,h in zip(self.tree["columns"],["ID","Book","Borrower","Issue","Due","Return","Fine","Status"]):self.tree.heading(c,text=h)
        self.tree.pack(fill="both",expand=True,padx=25,pady=15);self.load()
    def load(self):
        kind=self.type.get()
        with get_connection() as c:
            base="""SELECT t.id,b.title,br.name,t.issue_date,t.due_date,t.return_date,t.fine,t.status
                    FROM transactions t JOIN books b ON b.id=t.book_id JOIN borrowers br ON br.id=t.borrower_id"""
            if kind=="Overdue Books":base+=" WHERE t.status='Issued' AND t.due_date < ?";params=(date.today().isoformat(),)
            elif kind=="Issued Books":base+=" WHERE t.status='Issued'";params=()
            else:params=()
            rows=c.execute(base+" ORDER BY t.id DESC",params).fetchall()
        for i in self.tree.get_children():self.tree.delete(i)
        for r in rows:self.tree.insert("","end",values=tuple(r))
