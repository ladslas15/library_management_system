from tkinter import messagebox

def clear_tree(tree):
    for item in tree.get_children():
        tree.delete(item)

def valid_required(*values):
    return all(str(v).strip() for v in values)
