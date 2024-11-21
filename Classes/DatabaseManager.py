import sqlite3
from pathlib import Path
import random, string, hashlib
from datetime import datetime, timedelta
import logging
from student import Student
from tkinter import messagebox
from admin import Admin
from SharedData import SharedData

class DatabaseManager:
    def __init__(self, db_path: str = None):
        # Define the database path inside the Database folder
        if db_path is None:
            db_path = Path(__file__).parent.parent / "Database" / "READ_Database.db"
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    #def hash_password(self,password:str)->str:
    #    return hashlib.sha256(password.encode()).hexdigest()       
    
    def check_login_credentials(self, role: str, email: str, password: str):        
        #hashed_password = self.hash_password(password)
        if role == "Student":
            query = "SELECT Password FROM Students WHERE Email = ?"
        else:
            query = "SELECT Password FROM Admin WHERE Email = ?"
        
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()
        
        if result:
            if result[0] == password:
                return [True,"Password match successful"]
            else:
                return [False,"Password match failed"]
        else:
            return[False,"No result found for the given email"]
        
    def get_user(self,role,email,password):
        #hashed_password = self.hash_password(password)
        if role == "Student":
            query = "SELECT StudentID, Name, Email, Password, Grade, ReadingLevel FROM Students WHERE Email = ? AND Password = ?"
        else:
            query = "SELECT AdminID, Name, Email, Password FROM Admin WHERE Email = ? AND Password = ?"
        
        self.cursor.execute(query, (email,password))
        result = self.cursor.fetchone()

        if role == "Student":
            student_id, student_name, student_email, student_password, student_grade, student_reading_level = result
            student = Student(student_id, student_name, student_email, student_password, student_grade, student_reading_level)
            return student
        else:
            admin_id, admin_name, admin_email, admin_password = result
            admin = Admin(admin_id, admin_name, admin_email, admin_password)
            return admin


    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def view_tables(self):              
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()      
        return tables
    
    def generate_student_id(self, name):
        # First 3 letters of the name (or full name if it's 3 characters)
        name_part = name[:3]

        # If the name is shorter than 3 letters, append random letters
        while len(name_part) < 3:
            name_part += random.choice(string.ascii_uppercase)

        # Generate a 5-digit random number
        number_part = str(random.randint(10000, 99999))

        return name_part.upper() + number_part

    def add_student(self, name, email, password, grade, reading_level):
        # Check if email is already in use
        self.cursor.execute("SELECT * FROM Students WHERE Email = ?", (email,))
        if self.cursor.fetchone() is not None:
            print(f"Error: Email {email} is already in use.")
            return False  # Email is already in use
        
        # Generate unique StudentID
        while True:
            student_id = self.generate_student_id(name)
            self.cursor.execute("SELECT * FROM Students WHERE StudentID = ?", (student_id,))
            if self.cursor.fetchone() is None:
                break  # Found a unique ID
        try:
            self.cursor.execute(
                '''INSERT INTO Students (StudentID, Name, Email, Password, Grade, ReadingLevel)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (student_id, name, email, password, grade, reading_level)
            )
            self.connection.commit()
            print(f"Student {name} added with ID {student_id}")
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

    def remove_student(self, studentID):
        query = "DELETE FROM Students WHERE StudentID = ?"
        self.cursor.execute(query, (studentID,))
        self.connection.commit()
        messagebox.showinfo("Story Removed", f"Student with ID {studentID} removed successfully!")
        return True

    def add_admin(self,name,email,password,adminKey):
        # Check if email is already in use
        self.cursor.execute("SELECT * FROM Admin WHERE Email = ?", (email,))
        if self.cursor.fetchone() is not None:
            print(f"Error: Email {email} is already in use.")
            return False  # Email is already in use
    
        # Insert a new admin into the Admin table
        try:
            self.cursor.execute(
                '''INSERT INTO Admin (Name, Email, Password, AdminKey)
                VALUES (?, ?, ?, ?)''', (name, email, password, adminKey)
            )
            self.connection.commit()
            print(f"Admin {name} added successfully")
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

    def view_admins(self):
        try:
            self.cursor.execute("SELECT AdminID, Name, Email FROM Admin")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching admins: {e}")
            return []

    def display_table_data(self, table_name):
        # Fetch all data from the specified table
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()

        # Fetch the column names for better display
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in self.cursor.fetchall()]

        # Print column names and rows
        print(f"Data from the '{table_name}' table:")
        print(columns)  # Print the column headers
        for row in rows:
            print(row)  # Print each row of the table

    def update_student_details(self,student_id,name,email,password,grade,reading_level):
        try:
            #hashed_password = self.hash_password(password)
            query = '''
            UPDATE Students
            SET Name = ?, Email = ?, Password = ?, Grade = ?, ReadingLevel = ?
            WHERE StudentID = ?
            '''
            self.cursor.execute(query, (name, email, password, grade, reading_level, student_id)) 
            self.connection.commit()
            student = Student(student_id,name,email,password,grade,reading_level)
            SharedData.set_student(student)
            return True  
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False  # Indicate failure
        
    def update_password(self, role, email, new_password):
        if role == "Student":
            query = '''UPDATE Students
                    SET Password = ?
                    WHERE Email = ?'''
        else:
            query = '''UPDATE Admins
                    SET Password = ?
                    WHERE Email = ?'''
        
        self.cursor.execute(query, (new_password, email))
        self.connection.commit()    
        if role == "Student":
            student = self.get_user(role, email, new_password)
            SharedData.set_student(student)
        else:
            admin = self.get_user(role, email, new_password)
            SharedData.set_admin(admin)


    def check_if_user_exists(self, email, role):
        try:
            if role == "Student":
                self.cursor.execute("SELECT COUNT(1) FROM Students WHERE email = ?", (email,))
            elif role == "Admin":
                self.cursor.execute("SELECT COUNT(1) FROM Admin WHERE email = ?", (email,))
            
            result = self.cursor.fetchone()
            if result[0] > 0:
                return True
            return False

        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False
        
    def fetch_all_stats(self):
        try:
            self.cursor.execute("""
                SELECT ID, StudentID, AvgReadingSpeed, AvgAccuracy, Date 
                FROM Stats 
                ORDER BY Date DESC
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching statistics: {e}")
            return []
    
    def fetch_aggregated_stats(self):
        try:
            self.cursor.execute("""
                SELECT 
                    AVG(AvgReadingSpeed) as OverallAvgSpeed, 
                    AVG(AvgAccuracy) as OverallAvgAccuracy
                FROM Stats
            """)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching aggregated statistics: {e}")
            return None

    def fetch_user_stats(self, student_id):
        try:
            self.cursor.execute("""
                SELECT 
                    AVG(AvgReadingSpeed) as UserAvgSpeed, 
                    AVG(AvgAccuracy) as UserAvgAccuracy
                FROM Stats
                WHERE StudentID = ?
            """, (student_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching user statistics: {e}")
            return None

    def fetch_user_improvement(self, student_id, start_date, end_date):
        try:
            self.cursor.execute("""
                SELECT 
                    AVG(AvgReadingSpeed) as AvgSpeed, 
                    AVG(AvgAccuracy) as AvgAccuracy,
                    Date
                FROM Stats
                WHERE StudentID = ? AND Date BETWEEN ? AND ?
                GROUP BY Date
                ORDER BY Date
            """, (student_id, start_date, end_date))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching user improvement: {e}")
            return []

    def add_dummy_data(self, num_students=5, days_range=30):
        try:
            
            # Generate a list of student IDs
            student_ids = [f"STUDENT{i:03d}" for i in range(1, num_students + 1)]
            
            # Generate dates
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_range)
            
            # Prepare the SQL statement
            sql = """
            INSERT INTO Stats (StudentID, AvgReadingSpeed, AvgAccuracy, Date)
            VALUES (?, ?, ?, ?)
            """
            
            # Generate and insert dummy data
            for _ in range(100):  # Let's generate 100 random entries
                student_id = random.choice(student_ids)
                avg_reading_speed = round(random.uniform(50, 200), 2)  # Random speed between 50 and 200 WPM
                avg_accuracy = round(random.uniform(60, 100), 2)  # Random accuracy between 60% and 100%
                date = start_date + timedelta(days=random.randint(0, days_range))
                
                self.cursor.execute(sql, (student_id, avg_reading_speed, avg_accuracy, date.strftime('%Y-%m-%d')))
            
            self.connection.commit()
            print(f"Successfully added dummy data for {num_students} students over {days_range} days.")
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
        

    def clear_dummy_data(self):
        try:
            self.connect_to_database()
            self.cursor.execute("DELETE FROM Stats")
            self.connection.commit()
            print("Successfully cleared all data from Stats table.")
        
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
        

    # Method to both clear existing data and add new dummy data
    def refresh_dummy_data(self, num_students=5, days_range=30):
        self.clear_dummy_data()
        self.add_dummy_data(num_students, days_range)




    
