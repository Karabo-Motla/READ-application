import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Frame, Label, Toplevel
from pathlib import Path
import sys
from StoryDatabaseManager import StoryDatabaseManager
from PIL import Image, ImageTk

class ChooseStory:
    """
    A class to represent the story selection interface in the Read App.
    """
    def __init__(self, master=None, show_recommended=False, reading_level=None):
        """
        Initialize the ChooseStory interface.

        Args:
            master (tk.Tk, optional): The parent window. If None, a new Tk instance is created.
            show_recommended (bool): Whether to show recommended stories.
            reading_level (str, optional): The reading level to filter stories by.
        """
        self.master = master if master else tk.Tk()
        self.master.geometry("934x575")
        self.master.configure(bg="#FFFFFF")
        self.master.title("Read App")

        self.reading_level = reading_level 
        self.show_recommended = show_recommended
        self.story_db_manager = StoryDatabaseManager()
        if self.reading_level:
            self.all_excerpts = self.story_db_manager.get_story_excerpts_by_reading_level(self.reading_level, num_stories = 3)
        else:
            self.all_excerpts = self.story_db_manager.get_story_excerpts(num_stories=150)
            
        self.current_page = 1
        self.images = {}  # Dictionary to store image references

        self.setup_ui()
        self.load_images()
        self.create_widgets()
        self.display_stories()

    def setup_ui(self):
        """
        Set up the basic UI elements of the story selection interface.
        """
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

        self.canvas.create_rectangle(0.0, 0.0, 934.0, 582.0, fill="#D9D9D9", outline="")
        self.canvas.create_rectangle(0.0, 0.0, 934.0, 64.0, fill="#F8F7F2", outline="")

    def load_images(self):
        """
        Load all necessary images for the interface.
        """
        self.load_image("image_1.png")
        self.load_image("image_2.png")
        self.load_image("button_1.png")

    def create_widgets(self):
        """
        Create and place all widgets for the story selection interface.
        """
        self.canvas.create_image(467.0, 320.0, image=self.images["image_1.png"])
        self.canvas.create_image(466.0, 32.0, image=self.images["image_2.png"])

        self.home_button = Button(
            self.master,
            image=self.images["button_1.png"],
            borderwidth=0,
            highlightthickness=0,
            bg="#F8F7F2",
            command=self.open_student_home_page,
            relief="flat"
        )
        self.home_button.place(x=870.0, y=0.0, width=60.0, height=64.0)

        if self.reading_level:
            self.back_button = Button(self.master, text="← Back", command=self.back_page)
            self.back_button.place(x=100, y=500, width=120, height=40)
        else:
            self.prev_button = Button(self.master, text="← Previous", command=self.previous_page)
            self.prev_button.place(x=20, y=520, width=120, height=40)
            self.next_button = Button(self.master, text="Next →", command=self.next_page)
            self.next_button.place(x=794, y=520, width=120, height=40)

    def display_stories(self):
        """
        Display the stories in a grid layout, paginated based on the current page.
        """
        for widget in self.master.winfo_children():
            if isinstance(widget, Frame):
                widget.destroy()

        start = (self.current_page - 1) * 6
        end = start + 6
        excerpts = self.all_excerpts[start:end]

        columns = 3
        rows = 2
        frame_width = 280
        frame_height = 180
        x_padding = 20
        y_padding = 50

        for i, excerpt_data in enumerate(excerpts):
            if len(excerpt_data) != 4:
                print(f"Unexpected data structure: {excerpt_data}")
                continue

            story_id, title, excerpt, difficulty = excerpt_data

            row = i // columns
            col = i % columns

            x = col * (frame_width + x_padding) + x_padding
            y = row * (frame_height + y_padding) + y_padding + 30  # Extra 30 for top margin

            frame = Frame(self.master, relief=tk.RAISED, borderwidth=1, width=frame_width, height=frame_height)
            frame.place(x=x, y=y)
            frame.pack_propagate(False)  # Prevent the frame from shrinking

            title_label = Label(frame, text=title, font=("Arial", 12, "bold"), wraplength=frame_width-20)
            title_label.pack(pady=(10, 5))

            difficulty_label = Label(frame, text=f"Difficulty: {difficulty}", font=("Arial", 10))
            difficulty_label.pack()

            truncated_excerpt = (excerpt[:80] + '...') if len(excerpt) > 80 else excerpt
            excerpt_label = Label(frame, text=truncated_excerpt, wraplength=frame_width-20, justify=tk.LEFT)
            excerpt_label.pack(pady=(5, 10))

            button = Button(frame, text="Read Story", 
                            command=lambda i=story_id: self.show_story(i))
            button.pack(side=tk.BOTTOM, pady=10)

    def show_story(self, story_id):
        """
        Open the reading session for the selected story.

        Args:
            story_id (int): The ID of the selected story.
        """
        body = self.story_db_manager.get_story_text(story_id)
        self.master.withdraw()
        reading_window = Toplevel(self.master)
        from ReadingSession import ReadingSession
        reading_session = ReadingSession(body, reading_window)

    def previous_page(self):
        """
        Navigate to the previous page of stories if available.
        """
        # Move to the previous page only if there is one
        if self.current_page > 1:
            self.current_page -= 1
            self.display_stories()  # Display the stories for the previous page

        # Disable the "previous" button if we're back on the first page
        if self.current_page == 1:
            self.prev_button.config(state="disabled")
        else:
            self.prev_button.config(state="normal")  # Re-enable if there are previous pages

        # Enable the "next" button since we're no longer on the last page
        self.next_button.config(state="normal")

    def next_page(self):
        """
        Navigate to the next page of stories if available.
        """
        # Move to the next page only if there are more stories
        if self.current_page * 6 < len(self.all_excerpts):
            self.current_page += 1
            self.display_stories()  # Display the stories for the new page

        # Enable the "previous" button when there is a previous page
        if self.current_page > 1:
            self.prev_button.config(state="normal")

        # Disable the "next" button if the next page exceeds the total number of excerpts
        if self.current_page * 6 >= len(self.all_excerpts):
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")  # Re-enable if there are more pages

    def open_student_home_page(self):
        """
        Open the student home page and close the current window.
        """
        self.master.withdraw()
        student_home_page_window = Toplevel(self.master)
        from StudentHomePage import StudentHomePage
        student_home_page = StudentHomePage(student_home_page_window)
    
    def back_page(self):
        """
        Return to the story selection page.
        """
        self.master.withdraw()
        select_story_window = Toplevel(self.master)
        from SelectStory import SelectStory
        select_story = SelectStory(select_story_window)

    def load_image(self, filename):
        """
        Load an image from the assets directory.

        Args:
            filename (str): The name of the image file to load.

        Returns:
            ImageTk.PhotoImage: The loaded image, or None if loading fails.
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

    @staticmethod
    def relative_to_assets(path: str) -> Path:
        """
        Convert a relative path to an absolute path in the assets directory.

        Args:
            path (str): The relative path of the asset.

        Returns:
            Path: The absolute path to the asset.
        """
        return Path(__file__).parent / "assets" / "frame4" / Path(path)

    def run(self):
        """
        Start the main event loop for the ChooseStory interface.
        """
        self.master.mainloop()

    def close(self):
        """
        Close the database connection and quit the application.
        """
        self.story_db_manager.close_connection()
        self.master.quit()
        
def main():
    root = tk.Tk()
    app = ChooseStory(root)
    app.master.mainloop()

if __name__ == "__main__":
    main()