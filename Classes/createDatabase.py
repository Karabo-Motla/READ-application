import sqlite3
from pathlib import Path
import random, string

class DatabaseSetup:
    def __init__(self, db_folder: str = "Database", db_name: str = "READ_Database.db"):
        # Define the path for the database inside the specified folder
        self.db_path = Path(__file__).parent.parent / db_folder / db_name

    def create_local_database(self):
        # Ensure the directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.db_path.exists():
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Create a table for students
            cursor.execute(
                '''CREATE TABLE Students (
                    StudentID STRING PRIMARY KEY,
                    Name TEXT, 
                    Email TEXT UNIQUE, 
                    Password TEXT, 
                    Grade INTEGER,
                    ReadingLevel TEXT
                )'''
            )
            
            # Create a table for admin
            cursor.execute(
                '''CREATE TABLE Admin (
                    AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT,
                    Email TEXT UNIQUE,
                    Password TEXT,
                    AdminKey TEXT
                )'''
            )

            # Create a table for session
            cursor.execute(
                '''CREATE TABLE Session (
                    SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
                    StudentID STRING,
                    StoryID INTEGER,
                    ReadingSpeed REAL,
                    Accuracy REAL
                )'''
            )

            # Create a table for stats
            cursor.execute(
                '''CREATE TABLE Stats (
                    StudentID STRING,
                    AvgReadingSpeed REAL,
                    AvgAccuracy REAL
                )'''
            )

            connection.commit()
            connection.close()
            print(f"Database created at {self.db_path}")
        else:
            print(f"Database already exists at {self.db_path}")
        

# Example usage:
if __name__ == "__main__":
    db_setup = DatabaseSetup()
    db_setup.create_local_database()
