import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Toplevel, messagebox
from pathlib import Path
from SharedData import SharedData
from StoryDatabaseManager import StoryDatabaseManager
from PIL import Image, ImageTk

class SelectStory:
    """
    A class representing the story selection interface in the Read App.

    This class creates a window where users can choose to have a story recommended
    to them based on their reading level or browse all available stories.
    """

    def __init__(self, master=None):
        """
        Initialize the SelectStory interface.

        Args:
            master (tk.Tk, optional): The parent window. If None, a new Tk instance is created.
        """
        self.master = master if master else tk.Tk()
        self.master.geometry("934x575")
        self.master.configure(bg="#FFFFFF")
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface for the story selection window.

        This method creates the canvas, sets the background, and calls methods to create
        various UI elements.
        """
        self.canvas = Canvas(
        self.master,
        bg = "#FFFFFF",
        height = 575,
        width = 934,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)
             
        self.load_and_set_background()
        self.create_buttons()
        self.create_main_section()

        # Disable window resizing
        self.master.resizable(False, False)

    def load_and_set_background(self):
        """
        Load and set the background images for the interface.

        This method loads the main background image and the logo image, and places them
        on the canvas.
        """
        self.canvas.create_rectangle(0.0, 0.0, 934.0, 582.0, fill="#D9D9D9", outline="")
        bg_image = self.load_image("image_1.png")
        if bg_image:
            self.canvas.create_image(467.0, 320.0, image=bg_image)
            self.bg_image = bg_image  # Keep a reference

        self.canvas.create_rectangle(0.0, 0.0, 934.0, 64.0, fill="#F8F7F2", outline="")
        bg_logo_image = self.load_image("image_2.png")
        if bg_logo_image:
            self.canvas.create_image(466.0,32.0, image=bg_logo_image)
            self.bg_logo_image = bg_logo_image  # Keep a reference

    def create_main_section(self):
        """
        Create the main content section of the interface.

        This method adds text elements to the canvas, including the app title and
        instructions for the user.
        """
        self.canvas.create_rectangle(181.0, 96.0, 785.0, 159.0, fill="#C4D1EC", outline="")
        self.canvas.create_text(467.0, 130.0, anchor="center", text="The number 1 Reading App", fill="#000000", font=("Kadwa Regular", 24 * -1))
        self.canvas.create_text(467.0, 300.0, anchor="center", text="You can choose from our selection of\n stories or you could have the system \n recommend you a story. ", fill="#000000", font=("Kadwa Regular", 20 * -1))

    def create_buttons(self):
        """
        Create and place the buttons on the interface.

        This method loads button images and creates buttons for recommending a story,
        choosing a story, and returning to the home page.
        """
        self.recommend_img = self.load_image("button_1.png")
        self.choose_img = self.load_image("button_2.png")
        self.home_img = self.load_image("button_3.png")

        if self.recommend_img and self.choose_img and self.home_img:
            # Create buttons on the canvas
            Button(
                self.master,
                image=self.recommend_img,
                command=self.recommend_story,
                relief="flat",
                borderwidth=0,
                highlightthickness=0
            ).place(x=140, y=450, width=218, height=51)

            Button(
                self.master,
                image=self.choose_img,
                command=self.open_choose_story,
                relief="flat",
                borderwidth=0,
                highlightthickness=0
            ).place(x=600, y=450, width=218, height=51)

            Button(
                self.master,
                image=self.home_img,
                command=self.open_StudentHomePage,
                relief="flat",
                borderwidth=0,
                highlightthickness=0,
                bg="#F8F7F2",
            ).place(x=870, y=0, width=60, height=64)

    def load_image(self, filename):
        """
        Load an image from the assets directory.

        Args:
            filename (str): The name of the image file to load.

        Returns:
            PhotoImage: The loaded image, or None if loading fails.
        """
        try:
            return PhotoImage(file=self.relative_to_assets(filename))
        except tk.TclError as e:
            print(f"Error loading image {filename}: {e}")
            return None
    
    def relative_to_assets(self, path: str) -> Path:
        """
        Convert a relative path to an absolute path in the assets directory.

        Args:
            path (str): The relative path of the asset.

        Returns:
            Path: The absolute path to the asset.
        """
        return Path(__file__).parent / "assets" / "frame3" / path

    def recommend_story(self):
        """
        Open the ChooseStory window with recommended stories based on the user's reading level.

        This method retrieves the student's reading level from SharedData and opens the
        ChooseStory window with appropriate filters.
        """
        student = SharedData.get_student()
        reading_level = student.reading_level

        if reading_level == "Beginner":
            reading_level = "Easy"
        elif reading_level == "Intermediate":
            reading_level = "Medium"
        elif reading_level == "Advanced":
            reading_level = "Difficult"
        
        self.master.withdraw()
        choose_story_window = Toplevel(self.master)
        from ChooseStory import ChooseStory
        choose_story_window = ChooseStory(choose_story_window, show_recommended=True, reading_level=reading_level)
        choose_story_window.run()
    
    def open_StudentHomePage(self):
        """
        Open the StudentHomePage and close the current window.
        """
        self.master.withdraw()
        student_home_page_window = Toplevel(self.master)
        from StudentHomePage import StudentHomePage
        student_home_page = StudentHomePage(student_home_page_window)

    def open_choose_story(self):
        """
        Open the ChooseStory window to browse all available stories.
        """
        self.master.withdraw()
        choose_story_window = Toplevel(self.master)
        from ChooseStory import ChooseStory
        choose_story = ChooseStory(choose_story_window)
        choose_story.run()


def main():
    root = tk.Tk()
    app = SelectStory(root)
    root.mainloop()

# If this script is the main module, start the application
if __name__ == "__main__":
    main()
