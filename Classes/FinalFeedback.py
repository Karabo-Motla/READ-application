import tkinter as tk
from tkinter import Canvas, Button, PhotoImage , Toplevel
from PIL import Image, ImageTk
import random
from pathlib import Path
import sys

class FinalFeedback:
    """
    A class to create and manage the final feedback window in a reading application.
    
    This class displays the user's reading accuracy, provides feedback, and shows
    visual elements like stars and random images based on the performance.
    """
    
    def __init__(self, master, accuracy):
        """
        Initialize the FinalFeedback window.

        Args:
            master (tk.Tk): The parent window.
            accuracy (float): The user's reading accuracy as a percentage.
        """
        self.window = tk.Toplevel(master)
        self.window.geometry("934x575")
        self.window.configure(bg="#FFFFFF")
        self.window.title("Final Feedback")
        self.master = master
        self.accuracy = accuracy
        self.images = {}
        self.star_size = (90, 90) 

        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=575,
            width=934,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface elements."""
        self.create_background()
        self.display_feedback()
        self.display_stars()
        self.display_random_image()  # Moved this after stars
        self.create_buttons()

    def create_background(self):
        """Create the background rectangle."""
        self.canvas.create_rectangle(
            0.0, 0.0, 934.0, 575.0,
            fill="#C4D0EB", outline=""
        )

    def display_random_image(self):
        """Display a random image from a predefined list."""        
        image_files = ["image_3.png", "image_9.png", "image_5.png", "image_11.png", "image_12.png"]
        random_image = random.choice(image_files)
        image = self.load_image(random_image, (200, 200))  # Increased size
        self.canvas.create_image(467, 400, image=image)  # Adjusted position

    def display_feedback(self):
        """Display feedback text and accuracy score."""
        feedback = self.get_feedback()
        self.canvas.create_text(
            467.0, 80.0, 
            anchor="center",
            text=feedback,
            fill="#000000",
            font=("Inter Bold", 36)
        )

        self.canvas.create_text(
            467.0, 150.0, 
            anchor="center",
            text=f"Your reading accuracy: {self.accuracy:.2f}%",
            fill="#000000",
            font=("Inter Medium", 25)
        )

    def display_stars(self):
        """Display stars based on the accuracy score."""
        num_stars = self.get_num_stars()
        star_image = self.load_image("image_6.png", self.star_size)
        total_width = num_stars * self.star_size[0]
        start_x = (934 - total_width) / 2
        
        for i in range(num_stars):
            x = start_x + i * self.star_size[0]
            self.canvas.create_image(x + self.star_size[0]/2, 250.0, image=star_image) 

    def create_buttons(self):
        """Create 'Back to reading' and 'Exit' buttons."""
        back_button = self.create_button("Back to reading", 100.0, 500.0, 200.0, 40.0, self.open_select_story)  # Adjusted position and size
        back_button.configure(bg="#F8F7F2")
        end_button = self.create_button("Exit",600.0, 500.0, 200.0, 40.0, self.exit)
        end_button.configure(bg="#F8F7F2")

    def create_button(self, text, x, y, width, height, command):
        """Create a button with the given parameters."""
        button = Button(
            self.window,
            text=text,
            command=command,
            relief="raised",
            font=("Inter Medium", 14)
        )
        button.place(x=x, y=y, width=width, height=height)
        return button

    def get_feedback(self):
        """Get a random feedback message based on the accuracy score."""
        if self.accuracy >= 90:
            feedback_list = [
                "Excellent Job!", "Well Done!", "Outstanding Reading!",
                "Fantastic Effort!", "Perfect!", "Great Work!",
                "You're a Reading Pro!", "Impressive Performance!"
            ]
        elif self.accuracy >= 75:
            feedback_list = [
                "Good Job!", "Nice Work!", "Keep It Up!",
                "Great Effort!", "Almost There!", "Solid Reading!",
                "Well Done, Almost Perfect!", "Good Reading, Keep Practicing!"
            ]
        elif self.accuracy >= 60:
            feedback_list = [
                "You're Getting There!", "Keep Trying!", "Good Attempt!",
                "Nice Try!", "Keep Practicing, You're Improving!",
                "Solid Effort, Keep Working!", "Almost There, Keep Going!",
                "Nice Work, You're Making Progress!"
            ]
        else:
            feedback_list = [
                "Keep Practicing!", "Don't Give Up!", "You're Making Progress!",
                "Try Again, You're Learning!", "Keep Working On It!",
                "Practice Makes Perfect!", "You're Doing Great, Just Keep Trying!",
                "Don't Get Discouraged, You'll Improve!"
            ]
        return random.choice(feedback_list)

    def get_num_stars(self):
        """Determine the number of stars to display based on the accuracy score."""
        if self.accuracy >= 90:
            return 5
        elif self.accuracy >= 75:
            return 4
        elif self.accuracy >= 60:
            return 3
        elif self.accuracy >= 40:
            return 2
        else:
            return 1

    def load_image(self, filename, size):
        """Load and resize an image, caching it for future use."""
        if filename not in self.images:
            path = self.relative_to_assets(filename)
            image = Image.open(path)
            image = image.resize(size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.images[filename] = photo
        return self.images[filename]

    def relative_to_assets(self, path: str) -> Path:
        """Convert a relative path to an absolute path in the assets folder."""
        return Path(__file__).parent / Path(r"assets/frame7") / Path(path)
    
    def exit(self):
        """Close the application."""
        self.master.quit()
        self.master.destroy()
        sys.exit()
    
    def open_select_story(self):
        """Open the story selection window and close the current window."""
        select_story = Toplevel(self.master)
        from SelectStory import SelectStory
        select_story = SelectStory(select_story)
        self.window.destroy() 

def main():
    """Main function to run the FinalFeedback window."""
    root = tk.Tk()
    root.withdraw() 
    root.mainloop()

if __name__ == "__main__":
    main()