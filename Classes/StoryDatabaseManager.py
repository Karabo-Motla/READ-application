import sqlite3
from pathlib import Path
from tkinter import messagebox

class StoryDatabaseManager:
    def __init__(self, db_path: str = None):
        # Initialize the database connection.
        if db_path is None:
            db_path = Path(__file__).parent.parent / "Database" / "tinystories.db"
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        #Establish a connection to the database.
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def get_story_excerpts(self, num_stories=9):
        try:
            query = "SELECT id, title, excerpt, difficulty FROM stories LIMIT ?"
            self.cursor.execute(query, (num_stories,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching story excerpts: {e}")
            return []

    def get_story_excerpts_by_reading_level(self, reading_level, num_stories=3):
        query = "SELECT id, title, excerpt, difficulty FROM Stories WHERE difficulty = ? LIMIT ?"
        self.cursor.execute(query, (reading_level, num_stories))
        
        return self.cursor.fetchall()
    
    def get_story_text(self, story_id: int):                 
        try:
            query = "SELECT body FROM stories WHERE id = ?"
            self.cursor.execute(query, (story_id,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            return ""
        except sqlite3.Error as e:
            print(f"Error fetching story text: {e}")
            return ""
        
    def add_story(self, title: str, excerpt: str, body: str, difficulty: str):
        query = "INSERT INTO stories (title, excerpt, body, difficulty) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (title, excerpt, body, difficulty))
        self.connection.commit()
        messagebox.showinfo("Story Added", f"The story titled '{title}' has been added to the database.")

    def remove_story(self, story_id):
        query = "DELETE FROM stories WHERE id = ?"
        self.cursor.execute(query, (story_id,))
        self.connection.commit()
        messagebox.showinfo("Story Removed", f"Story with ID {story_id} removed successfully!")

    def close_connection(self):
        if self.cursor:
            try:
                self.cursor.close()
            except sqlite3.ProgrammingError:
                print("Cursor is already closed.")
        if self.connection:
            try:
                self.connection.close()
            except sqlite3.ProgrammingError:
                print("Connection is already closed.")

    def __del__(self):
        self.close_connection()
