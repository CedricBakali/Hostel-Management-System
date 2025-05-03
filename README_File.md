# Hostel Management System (Python Tkinter + SQLite)

This is a desktop-based Hostel Management System built using Python's Tkinter GUI library and SQLite for database management. It allows administrators to manage student records, room assignments, and fee payments efficiently through a user-friendly interface.

## 🚀 Features

- Admin Login: Secure login screen for admin access.
- Add Student: Register a new student with name, age, course, and room number.
- View Students: Display all student records including room numbers and fees paid.
- Update Student Info: Change student name and/or room number.
- Delete Student: Remove a student record permanently.
- Available Rooms: View a list of unassigned hostel rooms.this system / hostel accomodet single student per room
- Fee Payment: Record and update student payment information.
- Persistent Storage: Uses SQLite for local data storage.

## 🛠️ Technologies Used

- Python 3.x
- Tkinter - For building GUI applications
- SQLite3 - For storing data locally


## 🧰 How to Run the Project

	1. Make sure Python 3.x is installed on your system.
	2. Clone or download this repository.
	3. Run the main script:

bash
python main.py

Username: bakali
Password: cibah1234


🧑‍💼 Admin Operations
	After successful login, the admin can:

	Add a new student by entering name, room number, course, and age.

	View a table of all students including ID, name, age, course, room, and payment status.

	Update existing student information.

	Delete student records.

	See which rooms are still available.

	Record and update fee payments.

💡 Possible Future Enhancements
	Input validation improvements (e.g., regex checks for name and course).

	Room capacity management.

	Fee reports and due tracking.

	Password encryption and user roles.

	Export student data to CSV or PDF.

📌 Notes
	The system currently supports rooms numbered from 1 to 50.

	Student names must be unique.

Fees are updated incrementally per student.

