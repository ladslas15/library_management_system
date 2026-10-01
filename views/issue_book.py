import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_connection, issue_book

class IssueBookView(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg="#f4f6f8")
        tk.Label(self,text="Issue Book",bg="#f4f6f8",font=("Segoe UI",22,"bold")).pack(anchor="w",padx=25,pady=25)
        form=tk.Frame(self,bg="white",padx=25,pady=25);form.pack(fill="x",padx=25)
        tk.Label(form,text="Book",bg="white").grid(row=0,column=0,padx=8,pady=8,sticky="w")
        tk.Label(form,text="Borrower",bg="white").grid(row=1,column=0,padx=8,pady=8,sticky="w")
        tk.Label(form,text="Loan Period (days)",bg="white").grid(row=2,column=0,padx=8,pady=8,sticky="w")
        self.book=ttk.Combobox(form,width=60,state="readonly");self.borrower=ttk.Combobox(form,width=60,state="readonly");self.days=tk.StringVar(value="14")
        self.book.grid(row=0,column=1,padx=8);self.borrower.grid(row=1,column=1,padx=8);tk.Entry(form,textvariable=self.days,width=10).grid(row=2,column=1,sticky="w",padx=8)
        tk.Button(form,text="Issue Book",command=self.issue,bg="#2563eb",fg="white",relief="flat",padx=18,pady=8).grid(row=3,column=1,sticky="w",pady=15)
        self.books=[];self.borrowers=[];self.load()
    def load(self):
        with get_connection() as c:
            self.books=c.execute("SELECT id,title,author,available_copies FROM books WHERE available_copies>0 ORDER BY title").fetchall()
            self.borrowers=c.execute("SELECT id,name FROM borrowers ORDER BY name").fetchall()
        self.book["values"]=[f'{r["id"]} - {r["title"]} ({r["available_copies"]} available)' for r in self.books]
        self.borrower["values"]=[f'{r["id"]} - {r["name"]}' for r in self.borrowers]
        if self.books:self.book.current(0)
        if self.borrowers:self.borrower.current(0)
    def issue(self):
        try:
            if not self.books or not self.borrowers:raise ValueError("You need at least one available book and one borrower.")
            days=int(self.days.get()); 
            if days<1:raise ValueError("Loan period must be at least 1 day.")
            issue_book(self.books[self.book.current()]["id"],self.borrowers[self.borrower.current()]["id"],days)
            messagebox.showinfo("Success","Book issued successfully.");self.load()
        except Exception as e:messagebox.showerror("Error",str(e))
