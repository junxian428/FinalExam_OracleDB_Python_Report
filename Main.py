import tkinter as tk
from tkinter import messagebox, ttk
import cx_Oracle

# --- Oracle DB Connection Info ---
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XEPDB1")
conn = cx_Oracle.connect(user="system", password="123", dsn=dsn)
cursor = conn.cursor()

# --- Insert Staff Function ---
def insert_staff():
    try:
        cursor.execute("""
            INSERT INTO ProjectAlpha_Staff (EmployeeID, EmployeeName, Department, JoinDate, Salary)
            VALUES (:1, :2, :3, TO_DATE(:4, 'DD-MON-YYYY'), :5)
        """, (
            entry_id.get(),
            entry_name.get(),
            entry_department.get(),
            entry_joindate.get(),
            float(entry_salary.get())
        ))
        conn.commit()
        messagebox.showinfo("Success", "Staff added successfully!")
        load_staff()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Load Staff Into Treeview ---
def load_staff():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM ProjectAlpha_Staff ORDER BY EmployeeID")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

# --- GUI Setup ---
root = tk.Tk()
root.title("ProjectAlpha Staff Form")
root.geometry("800x450")

# --- Input Frame ---
frame = tk.LabelFrame(root, text="Add New Staff")
frame.pack(fill="x", padx=10, pady=5)

tk.Label(frame, text="Employee ID").grid(row=0, column=0)
entry_id = tk.Entry(frame)
entry_id.grid(row=0, column=1)

tk.Label(frame, text="Employee Name").grid(row=0, column=2)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=3)

tk.Label(frame, text="Department").grid(row=1, column=0)
entry_department = tk.Entry(frame)
entry_department.grid(row=1, column=1)

tk.Label(frame, text="Join Date (DD-MON-YYYY)").grid(row=1, column=2)
entry_joindate = tk.Entry(frame)
entry_joindate.grid(row=1, column=3)

tk.Label(frame, text="Salary").grid(row=2, column=0)
entry_salary = tk.Entry(frame)
entry_salary.grid(row=2, column=1)

tk.Button(frame, text="Add Staff", command=insert_staff).grid(row=2, column=3, pady=5)

# --- Treeview for Displaying Staff ---
tree = ttk.Treeview(root, columns=("EmployeeID", "EmployeeName", "Department", "JoinDate", "Salary"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True, padx=10, pady=10)

# --- Load Staff Initially ---
load_staff()

root.mainloop()
