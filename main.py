import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "gui_attendance_data.json"

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management System")
        self.root.geometry("750x600")
        self.root.config(bg="#f4f6f9")
        
        # Load backend storage
        self.student_records = self.load_data()
        
        # Initialize UI layout configurations
        self.create_styles()
        self.build_ui()
        self.refresh_table()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.student_records, file, indent=4)

    def create_styles(self):
        """Sets custom design tokens for a cleaner interface styling."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#f4f6f9", font=("Helvetica", 10))
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), background="#f4f6f9")
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5)
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#e0e0e0")

    def build_ui(self):
        # --- TITLE BAR ---
        title = ttk.Label(self.root, text="📊 Attendance Management System Dashboard", style="Header.TLabel")
        title.pack(pady=15)

        # --- UPPER SECTION: CONTROLS ---
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill="x", padx=20, pady=5)

        # Left Control side: Registering new student names
        add_frame = ttk.LabelFrame(control_frame, text=" Add New Student ", padding=10)
        add_frame.pack(side="left", fill="both", expand=True, padx=5)

        ttk.Label(add_frame, text="Student Name:").pack(side="left", padx=5)
        self.name_entry = ttk.Entry(add_frame, font=("Helvetica", 10))
        self.name_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        add_btn = ttk.Button(add_frame, text="Register", command=self.add_student)
        add_btn.pack(side="left", padx=5)

        # Right Control side: Action Panel triggers
        action_frame = ttk.LabelFrame(control_frame, text=" Quick Actions ", padding=10)
        action_frame.pack(side="right", fill="both", padx=5)

        mark_btn = ttk.Button(action_frame, text="🗓️ Mark Today's Attendance", command=self.open_attendance_window)
        mark_btn.pack(side="left", padx=5)

        # --- LOWER SECTION: DATA GRID TABLE ---
        table_frame = ttk.LabelFrame(self.root, text=" Attendance Database Records Summary ", padding=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Configuring standard columns for structural grid previewing 
        columns = ("name", "total_sessions", "presents", "absents", "percentage")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("name", text="Student Name")
        self.tree.heading("total_sessions", text="Total Sessions")
        self.tree.heading("presents", text="Present Count")
        self.tree.heading("absents", text="Absent Count")
        self.tree.heading("percentage", text="Attendance %")

        self.tree.column("name", width=200, anchor="w")
        self.tree.column("total_sessions", width=110, anchor="center")
        self.tree.column("presents", width=110, anchor="center")
        self.tree.column("absents", width=110, anchor="center")
        self.tree.column("percentage", width=110, anchor="center")

        # Vertical Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_student(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Name field input box cannot be empty!")
            return
        
        if name in self.student_records:
            messagebox.showwarning("Warning", f"Student '{name}' is already registered.")
        else:
            self.student_records[name] = []
            self.save_data()
            self.name_entry.delete(0, tk.END)
            self.refresh_table()
            messagebox.showinfo("Success", f"'{name}' added successfully to tracking index.")

    def refresh_table(self):
        """Clears old analytical rows and recalculates state from storage."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for name, history in self.student_records.items():
            total = len(history)
            presents = sum(1 for item in history if item["status"] == "Present")
            absents = total - presents
            pct = f"{(presents / total) * 100:.1f}%" if total > 0 else "N/A"
            
            self.tree.insert("", "end", values=(name, total, presents, absents, pct))

    def open_attendance_window(self):
        """Feature 2 Overlay: Instantiates temporary popup checking profile lists."""
        if not self.student_records:
            messagebox.showwarning("Empty System", "Please register students prior to creating active logs.")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        
        # Window popup definition
        win = tk.Toplevel(self.root)
        win.title(f"Attendance Tracking Panel: {today}")
        win.geometry("400x450")
        win.grab_set()  # Focus interaction lock helper

        ttk.Label(win, text=f"Mark Session Attendance For: {today}", font=("Helvetica", 11, "bold")).pack(pady=10)

        # Create a container frame with an internal scrollable canvas for bulk students
        canvas_container = ttk.Frame(win)
        canvas_container.pack(fill="both", expand=True, padx=15, pady=5)

        canvas = tk.Canvas(canvas_container, highlightthickness=0)
        scrollable_frame = ttk.Frame(canvas)
        v_scroll = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        
        canvas.configure(yscrollcommand=v_scroll.set)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")

        # Dictionary tracking boolean variables mapped to user records
        checkbox_vars = {}
        
        for name in self.student_records:
            row = ttk.Frame(scrollable_frame, padding=5)
            row.pack(fill="x", expand=True)
            
            ttk.Label(row, text=name, width=25, anchor="w").pack(side="left")
            
            # Use BooleanVar: True means Present, False means Absent
            var = tk.BooleanVar(value=True)
            checkbox_vars[name] = var
            
            cb = ttk.Checkbutton(row, text="Present", variable=var)
            cb.pack(side="right")

        def submit_logs():
            for name, status_var in checkbox_vars.items():
                status_str = "Present" if status_var.get() else "Absent"
                self.student_records[name].append({"date": today, "status": status_str})
            
            self.save_data()
            self.refresh_table()
            win.destroy()
            messagebox.showinfo("Saved", f"Attendance roster submitted for session tracking date: {today}")

        # Static execution processing button
        ttk.Button(win, text="Submit Sheet Updates", command=submit_logs).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
