import tkinter as tk
from tkinter import ttk, messagebox
import cx_Oracle

# Oracle connection settings
host = "localhost"
port = 1521
service_name = "XEPDB1"
username = "system"
password = "123"

# Build DSN (Data Source Name)
dsn = cx_Oracle.makedsn(host, port, service_name=service_name)

# Tkinter UI setup
root = tk.Tk()
root.title("Oracle Employees Viewer")

frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Define columns matching your table
columns = ("ID", "First Name", "Last Name", "Department ID")
tree = ttk.Treeview(frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill=tk.BOTH, expand=True)

# --- Load Data Function ---
def load_data():
    try:
        conn = cx_Oracle.connect(username, password, dsn)
        cursor = conn.cursor()

        # Clear existing rows in the Treeview
        for row in tree.get_children():
            tree.delete(row)

        cursor.execute("SELECT employee_id, first_name, last_name, department_id FROM employees")
        for row in cursor:
            tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

# --- Truncate Table Function ---
def truncate_table():
    answer = messagebox.askyesno("Confirm", "Are you sure you want to truncate the employees table?")
    if answer:
        try:
            conn = cx_Oracle.connect(username, password, dsn)
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE employees")
            conn.commit()  # optional, TRUNCATE auto-commits
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Employees table truncated successfully!")
            load_data()  # Refresh Treeview
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Buttons
btn_load = ttk.Button(root, text="Load Employees", command=load_data)
btn_load.pack(pady=5)

btn_truncate = ttk.Button(root, text="Truncate Table", command=truncate_table)
btn_truncate.pack(pady=5)

root.mainloop()
