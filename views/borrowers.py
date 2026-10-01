import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_connection
from utils.helpers import clear_tree

class BorrowersView(tk.Frame):
    def __init__(self,parent,app):
        super().__init__(parent,bg="#f4f6f8"); self.selected_id=None
        tk.Label(self,text="Borrower Management",bg="#f4f6f8",font=("Segoe UI",22,"bold")).pack(anchor="w",padx=25,pady=20)
        form=tk.Frame(self,bg="white",padx=15,pady=15);form.pack(fill="x",padx=25)
        self.vars={k:tk.StringVar() for k in ["name","contact","email"]}
        for i,(k,l) in enumerate([("name","Name"),("contact","Contact"),("email","Email")]):
            tk.Label(form,text=l,bg="white").grid(row=0,column=i*2,sticky="w",padx=5);tk.Entry(form,textvariable=self.vars[k],width=28).grid(row=0,column=i*2+1,padx=5)
        for i,(t,cmd) in enumerate([("Save",self.save),("Update",self.update),("Delete",self.delete),("Clear",self.clear)]):
            tk.Button(form,text=t,command=cmd,relief="flat",padx=15,pady=6,bg="#2563eb" if t=="Save" else "#e5e7eb",fg="white" if t=="Save" else "#111827").grid(row=1,column=i*2+1,pady=12)
        self.q=tk.StringVar();bar=tk.Frame(self,bg="#f4f6f8");bar.pack(fill="x",padx=25,pady=12);tk.Entry(bar,textvariable=self.q,width=35).pack(side="left");tk.Button(bar,text="Search",command=self.load,relief="flat").pack(side="left",padx=5)
        self.tree=ttk.Treeview(self,columns=("id","name","contact","email"),show="headings")
        for c,h in zip(("id","name","contact","email"),("ID","Name","Contact","Email")):self.tree.heading(c,text=h)
        self.tree.pack(fill="both",expand=True,padx=25,pady=(0,25));self.tree.bind("<<TreeviewSelect>>",self.select);self.load()
    def load(self):
        q=self.q.get();clear_tree(self.tree)
        with get_connection() as c:rows=c.execute("SELECT * FROM borrowers WHERE name LIKE ? OR contact LIKE ? OR email LIKE ? ORDER BY id DESC",(f"%{q}%",)*3).fetchall()
        for r in rows:self.tree.insert("","end",values=(r["id"],r["name"],r["contact"],r["email"]))
    def select(self,_):
        s=self.tree.selection()
        if s:
            v=self.tree.item(s[0])["values"];self.selected_id=v[0]
            for k,val in zip(self.vars,v[1:]):self.vars[k].set(val)
    def save(self):
        if not self.vars["name"].get().strip():return messagebox.showwarning("Required","Name is required.")
        with get_connection() as c:c.execute("INSERT INTO borrowers(name,contact,email) VALUES(?,?,?)",tuple(v.get().strip() for v in self.vars.values()))
        self.clear();self.load()
    def update(self):
        if not self.selected_id:return
        with get_connection() as c:c.execute("UPDATE borrowers SET name=?,contact=?,email=? WHERE id=?",(self.vars["name"].get(),self.vars["contact"].get(),self.vars["email"].get(),self.selected_id))
        self.clear();self.load()
    def delete(self):
        if not self.selected_id:return
        try:
            with get_connection() as c:c.execute("DELETE FROM borrowers WHERE id=?",(self.selected_id,))
            self.clear();self.load()
        except Exception as e:messagebox.showerror("Error","Cannot delete a borrower with transaction history.")
    def clear(self):
        self.selected_id=None
        for v in self.vars.values():v.set("")
