import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_connection
from utils.helpers import clear_tree, valid_required

class BooksView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f4f6f8")
        self.selected_id = None
        tk.Label(self, text="Book Management", bg="#f4f6f8", font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=25, pady=20)
        form = tk.Frame(self, bg="white", padx=15, pady=15); form.pack(fill="x", padx=25)
        self.vars = {k: tk.StringVar() for k in ["title","author","publisher","year","copies"]}
        labels = [("title","Title"),("author","Author"),("publisher","Publisher"),("year","Year"),("copies","Copies")]
        for i,(key,label) in enumerate(labels):
            tk.Label(form,text=label,bg="white").grid(row=0,column=i*2,sticky="w",padx=5)
            tk.Entry(form,textvariable=self.vars[key],width=20).grid(row=0,column=i*2+1,padx=5)
        tk.Button(form,text="Save Book",command=self.save,bg="#2563eb",fg="white",relief="flat",padx=12,pady=6).grid(row=1,column=1,pady=12)
        tk.Button(form,text="Update Selected",command=self.update,relief="flat",padx=12,pady=6).grid(row=1,column=3)
        tk.Button(form,text="Delete Selected",command=self.delete,relief="flat",padx=12,pady=6).grid(row=1,column=5)
        tk.Button(form,text="Clear",command=self.clear,relief="flat",padx=12,pady=6).grid(row=1,column=7)
        search = tk.Frame(self,bg="#f4f6f8"); search.pack(fill="x",padx=25,pady=12)
        self.q=tk.StringVar(); tk.Entry(search,textvariable=self.q,width=35).pack(side="left")
        tk.Button(search,text="Search",command=self.load,relief="flat",padx=12).pack(side="left",padx=5)
        tk.Button(search,text="Show All",command=lambda:self.load(""),relief="flat",padx=12).pack(side="left")
        cols=("id","title","author","publisher","year","copies","available")
        self.tree=ttk.Treeview(self,columns=cols,show="headings")
        heads=["ID","Title","Author","Publisher","Year","Copies","Available"]
        for c,h in zip(cols,heads): self.tree.heading(c,text=h)
        self.tree.column("id",width=50); self.tree.pack(fill="both",expand=True,padx=25,pady=(0,25))
        self.tree.bind("<<TreeviewSelect>>",self.select)
        self.load("")

    def load(self, q=None):
        q=self.q.get() if q is None else q
        clear_tree(self.tree)
        with get_connection() as c:
            rows=c.execute("""SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR publisher LIKE ?
                              ORDER BY id DESC""",(f"%{q}%",f"%{q}%",f"%{q}%")).fetchall()
        for r in rows:self.tree.insert("", "end", values=(r["id"],r["title"],r["author"],r["publisher"],r["year"],r["copies"],r["available_copies"]))

    def select(self,_):
        s=self.tree.selection()
        if not s:return
        v=self.tree.item(s[0])["values"]; self.selected_id=v[0]
        for key,val in zip(["title","author","publisher","year","copies"],v[1:6]): self.vars[key].set(val)

    def save(self):
        try:
            if not valid_required(self.vars["title"].get(),self.vars["author"].get(),self.vars["copies"].get()): raise ValueError("Title, author and copies are required.")
            copies=int(self.vars["copies"].get()); 
            if copies<1: raise ValueError("Copies must be at least 1.")
            year=self.vars["year"].get(); year=int(year) if year else None
            with get_connection() as c:c.execute("INSERT INTO books(title,author,publisher,year,copies,available_copies) VALUES(?,?,?,?,?,?)",(self.vars["title"].get().strip(),self.vars["author"].get().strip(),self.vars["publisher"].get().strip(),year,copies,copies))
            self.clear(); self.load(""); messagebox.showinfo("Success","Book added successfully.")
        except Exception as e: messagebox.showerror("Error",str(e))
    def update(self):
        if not self.selected_id:return messagebox.showwarning("Select Book","Select a book first.")
        try:
            copies=int(self.vars["copies"].get())
            with get_connection() as c:
                old=c.execute("SELECT copies,available_copies FROM books WHERE id=?",(self.selected_id,)).fetchone()
                borrowed=old["copies"]-old["available_copies"]
                if copies<borrowed: raise ValueError(f"Copies cannot be below {borrowed} currently borrowed.")
                available=copies-borrowed
                c.execute("""UPDATE books SET title=?,author=?,publisher=?,year=?,copies=?,available_copies=? WHERE id=?""",
                          (self.vars["title"].get(),self.vars["author"].get(),self.vars["publisher"].get(),int(self.vars["year"].get()) if self.vars["year"].get() else None,copies,available,self.selected_id))
            self.load(""); self.clear(); messagebox.showinfo("Success","Book updated.")
        except Exception as e:messagebox.showerror("Error",str(e))
    def delete(self):
        if not self.selected_id:return messagebox.showwarning("Select Book","Select a book first.")
        if not messagebox.askyesno("Confirm","Delete selected book?"):return
        try:
            with get_connection() as c:c.execute("DELETE FROM books WHERE id=?",(self.selected_id,))
            self.load("");self.clear()
        except Exception as e:messagebox.showerror("Error","Cannot delete a book with transaction history.")
    def clear(self):
        self.selected_id=None
        for v in self.vars.values():v.set("")
