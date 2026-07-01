import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("650x450")
        
        # Initialize Database Tables
        self.init_db()
        
        # Create Tabbed Layout Structure
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_add = ttk.Frame(self.notebook)
        self.tab_mark = ttk.Frame(self.notebook)
        self.tab_report = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_add, text=" ➕ Add Student ")
        self.notebook.add(self.tab_mark, text=" ✔️ Mark Attendance ")
        self.notebook.add(self.tab_report, text=" 📊 View Report ")
        
        # Build individual screens
        self.setup_add_tab()
        self.setup_mark_tab()
        self.setup_report_tab()

    # =========================================================================
    # 🗄️ DATA STORAGE & TABLES (Backend Setup)
    # =========================================================================
    def init_db(self):
        conn = sqlite3.connect("attendance_sys.db")
        cursor = conn.cursor()
        # Students entity table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        # Attendance tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(student_id)
            )
        """)
        conn.commit()
        conn.close()

    # =========================================================================
    # 👥 FEATURE 1: Add Student Names
    # =========================================================================
    def setup_add_tab(self):
        frame = ttk.LabelFrame(self.tab_add, text=" Register New Student Profile ")
        frame.pack(padx=20, pady=40, fill="both", expand=True)
        
        ttk.Label(frame, text="Full Name:", font=("Arial", 11)).pack(pady=10)
        self.name_entry = ttk.Entry(frame, width=30, font=("Arial", 11))
        self.name_entry.pack(pady=5)
        
        btn_submit = ttk.Button(frame, text="Add Student Data", command=self.save_student)
        btn_submit.pack(pady=20)

    def save_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Student name field cannot be empty!")
            return
            
        conn = sqlite3.connect("attendance_sys.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"'{name}' successfully added to data storage!")
        self.name_entry.delete(0, tk.END)
        self.refresh_mark_list() # Synchronize list state

    # =========================================================================
    # 📝 FEATURE 2: Mark Attendance Table Records
    # =========================================================================
    def setup_mark_tab(self):
        self.today_str = date.today().strftime("%Y-%m-%d")
        
        lbl_date = ttk.Label(self.tab_mark, text=f"Date: {self.today_str}", font=("Arial", 12, "bold"))
        lbl_date.pack(pady=10)
        
        # Container to house active student listing
        self.scroll_frame = ttk.Frame(self.tab_mark)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.canvas = tk.Canvas(self.scroll_frame, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.list_inner_frame = ttk.Frame(self.canvas)
        
        self.list_inner_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.list_inner_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Submit execution button
        btn_save = ttk.Button(self.tab_mark, text="Submit Attendance Ledger", command=self.submit_attendance)
        btn_save.pack(pady=15)
        
        self.refresh_mark_list()

    def refresh_mark_list(self):
        # Clear prior entries
        for widget in self.list_inner_frame.winfo_children():
            widget.destroy()
            
        conn = sqlite3.connect("attendance_sys.db")
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name FROM students")
        self.student_records = cursor.fetchall()
        conn.close()
        
        self.status_variables = {} # Trace radio selection bindings dynamically
        
        if not self.student_records:
            ttk.Label(self.list_inner_frame, text="No students added yet. Access the first tab.", font=("Arial", 10, "italic")).pack(pady=20)
            return

        for index, (s_id, name) in enumerate(self.student_records):
            row_frame = ttk.Frame(self.list_inner_frame, padding=5)
            row_frame.pack(fill="x", expand=True)
            
            ttk.Label(row_frame, text=f"{name} (ID: {s_id})", width=30, anchor="w").pack(side="left", padx=10)
            
            # Tracking variable default assignment: 'Present'
            var = tk.StringVar(value="Present")
            self.status_variables[s_id] = var
            
            ttk.Radiobutton(row_frame, text="P", variable=var, value="Present").pack(side="left", padx=5)
            ttk.Radiobutton(row_frame, text="A", variable=var, value="Absent").pack(side="left", padx=5)

    def submit_attendance(self):
        if not self.student_records:
            messagebox.showwarning("Warning", "Data log sequence aborted: No student profiles available.")
            return
            
        conn = sqlite3.connect("attendance_sys.db")
        cursor = conn.cursor()
        
        # Remove pre-existing overlaps for clean day overwrite validation logic
        cursor.execute("DELETE FROM attendance WHERE date = ?", (self.today_str,))
        
        for s_id, var in self.status_variables.items():
            status = var.get()
            cursor.execute(
                "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                (s_id, self.today_str, status)
            )
            
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Attendance for {self.today_str} successfully committed!")
        self.populate_report_table() # Update downstream report engine

    # =========================================================================
    # 📊 FEATURE 3: View Compiled Tables Report
    # =========================================================================
    def setup_report_tab(self):
        btn_refresh = ttk.Button(self.tab_report, text="🔄 Refresh Database Report", command=self.populate_report_table)
        btn_refresh.pack(pady=10)
        
        # Interactive Treeview grid implementation representing physical tables
        columns = ("date", "id", "name", "status")
        self.tree = ttk.Treeview(self.tab_report, columns=columns, show="headings")
        
        self.tree.heading("date", text="Log Date")
        self.tree.heading("id", text="Student ID")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("status", text="Attendance Status")
        
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("name", width=220, anchor="center")  # Modified layout column anchor to center alignment
        self.tree.column("status", width=120, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=15, pady=5)
        self.populate_report_table()

    def populate_report_table(self):
        # Flush existing visual rows
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = sqlite3.connect("attendance_sys.db")
        cursor = conn.cursor()
        
        # Relational JOIN logic mapping ID targets back to user names
        query = """
            SELECT a.date, s.student_id, s.name, a.status 
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            ORDER BY a.date DESC, s.name ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            self.tree.insert("", tk.END, values=row)

# Run Environment Core Launcher
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
