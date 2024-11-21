import tkinter as tk
from tkinter import ttk, Canvas, Entry, Button, PhotoImage, StringVar, Label, Toplevel
from pathlib import Path
from PIL import Image, ImageTk
from DatabaseManager import DatabaseManager
from SharedData import SharedData

class StudentHomePage:
    """
    A class representing the home page for a student in the READ APP.
    
    This class creates a GUI for displaying and editing student information,
    including name, email, password, grade, and reading level.
    """

    def __init__(self, master=None):
        """
        Initialize the StudentHomePage.

        Args:
            master (tk.Tk, optional): The parent window. If None, a new Tk instance is created.
        """
        self.student = SharedData.get_student()
        self.master = master if master else tk.Tk()
        self.master.geometry("934x575")
        self.master.configure(bg="#FFFFFF")
        self.db_manager = DatabaseManager()
        self.images = {}  # Dictionary to store image references
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface components."""
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
        
        self.load_and_set_background()
        self.create_header()
        self.create_main_section()
        self.create_form_fields()
        self.create_buttons()

        self.master.resizable(False, False)

    def load_and_set_background(self):
        """Load and set the background image for the canvas."""
        self.canvas.create_rectangle(0.0, 0.0, 934.0, 575.0, fill="#D9D9D9", outline="")
        bg_image = self.load_image("image_1.png")
        if bg_image:
            self.canvas.create_image(470.0, 289.0, image=bg_image)

    def create_header(self):
        """Create the header section of the page."""
        self.canvas.create_rectangle(165.0, 33.0, 769.0, 96.0, fill="#AAC0F6", outline="")
        self.canvas.create_text(
            467.0, 65.0, anchor="center",
            text="WELCOME TO THE READ APP",
            fill="#000000",
            font=("Kadwa Regular", 24)
        )

    def create_main_section(self):
        """Create the main section of the page."""
        self.canvas.create_rectangle(196.0, 118.0, 736.0, 530.0, fill="#AAC0F6", outline="")
        self.canvas.create_rectangle(220.0, 186.0, 703.0, 187.0, fill="#000000", outline="")
        self.canvas.create_text(
            467.0, 160.0, anchor="center",
            text="Personal Information",
            fill="#000000",
            font=("Kadwa Regular", 24)
        )

    def create_form_fields(self):
        """Create and populate the form fields for student information."""
        # Name field
        self.create_field("Name", 220, "image_3.png", 356, 235)
        self.entry_name = self.create_entry(375.0, 221.0)
        self.entry_name.insert(0, self.student.name)
        self.entry_name.config(state="readonly")

        # Email field
        self.create_field("Email", 280, "image_2.png", 358, 294)
        self.entry_email = self.create_entry(375.0, 281.0)
        self.entry_email.insert(0, self.student.email)
        self.entry_email.config(state="readonly")

        # Password field
        self.create_field("Password", 340, "image_4.png", 356, 354)
        self.entry_password = self.create_entry(370.0, 340.0)
        self.entry_password.insert(0, self.student.password) 
        self.entry_password.config(state="readonly")

        # Grade field
        Label(self.master, text="Grade", font=("Kadwa Regular", 19), bg="#AAC0F6", fg="#000000").place(x=219.0, y=400.0)
        self.entry_grade = self.create_entry(340.0, 400.0, width=100.0)
        self.entry_grade.insert(0, self.student.grade)
        self.entry_grade.config(state="readonly")

        # Reading level dropdown
        self.reading_level = StringVar(self.master)
        self.reading_level.set(self.student.reading_level)
        self.reading_level_menu = ttk.Combobox(
            self.master, 
            textvariable=self.reading_level, 
            values=["Beginner", "Intermediate", "Advanced"], 
            state="disabled"
        )
        self.reading_level_menu.place(x=500.0, y=400.0, width=150.0, height=27.0)

    def create_buttons(self):
        """Create the buttons for editing, submitting, and navigating back."""
        self.edit_button = Button(self.master, text="Edit details", font="Kadwa 9 bold", fg="black", bd=3, borderwidth=1, highlightthickness=0, command=self.enable_edits, relief="raised")
        self.edit_button.place(x=300.0, y=470.0, width=100.0, height=30.0)

        self.back_button = Button(self.master, text="Back", font="Kadwa 9 bold", fg="black", bd=3, borderwidth=1, highlightthickness=0, command=self.open_selectStory, relief="raised")
        self.back_button.place(x=530.0, y=470.0, width=100.0, height=30.0)

        self.submit_button = Button(self.master, text="Submit", font="Kadwa 9 bold", fg="black", bd=3, borderwidth=1, highlightthickness=0, command=self.update_details, relief="raised")
        self.submit_button.place_forget()

    def create_field(self, label_text, y_pos, icon_filename, icon_x, icon_y):
        """
        Create a field with a label and an icon.

        Args:
            label_text (str): The text for the field label.
            y_pos (int): The y-position of the label.
            icon_filename (str): The filename of the icon image.
            icon_x (int): The x-position of the icon.
            icon_y (int): The y-position of the icon.
        """
        self.canvas.create_text(219.0, y_pos, anchor="nw", text=label_text, fill="#000000", font=("Kadwa Regular", 19))
        icon = self.load_image(icon_filename)
        if icon:
            self.canvas.create_image(icon_x, icon_y, image=icon)

    def create_entry(self, x, y, width=220.0, height=27.0, show=None):
        """
        Create and return an Entry widget.

        Args:
            x (float): The x-position of the entry.
            y (float): The y-position of the entry.
            width (float, optional): The width of the entry. Defaults to 220.0.
            height (float, optional): The height of the entry. Defaults to 27.0.
            show (str, optional): The character to show instead of the actual input. Defaults to None.

        Returns:
            tk.Entry: The created Entry widget.
        """
        entry = Entry(self.master, bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0, state="normal", show=show)
        entry.place(x=x, y=y, width=width, height=height)
        return entry

    def load_image(self, filename):
        """
        Load an image and return a PhotoImage object.

        Args:
            filename (str): The filename of the image to load.

        Returns:
            ImageTk.PhotoImage: The loaded image, or None if loading fails.
        """
        if filename not in self.images:
            try:
                image_path = self.relative_to_assets(filename)
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                self.images[filename] = photo
            except Exception as e:
                print(f"Error loading image {filename}: {e}")
                return None
        return self.images[filename]

    def relative_to_assets(self, path: str) -> Path:
        """
        Get the full path to an asset file.

        Args:
            path (str): The filename of the asset.

        Returns:
            Path: The full path to the asset file.
        """
        return Path(__file__).parent / "assets" / "frame0" / path

    def enable_edits(self):
        """Enable editing of student information fields."""
        for widget in [self.entry_name, self.entry_email, self.entry_grade, self.entry_password, self.reading_level_menu]:
            widget.configure(state="normal")
        self.reading_level_menu.configure(state="readonly")
        self.submit_button.place(x=400.0, y=470.0, width=100.0, height=30.0)
        self.edit_button.place_forget()
        self.back_button.place_forget()

    def disable_edit(self):
        """Disable editing of student information fields."""
        for widget in [self.entry_name, self.entry_email, self.entry_grade, self.entry_password, self.reading_level_menu]:
            widget.configure(state="readonly")
        self.reading_level_menu.configure(state="disabled")
        self.submit_button.place_forget()
        self.back_button.place(x=530.0, y=470.0, width=100.0, height=30.0)
        self.edit_button.place(x=300.0, y=470.0, width=100.0, height=30.0)

    def update_details(self):
        """Update the student details in the database."""
        self.disable_edit()
        self.db_manager.update_student_details(
            self.student.student_id,
            self.entry_name.get(),
            self.entry_email.get(),
            self.entry_password.get(),
            self.entry_grade.get(),
            self.reading_level.get()
        )

    def open_selectStory(self):
        """Open the SelectStory window and hide the current window."""
        self.master.withdraw()
        select_story_window = Toplevel(self.master)
        from SelectStory import SelectStory
        select_story = SelectStory(select_story_window)

def main():
    """Main function to run the StudentHomePage application."""
    root = tk.Tk()
    app = StudentHomePage(root)
    root.mainloop()

if __name__ == "__main__":
    main()