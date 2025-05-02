import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import logging
from datetime import date
from tkinter import ttk

class login:

    def __init__(self, window):
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
        try:
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
            
        except Exception as e:
            logging.error("Login failed: %s", e)
            messagebox.showerror("Login Error", "Unexpected error during login.")    


class HostelManagementSystem:
    """Main hostel management interface with SQLite integration."""

    def __init__(self, window):
        self.window = window
        self.window.title("Hostel Management System")
        self.window.config(bg="#0BA68A")
        self.window.geometry("700x800")
        
        

        
       

        #variables
        # List of all room numbers
        self.all_rooms = [str(i) for i in range(1, 51)]
        # Valid room range
        self.valid_room_range = range(1, 51)
        self.age_var = tk.StringVar()
        self.course_var = tk.StringVar()
        
        self.fees_name_entry = None
        self.payment_entry = None
        self.fees_frame = None
        




        # Create database and table
        self.conn = sqlite3.connect("hostel.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Title
        self.label = tk.Label(window, text="Hostel Management System", fg="white", bg="#0BA68A",font=("Times New Roman", 20))
        self.label.pack(pady=20)

        # Student Name
       # tk.Label(self.window, text="Student Name:", bg="#0BA68A", fg="white").pack()
        #self.name_entry = tk.Entry(self.window)
        #self.name_entry.pack(pady=5)

        # Room Number
        #tk.Label(self.window, text="Room Number:", bg="#0BA68A", fg="white").pack()
        #self.room_entry = tk.Entry(self.window)
        #self.room_entry.pack(pady=5)

        # Buttons
        self.add_student_button = tk.Button(window, text="Add Student", fg="white",bg="#0BA68A", command=self.show_add_student_form)
        self.add_student_button.pack(pady=10)

        self.view_students_button = tk.Button(window, text="View Students", fg="white",bg="#0BA68A", command=self.view_students)
        self.view_students_button.pack(pady=10)

        self.available_rooms_button = tk.Button(window, text="Show Available Rooms",fg="white", bg="#0BA68A", command=self.show_available_rooms)
        self.available_rooms_button.pack(pady=10)

        self.update_button = tk.Button(window, text="Update Student Info", fg="white",bg="#0BA68A", command=self.show_update_form)
        self.update_button.pack(pady=10)
        
        self.fees_button = tk.Button(window, text="Fees Payment", fg="white",bg="#0BA68A",command=self.fees_payment)
        self.fees_button.pack(padx=10)

        self.delete_button = tk.Button(window, text="Delete Student",fg="white", bg="#0BA68A", command=self.show_delete_form)
        self.delete_button.pack(pady=10)
        
        

        # Add Student Form Frame (initially hidden)
        self.add_student_frame = tk.Frame(self.window, bg="#0BA68A")

        """tk.Label(self.add_student_frame, text="Student Name:", bg="#0BA68A", fg="white").pack()
        self.name_entry_add = tk.Entry(window)

        tk.Label(self.add_student_frame, text="Room Number:", bg="#0BA68A", fg="white").pack()
        self.name_entry_add = tk.Entry(window)"""

        self.name_entry = None
        self.room_entry = None
        self.name_label = None
        self.room_label = None

        #self.submit_student_button = tk.Button(self.add_student_frame, text="Submit", bg="#0BA68A", command=self.add_student)

        # Update Student Form (initially hidden)
        self.update_frame = tk.Frame(self.window, bg="#0BA68A")

        tk.Label(self.update_frame, text="Current Student Name:", bg="#0BA68A", fg="white").pack()
        self.update_name_entry = tk.Entry(self.update_frame)
        self.update_name_entry.pack(pady=5)

        tk.Label(self.update_frame, text="New Name (optional):", bg="#0BA68A", fg="white").pack()
        self.new_name_entry = tk.Entry(self.update_frame)
        self.new_name_entry.pack(pady=5)

        tk.Label(self.update_frame, text="New Room Number:", bg="#0BA68A", fg="white").pack()
        self.new_room_entry = tk.Entry(self.update_frame)
        self.new_room_entry.pack(pady=5)

        self.update_submit_button = tk.Button(self.update_frame, text="Submit Update", bg="#0BA68A", command=self.update_student)
        self.update_submit_button.pack(pady=10)

    def show_update_form(self):
        self.update_frame.pack(pady=10)  # Shows the form when "Update Student Info" is clicked

    def create_table(self):
        # Creates the students table.
        try:
            #self.cursor.execute("DROP TABLE IF EXISTS students")

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    course TEXT,
                    room_number TEXT NOT NULL,
                    fees_paid REAL DEFAULT 0.0
                    )
                """)
         #Create payments table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS payment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                date TEXT
                )
                """)
            #create rooms table
            self.cursor.execute("""  CREATE TABLE IF NOT EXISTS rooms(
                room_number INTEGER ,
                capacity INTEGER,
                is_available BOOLEAN DEFAULT 1
        
                )
                """)

            self.conn.commit()
            
        except sqlite3.Error as e:
            logging.error("Table creation failed: %s", e)
            messagebox.showerror("Database Error", "Could not initialize tables.")
      
    


    

    def show_add_student_form(self):

        # Clear previous frame if exists
        if hasattr(self, 'add_student_frame'):
            self.add_student_frame.destroy()
    
        self.add_student_frame = tk.Frame(self.window, bg="#0BA68A", padx=20, pady=20)
        self.add_student_frame.pack(pady=10)
    
        fields = [
            ("Student Name:", "name_entry"),
            ("Room Number:", "room_entry"), 
            ("Course:", "course_var"),
            ("Age:", "age_var")
    ]
    
        for i, (label_text, var_name) in enumerate(fields):
            tk.Label(self.add_student_frame, text=label_text, bg="#0BA68A", fg="white").grid(row=i, column=0, pady=5, sticky="e")
        
            if var_name.endswith("_var"):
                entry = tk.Entry(self.add_student_frame, textvariable=getattr(self, var_name))
            else:
                entry = tk.Entry(self.add_student_frame)
                setattr(self, var_name, entry)
            
            entry.grid(row=i, column=1, pady=5, padx=5)
    
        tk.Button(self.add_student_frame, text="Submit", bg="#4CAF50", fg="white",command=self.add_student).grid(row=len(fields), column=0, columnspan=2, pady=10)
       

        
    

    
    def show_delete_form(self):
        self.delete_frame = tk.Frame(self.window, bg="#0BA68A")
        self.delete_frame.pack(pady=10)

        tk.Label(self.delete_frame, text="Student Name to Delete:", bg="#0BA68A", fg="white").pack()
        self.delete_name_entry = tk.Entry(self.delete_frame)
        self.delete_name_entry.pack(pady=5)

        tk.Button(self.delete_frame, text="Delete", bg="red", fg="white", command=self.delete_student).pack(pady=10)

    
    def add_student(self):
        name = self.name_entry.get().strip()
        room = self.room_entry.get().strip()
        course = self.course_var.get().strip()
        age = self.age_var.get().strip()

        if not name or not room or not course or not age:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be a number.")
            return

        try:
            self.cursor.execute(
            "INSERT INTO students (name, age, course, room_number) VALUES (?, ?, ?, ?)",
            (name, age, course, room)
            )
            self.conn.commit()
            messagebox.showinfo("Success", f"Student {name} added to Room {room}")
            self.name_entry.delete(0, tk.END)
            self.room_entry.delete(0, tk.END)
            self.course_var.set("")
            self.age_var.set("")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add student: {e}")
            
        self.add_student_frame.pack_forget()    


    def view_students(self):
        """Retrieves and displays all students from the database."""
        view_win = tk.Toplevel(self.window)
        view_win.title("VIEW STUDENTS")
        view_win.geometry("700x400")
        view_win.config(bg="#0BA68A")
        
        tk.Label(view_win, text="Students List", bg="#0BA68A", fg="white", font=("Arial", 14, "bold")).pack(pady=10)

         # Treeview Widget
        columns = ("ID", "Name", "Age","Course", "Room", "Fees Paid")
        tree = ttk.Treeview(view_win, columns=columns, show="headings")
    
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=90)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        
        
        # Fetch data from database
        try:
            self.cursor.execute("SELECT id, name, age, course, room_number, fees_paid FROM students")
            students = self.cursor.fetchall()
        
            if not students:
                tree.insert("", tk.END, values=("No records found", "", "", "", "", ""))
            else:
                for student in students:
                    tree.insert("", tk.END, values=student)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
    

        
       


        

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
        new_name = self.new_name_entry.strip()
        new_room = self.new_room_entry.strip()

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
            self.update_name_entry.delete(0, tk.END)
            self.new_name_entry.delete(0, tk.END)
            self.new_room_entry.delete(0, tk.END)
            self.update_frame.pack_forget()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update: {e}")
            
    def fees_payment(self):
        name = self.fees_name_entry.strip()
        payment = self.payment_entry.strip()
    
        if not name:
            messagebox.showwarning("Error", "Please enter student name")
            return
    
        if not payment:
            messagebox.showwarning("Error", "Please enter payment amount")
            return
    
        try:
            payment = float(payment)
            if payment <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Payment must be a positive number")
            return
    
        # Update fees in database
        try:
            # Get current fees
            self.cursor.execute("SELECT id, fees_paid FROM students WHERE name=?", (name,))
            student_data = self.cursor.fetchone()
        
            if not student_data:
                messagebox.showerror("Error", "Student not found")
                return
        
            student_id, current_fees = student_data
            new_fees = current_fees + payment
        
            # Update student record
            self.cursor.execute("""
                UPDATE students 
                SET fees_paid = ?
                WHERE id = ?
            """, (new_fees, student_id))
        
            # Record payment in payment table
            today = date.today().isoformat()
            self.cursor.execute("""
                INSERT INTO payment (student_id, amount, date)
                VALUES (?, ?, ?)
            """, (student_id, payment, today))
        
            self.conn.commit()
        
            messagebox.showinfo("Success", 
                          f"Added ${payment:.2f} payment for {name}\n"
                          f"Total paid: ${new_fees:.2f}")
        
        # Clear form
            self.fees_name_entry.delete(0, tk.END)
            self.payment_entry.delete(0, tk.END)
            self.fees_frame.pack_forget()
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to process payment: {e}")
    
    def delete_student(self):
        name_to_delete = self.delete_name_entry.get().strip()

        if not name_to_delete:
            messagebox.showwarning("Input Error", "Please enter a student's name to delete.")
            return

        self.cursor.execute("SELECT * FROM students WHERE name = ?", (name_to_delete,))
        student = self.cursor.fetchone()

        if not student:
            messagebox.showerror("Not Found", "No student found with that name.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name_to_delete}?")
        if confirm:
            try:
                self.cursor.execute("DELETE FROM students WHERE name = ?", (name_to_delete,))
                self.conn.commit()
                messagebox.showinfo("Deleted", f"{name_to_delete} has been removed.")
                self.delete_name_entry.delete(0, tk.END)
                self.delete_frame.pack_forget()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete student: {e}")

    def __del__(self):
        """Closes the database connection when the app is closed."""
        self.conn.close()

# MAIN LOOP
if __name__ == "__main__":
    window = tk.Tk()
    login(window)
    window.mainloop()
