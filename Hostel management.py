#hostel management system

import tkinter as tk
#from tkinter import *
from tkinter import messagebox, simpledialog
import sqlite3

class login:

    def __init__(self,window):
        self.window = window
        self.window.title("Admin login")
        self.window.config(bg="#0BA68A")
        self.window.geometry("700x800")

        tk.Label(window, text="Admin Login", font=("Times New Roman", 20), bg="#0BA68A", fg="white").pack(pady=20)

        tk.Label(window, text="Username:", bg="#0BA68A", fg="white").pack()
        self.username_entry = tk.Entry(window)
        self.username_entry.pack(pady=5)

        tk.Label(window, text="Password:", bg="#0BA68A", fg="white").pack()
        self.password_entry = tk.Entry(window, show="*")  # Hides password
        self.password_entry.pack(pady=5)

        tk.Button(window, text="Login", bg="white", command=self.check_login).pack(pady=10)

    def check_login(self):
            """Checks if login credentials are correct."""
            username = self.username_entry.get()
            password = self.password_entry.get()

            if username == "bakali" and password == "cibah1234":  # Change as needed
                self.window.destroy()  # Close login window
                main_window = tk.Tk()
                HostelManagementSystem(main_window)  # Open main system
                main_window.mainloop()
            else:
                messagebox.showerror("Error", "Invalid Username or Password")


class HostelManagementSystem:
    """Main hostel management interface with SQLite integration."""

    def __init__(self, window):
        self.window = window
        self.window.title("Hostel Management System")
        self.window.config(bg="#0BA68A")
        self.window.geometry("700x800")

        # List of all room numbers
        self.all_rooms = [str(i) for i in range(1, 51)]

        # Create database and table
        self.conn = sqlite3.connect("hostel.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Title
        self.label = tk.Label(window, text="Hostel Management System", fg="white", bg="#0BA68A",
                              font=("Times New Roman", 20))
        self.label.pack(pady=20)



        #Student Name
        tk.Label(self.window, text="Student Name:", bg="#0BA68A", fg="white").pack()
        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack(pady=5)

        # Room Number
        tk.Label(self.window, text="Room Number:", bg="#0BA68A", fg="white").pack()
        self.room_entry = tk.Entry(self.window)
        self.room_entry.pack(pady=5)

        # Buttons
        self.add_student_button = tk.Button(window, text="Add Student", bg="#0BA68A", command=self.add_student)
        self.add_student_button.pack(pady=10)

        self.view_students_button = tk.Button(window, text="View Students", bg="#0BA68A", command=self.view_students)
        self.view_students_button.pack(pady=10)

        self.available_rooms_button = tk.Button(window, text="Show Available Rooms", bg="#0BA68A",command=self.show_available_rooms)
        self.available_rooms_button.pack(pady=10)

        self.update_button = tk.Button(window, text="Update Student Info", bg="#0BA68A", command=self.update_student)
        self.update_button.pack(pady=10)

        # Add Student Form Frame (initially hidden)
        self.add_student_frame = tk.Frame(self.window, bg="#0BA68A")

        tk.Label(self.add_student_frame, text="Student Name:", bg="#0BA68A", fg="white").pack()
        self.name_entry = tk.Entry(self.add_student_frame)
        #self.name_entry.pack(pady=5)

        tk.Label(self.add_student_frame, text="Room Number:", bg="#0BA68A", fg="white").pack()
        self.room_entry = tk.Entry(self.add_student_frame)
        #self.room_entry.pack(pady=5)

        self.submit_student_button = tk.Button(self.add_student_frame, text="Submit", bg="#0BA68A",
                                               command=self.add_student)


    def show_add_student_form(self):
        self.add_student_frame.pack(pady=10)  # Only shows the form when "Add Student" is clicked
        self.submit_student_button.pack(pady=10)

    def create_table(self):
        #Creates the students table if it doesn't exist.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                room_number TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_student(self):
        """Adds a new student to the database from input fields."""
        room = self.room_entry.get().strip()
        name = self.name_entry.get().strip()

        print("Button clicked!")  # Debugging

        if name and room:
            try:
                self.cursor.execute("INSERT INTO students (name, room_number) VALUES (?, ?)", (name, room))
                self.conn.commit()
                messagebox.showinfo("Success", f"Student {name} added to Room {room}")
                print(f"Added: {name}, Room: {room}")  # Debugging

                # Clear fields after adding student
                self.name_entry.delete(0, tk.END)
                self.room_entry.delete(0, tk.END)

            except sqlite3.Error as e:
                print("Database Insert Error:", e)
                messagebox.showerror("Database Error", "Failed to add student.")
        else:
            messagebox.showwarning("Input Error", "Please enter both name and room number")
            print("Empty fields!")  # Debugging

    def view_students(self):
        """Retrieves and displays all students from the database."""
        self.cursor.execute("SELECT name, room_number FROM students")
        students = self.cursor.fetchall()

        if not students:
            messagebox.showinfo("Students", "No students added yet.")
        else:
            student_list = "\n".join([f"{s[0]} - Room {s[1]}" for s in students])
            messagebox.showinfo("Students List", student_list)

    def show_available_rooms(self):
        # Get rooms already taken
        self.cursor.execute("SELECT room_number FROM students")
        occupied = [row[0] for row in self.cursor.fetchall()]

        # Compare with all rooms
        available = [room for room in self.all_rooms if room not in occupied]

        if available:
            messagebox.showinfo("Available Rooms", "\n".join(available))
        else:
            messagebox.showinfo("Available Rooms", "No rooms available.")

    def update_student(self):
        original_name = self.update_name_entry.get().strip()
        new_name = self.new_name_entry.get().strip()
        new_room = self.new_room_entry.get().strip()

        if not original_name:
            messagebox.showwarning("Input Error", "Please enter the student's current name.")
            return

        if not new_room:
            messagebox.showwarning("Input Error", "Please enter a new room number.")
            return

        # Validate new room
        if not new_room.isdigit() or int(new_room) not in self.valid_room_range:
            messagebox.showerror("Invalid Room", "Room number must be between 1 and 50.")
            return

        # Check if room is already taken by someone else
        self.cursor.execute("SELECT * FROM students WHERE room_number = ?", (new_room,))
        existing = self.cursor.fetchone()
        if existing and existing[1] != original_name:
            messagebox.showerror("Room Occupied", f"Room {new_room} is already taken.")
            return

        # Find the student by name
        self.cursor.execute("SELECT * FROM students WHERE name = ?", (original_name,))
        student = self.cursor.fetchone()

        if not student:
            messagebox.showerror("Not Found", "Student not found.")
            return

        # Use original name if no new name provided
        if not new_name:
            new_name = original_name

        # Update in DB
        try:
            self.cursor.execute("UPDATE students SET name = ?, room_number = ? WHERE name = ?",
                                (new_name, new_room, original_name))
            self.conn.commit()
            messagebox.showinfo("Success", f"{original_name} updated to {new_name}, Room {new_room}")

            # Clear fields
            self.update_name_entry.delete(0, tk.END)
            self.new_name_entry.delete(0, tk.END)
            self.new_room_entry.delete(0, tk.END)
            self.update_frame.pack_forget()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update: {e}")

    def __del__(self):
        """Closes the database connection when the app is closed."""



if __name__ == "__main__":
    window = tk.Tk()
    login(window)
    #app = HostelManagementSystem(window)
    window.mainloop()
