import tkinter as tk
import sys
from pathlib import Path
from tkinter import Canvas, PhotoImage, Text, Toplevel, Button
import re
from audio import Audio
from Feedback import Feedback
from PIL import Image, ImageTk
import time
import sqlite3
from SharedData import SharedData

class ReadingSession:
    """
    A class representing a reading session for a story-based reading application.

    This class manages the user interface and functionality for a reading session,
    including displaying text, recording audio, providing feedback, and storing
    statistics.
    """

    story_ended = False

    def __init__(self, story_text, master=None):
        """
        Initialize the ReadingSession.

        Args:
            story_text (str): The full text of the story.
            master (tk.Tk, optional): The main Tkinter window. Defaults to None.
        """
        self.master = master if master else tk.Tk()
        self.feedback_window= None
        self.master.geometry("934x575")
        self.master.configure(bg="#FFFFFF")
        self.story_text = story_text if story_text else "No story provided."
        self.current_line = 0
        self.total_time = 0
        self.word_count = 0
        self.total_correct_words = 0
        self.sentences = re.split(r'(?<=[.!?]) +', story_text)
        self.expected_text = ""
        self.recorder = Audio()
        self.button_next = None
        self.stop_recording_button= None
        self.start_recording_button= None
        self.images = {}  
        self.start_time = None 
        self.setup_ui()
        self.load_images()
        self.create_buttons()
        self.display_current_line()
        self.db_path = Path(__file__).parent.parent / "Database" / "READ_Database.db"
        self.connection = None
        self.cursor = None
        self.connect_to_database()
        SharedData.set_session_status(True)
        
    def connect_to_database(self):
        """Establish a connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def close_database_connection(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()

    def __del__(self):
        """Destructor to ensure database connection is closed."""
        self.close_database_connection()

    def setup_ui(self):
        """Set up the user interface elements."""
        self.canvas = Canvas(
            self.master,
            bg="#FFFFFF",
            height=575,
            width=934,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            934.0,
            575.0,
            fill="#F8BABA",
            outline=""
        )
        self.canvas.create_rectangle(
            167.0,
            30.0,
            730.0,
            120.0,
            fill="#F7B3B3",
            outline="pink1"
        )
        self.canvas.create_text(
            450.0,
            75.0,
            anchor="center",
            text="Press button and start reading",
            fill="#000000",
            font=("Inter Medium", 40 * -1)
        )
        self.canvas.create_rectangle(
            20.0,
            142.0,
            922.0,
            348.0,
            fill="#F8BABA",
            outline=""
        )     
        
        self.text_widget = Text(self.master, bg="#F8BABA", font=("Inter Bold", 20), wrap="word", height=4, width=55)
        self.text_widget.place(x=61.0, y=185.0)
        self.text_widget.config(state=tk.DISABLED)

    def load_images(self):
        """Load images for buttons."""
        self.load_image("button_1.png")
        self.load_image("button_2.png")
        self.load_image("button_3.png")

    def create_buttons(self):
        """Create and place buttons on the interface."""
        if all(name in self.images for name in ["button_1.png", "button_2.png", "button_3.png"]):
            self.button_next = Button(
                self.master,
                image=self.images["button_1.png"],
                command=self.next_line,
                relief="flat",
                borderwidth=0,
                highlightthickness=0
            )
            self.button_next.place(x=350.0, y=370.0, width=211.0, height=39.0)
            self.button_next.config(state="disabled")

            self.start_recording_button = Button(
                self.master,
                image=self.images["button_2.png"],
                command=self.start_recording,
                relief="flat",
                borderwidth=0,
                highlightthickness=0
            )
            self.start_recording_button.place(x=150.0, y=454.0, width=174.0, height=51.0)

            self.stop_recording_button = Button(
                self.master,
                image=self.images["button_3.png"],
                command=self.on_stop_recording,
                relief="flat",
                borderwidth=0,
                highlightthickness=0
            )
            self.stop_recording_button.place(x=580.0, y=454.0, width=174.0, height=51.0)
            self.stop_recording_button.config(state="disabled")

    def display_current_line(self):
        """Display the current sentence of the story."""
        if self.current_line >= len(self.sentences):
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete(1.0, "end")
            self.text_widget.insert("end", "Well done. You have completed the story")
            self.text_widget.config(state=tk.DISABLED)
            self.button_next.config(state=tk.DISABLED)
            SharedData.set_session_status(False)
            self.accuracy = Feedback.get_accuracy()
            self.insert_stats()
            self.total_time = 0
            self.word_count = 0
            self.fetch_and_print_data()
            self.show_final_feedback()
        else:
            current_sentence = self.sentences[self.current_line]
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete(1.0, "end")
            self.text_widget.insert("end", current_sentence)
            self.text_widget.config(state=tk.DISABLED)
            self.expected_text = current_sentence
            self.word_count += len(self.expected_text.split())
        
    def next_line(self):
        """Move to the next sentence in the story."""
        self.current_line += 1
        self.display_current_line()
        self.start_recording_button.config(state="active")
        self.button_next.config(state="disabled")

    def load_image(self, filename):
        """
        Load an image file.

        Args:
            filename (str): The name of the image file.

        Returns:
            PhotoImage: The loaded image, or None if loading failed.
        """
        try:
            path = self.relative_to_assets(filename)
            image = Image.open(path)
            photo = ImageTk.PhotoImage(image)
            self.images[filename] = photo
            return photo
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
            return None

    def relative_to_assets(self, path: str) -> Path:
        """
        Get the relative path to asset files.

        Args:
            path (str): The file name.

        Returns:
            Path: The full path to the asset file.
        """
        return Path(__file__).parent / "assets" / "frame2" / path

    def on_stop_recording(self):
        """Handle stopping of audio recording."""
        transcription = self.recorder.stop_recording()
        self.button_next.config(state="active")
        self.total_time += time.time() - self.start_time  
        if self.feedback_window is None or not self.feedback_window.is_alive():
            self.feedback_window = Feedback(transcription, self.expected_text, self)
        else:
            self.feedback_window.update_content(transcription, self.expected_text)
        self.feedback_window.show()
        self.master.withdraw()  # Hide the reading session window

    def show(self):
        """Display the reading session window."""
        self.master.deiconify()  
        self.set_button_states()

    def start_recording(self):
        """Start audio recording."""
        self.stop_recording_button.config(state="active")
        self.start_recording_button.config(state="disabled")
        self.start_time = time.time()  # Start the timer
        self.recorder.start_recording()  # Start recording
        
    def set_button_states(self):
        """Set the states of buttons based on current action."""
        self.stop_recording_button.config(state="disabled")
        self.button_next.config(state="active")
        self.start_recording_button.config(state="disabled")

    def calculate_reading_speed(self):
        """
        Calculate the reading speed in words per minute.

        Returns:
            float: The reading speed in WPM.
        """
        if  self.total_time> 0:
            wpm = (self.word_count / self.total_time) * 60  # WPM formula
            return wpm
        return 0
    
    def insert_stats(self):
        """Insert reading statistics into the database."""
        if not self.cursor:
            self.connect_to_database()
        
        self.speed = self.calculate_reading_speed()
        self.student = SharedData.get_student()
        self.student_id = self.student.student_id

        try:
            self.cursor.execute(
                '''INSERT INTO Stats (StudentID, AvgReadingSpeed, AvgAccuracy)
                VALUES (?, ?, ?)''',
                 (self.student_id, f"{self.speed:.1f}", f"{self.accuracy:.1f}")
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting Stats into database: {e}")
        finally:
            self.close_database_connection()

    def fetch_and_print_data(self):
        """Fetch and print session data from the database."""
        self.connect_to_database()
        try:
            self.cursor.execute('SELECT * FROM Session')
            rows = self.cursor.fetchall()
        finally:
            self.close_database_connection()

    def show_final_feedback(self):
        """Display final feedback after completing the story."""
        from FinalFeedback import FinalFeedback
        final_feedback = FinalFeedback(self.master, self.accuracy)
        self.master.wait_window(final_feedback.window)
        

    def open_feedback(self):
        """Open the feedback window."""
        self.master.withdraw()
        feedback_window = Toplevel(self.master)
        from Feedback import Feedback
        feedback_window_page = Feedback(feedback_window)

def main():
    """Main function to run the ReadingSession."""
    root = tk.Tk()
    app = ReadingSession("Initial expected text", root)
    root.mainloop()
    
if __name__ == "__main__":
    main()