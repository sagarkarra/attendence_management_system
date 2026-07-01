# 📊 Attendance Management System Using Python Tkinter

A simple and user-friendly **Attendance Management System** developed using **Python** and **Tkinter**. This desktop application allows users to register students, mark daily attendance, and view attendance statistics such as total sessions, present count, absent count, and attendance percentage. All attendance records are stored locally in a JSON file for future use.

---

## 📌 Features

- ➕ Register new students
- 🗓️ Mark daily attendance
- ☑️ Mark students as Present or Absent
- 📊 View attendance summary in a table
- 📈 Automatically calculate attendance percentage
- 💾 Save attendance records using a JSON file
- 🔄 Automatically refresh attendance data
- 🖥️ Clean and easy-to-use graphical interface

---

## 🛠️ Technologies Used

- Python 3
- Tkinter
- ttk Widgets
- JSON
- Datetime Module
- Messagebox
- Object-Oriented Programming (OOP)

---

## 📂 Project Structure

```text
Attendance-Management-System/
│
├── main.py                    # Main application source code
├── gui_attendance_data.json   # Stores attendance records
└── README.md                  # Project documentation
```

---

## 📋 Requirements

- Python 3.x

Tkinter is included with Python, so no additional installation is required.

Verify Tkinter installation:

```bash
python -m tkinter
```

---

## 🚀 How to Run

1. Download or clone the repository.

2. Navigate to the project folder.

3. Run the application using:

```bash
python main.py
```

4. The Attendance Management System window will open.

---

## ⚙️ How the Application Works

### Step 1: Register Students

- Enter the student's name.
- Click the **Register** button.
- The student is added to the attendance database.

### Step 2: Mark Attendance

- Click **Mark Today's Attendance**.
- A new window opens displaying all registered students.
- Select **Present** or leave unchecked for **Absent**.
- Click **Submit Sheet Updates**.

### Step 3: View Attendance Report

The dashboard automatically displays:

- Student Name
- Total Sessions
- Present Count
- Absent Count
- Attendance Percentage

All records are automatically saved in the JSON database.

---

## 📊 Attendance Calculation

Attendance Percentage is calculated using the following formula:

```text
Attendance Percentage = (Present Count / Total Sessions) × 100
```

---

## 💾 Data Storage

The application stores all attendance records in **gui_attendance_data.json**.

Example:

```json
{
    "John": [
        {
            "date": "2026-07-01",
            "status": "Present"
        },
        {
            "date": "2026-07-02",
            "status": "Absent"
        }
    ]
}
```

---

## 🎯 Learning Outcomes

This project demonstrates:

- GUI development using Tkinter
- Object-Oriented Programming (OOP)
- Event-driven programming
- JSON file handling
- Data persistence
- Attendance management logic
- Working with Treeview widgets
- Popup windows using Toplevel
- Date handling using the Datetime module

---

## 🔮 Future Enhancements

- 📅 Monthly attendance reports
- 📊 Graphical attendance charts
- 🔍 Search student records
- ✏️ Edit student details
- 🗑️ Delete student records
- 📤 Export attendance reports to Excel or PDF
- 👨‍🏫 Subject-wise attendance tracking
- 🔐 Login authentication for administrators
- ☁️ Cloud database integration
- 📧 Email attendance reports

---

## ⚠️ Limitations

- Stores data locally using a JSON file.
- Does not support multiple user accounts.
- Attendance can be marked only once per session.
- No online database integration.
- No biometric or RFID attendance support.
