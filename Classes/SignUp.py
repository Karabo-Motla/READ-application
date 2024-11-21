import tkinter as tk
from tkinter import ttk, Canvas, Entry, Button, PhotoImage, StringVar, Label, messagebox, Radiobutton
from pathlib import Path
from PIL import Image, ImageTk
from DatabaseManager import DatabaseManager
from SharedData import SharedData 
import re

class SignUp:
    """
    A class representing the sign-up interface in the Read App.

    This class creates a window where new users can register as either an admin or a student,
    providing necessary information based on their role.
    """

    def __init__(self, master=None):
        """
        Initialize the SignUp interface.

        Args:
            master (tk.Tk, optional): The parent window. If None, a new Tk instance is created.
        """
        self.master = master if master else tk.Tk()
        self.master.geometry("934x575")
        self.master.configure(bg="#FFFFFF")
        self.db_manager = DatabaseManager()
        self.selected_role = StringVar(value="Admin")
        self.selected_role.trace_add("write", self.update_visibility)
        self.setup_ui()
        
        
    def setup_ui(self):
        """
        Set up the user interface for the sign-up window.

        This method creates the canvas and calls other methods to set up various UI elements.
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
        
        self.load_and_set_background()
        self.create_header()
        self.create_main_section()
        self.create_form_fields()
        self.create_buttons()

        self.master.resizable(False, False)

    def load_and_set_background(self):
        """
        Load and set the background image for the interface.
        """
        self.canvas.create_rectangle(0.0, 0.0, 934.0, 575.0, fill="#D9D9D9", outline="")
        bg_image = self.load_image("image_1.png")
        if bg_image:
            self.canvas.create_image(470.0, 289.0, image=bg_image)
            self.bg_image = bg_image  # Keep a reference

    def create_header(self):
        """
        Create the header section of the interface.
        """
        self.canvas.create_rectangle(165.0, 33.0, 769.0, 96.0, fill="#AAC0F6", outline="")
        self.canvas.create_text(
            467.0, 65.0, anchor="center",
            text="WELCOME TO THE READ APP",
            fill="#000000",
            font=("Kadwa Regular", 24)
        )

    def create_main_section(self):
        """
        Create the main content section of the interface.
        """
        self.canvas.create_rectangle(196.0, 118.0, 736.0, 530.0, fill="#AAC0F6", outline="")
        self.canvas.create_rectangle(220.0, 186.0, 703.0, 187.0, fill="#000000", outline="")
        self.canvas.create_text(
            467.0, 160.0, anchor="center",
            text="Sign Up",
            fill="#000000",
            font=("Kadwa Regular", 24)
        )

    def create_form_fields(self):
        """
        Create and place the form fields for user input.

        This method sets up entry fields for name, email, password, and role-specific fields.
        """
        # Name field
        self.image_3 = self.load_image("image_3.png")
        self.create_field("Name", 220, self.image_3, 356, 235)
        self.entry_name = self.create_entry(375.0, 221.0)

        # Email field
        self.image_2 = self.load_image("image_2.png")
        self.create_field("Email", 280, self.image_2, 358, 294)
        self.entry_email = self.create_entry(375.0, 281.0)
        
        # Password field
        self.image_4 = self.load_image("image_4.png")
        self.create_field("Password", 380, self.image_4, 356, 394)
        self.entry_password = self.create_entry(370.0, 380.0,show="*")

        # Role section
        self.canvas.create_text(219.0, 335.0, anchor="nw", text="Role", fill="#000000", font=("Kadwa Regular", 24 * -1))
        radio_admin = Radiobutton(self.master, text="Admin", variable=self.selected_role, value="Admin", indicatoron=True)
        radio_student = Radiobutton(self.master, text="Student", variable=self.selected_role, value="Student", indicatoron=True)
        radio_admin.place(x=342.0, y=340.0, width=85.0, height=17.0)
        radio_student.place(x=485.0, y=340.0, width=85.0, height=18.0)

        # admin key field (for admins)
        self.key_label = Label(self.master, text="Admin Key", font=("Kadwa Regular", 24 * -1), bg="#AAC0F6", fg="#000000")
        self.entry_key = Entry(self.master,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
        self.key_label.place(x=219.0, y=430.0)
        self.entry_key.place(x=400.0, y=430.0, width=100.0, height=27.0)
        
        # Grade field
        self.grade_label = Label(self.master, text="Grade", font=("Kadwa Regular", 19), bg="#AAC0F6", fg="#000000")
        self.grade_label.place(x=219.0, y=430.0)
        self.grade_label.place_forget()
        self.entry_grade = self.create_entry(340.0, 430.0, width=100.0)
        self.entry_grade.place_forget()

        # Reading level dropdown
        self.reading_level = StringVar(self.master)
        self.reading_level.set("Select reading level")
        self.reading_level_menu = ttk.Combobox(
            self.master, 
            textvariable=self.reading_level, 
            values=["Beginner", "Intermediate", "Advanced"], 
        )
        self.reading_level_menu.place(x=500.0, y=430.0, width=150.0, height=27.0)
        self.reading_level_menu.place_forget()

    def create_buttons(self):
        """
        Create and place the buttons on the interface.

        This method creates the sign-up button and a link to the login page.
        """
        self.signUp_img = self.load_image("button_1.png")

        if self.signUp_img:
            Button(
                self.master,
                image=self.signUp_img,
                command=self.check_entries,
                relief="flat",
                borderwidth=0,
                highlightthickness=0
            ).place(x=390.0, y=475.0, width=140.0, height=40.0)

            Button(
                self.master,
                text="login", 
                fg="blue", 
                borderwidth=0, 
                highlightthickness=0, 
                command=self.open_Login, 
                relief="flat"
            ).place(x=440.0, y=545.0, width=52.0, height=20.0)

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

    def create_field(self, label_text, y_pos, icon, icon_x, icon_y):
        """
        Create a labeled field with an icon on the canvas.

        Args:
            label_text (str): The text for the field label.
            y_pos (int): The y-coordinate for the label.
            icon (PhotoImage): The icon image.
            icon_x (int): The x-coordinate for the icon.
            icon_y (int): The y-coordinate for the icon.
        """
        self.canvas.create_text(219.0, y_pos, anchor="nw", text=label_text, fill="#000000", font=("Kadwa Regular", 19))
        if icon:
            self.canvas.create_image(icon_x, icon_y, image=icon)

    def create_entry(self, x, y, width=220.0, height=27.0, show=None):
        """
        Create and place an entry widget.

        Args:
            x (float): The x-coordinate for the entry.
            y (float): The y-coordinate for the entry.
            width (float, optional): The width of the entry. Defaults to 220.0.
            height (float, optional): The height of the entry. Defaults to 27.0.
            show (str, optional): The character to show instead of the actual input. Defaults to None.

        Returns:
            tk.Entry: The created entry widget.
        """
        entry = Entry(self.master, bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0, state="normal", show=show)
        entry.place(x=x, y=y, width=width, height=height)
        return entry

    def relative_to_assets(self, path: str) -> Path:
        """
        Convert a relative path to an absolute path in the assets directory.

        Args:
            path (str): The relative path of the asset.

        Returns:
            Path: The absolute path to the asset.
        """
        return Path(__file__).parent / "assets" / "frame0" / path
    
    def is_entry_empty(self,entry):
        """
        Check if an entry widget is empty.

        Args:
            entry (tk.Entry): The entry widget to check.

        Returns:
            bool: True if the entry is empty, False otherwise.
        """
        return not entry.get().strip()
    
    def is_valid_email(self, email_entry):
        """
        Check if the email in the entry widget is valid.

        Args:
            email_entry (tk.Entry): The entry widget containing the email.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        email = email_entry.get()  
        return bool(re.match(pattern, email))
    
    def check_password_validity(self, password):
        """
        Check if the provided password meets the required security criteria.

        This method verifies that the password:
        - Is at least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        - Contains at least one special character

        Args:
            password (str): The password to be validated.

        Returns:
            bool: True if the password meets all criteria, False otherwise.

        Note:
            If the password fails to meet any criterion, an error message is displayed
            using the show_error method.
        """
        min_length = 8
        has_uppercase = False
        has_lowercase = False
        has_digit = False
        has_special = False
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if len(password) < min_length:
            messagebox.showerror("Invalid Password", "Password must be at least 8 characters long.")
            return False

        for char in password:
            if char.isupper():
                has_uppercase = True
            elif char.islower():
                has_lowercase = True
            elif char.isdigit():
                has_digit = True
            elif char in special_chars:
                has_special = True

        if not has_uppercase:
            messagebox.showerror("Invalid Password", "Password must contain at least one uppercase letter.")
            return False
        if not has_lowercase:
            messagebox.showerror("Invalid Password", "Password must contain at least one lowercase letter.")
            return False
        if not has_digit:
            messagebox.showerror("Invalid Password", "Password must contain at least one digit.")
            return False
        if not has_special:
            messagebox.showerror("Invalid Password", "Password must contain at least one special character.")
            return False

        return True


    def check_entries(self):
        """
        Validate the entries and add the user to the database.

        This method checks if all required fields are filled, validates the email,
        and adds the user to the database based on their role.
        """
        if self.is_entry_empty(self.entry_name) or self.is_entry_empty(self.entry_email) or self.is_entry_empty(self.entry_password):
            messagebox.showwarning("Warning", "One or more fields are empty")
        elif self.selected_role.get() == "Student" and (self.is_entry_empty(self.entry_grade) or self.reading_level.get() == ""):
            messagebox.showwarning("Warning", "Please fill out the grade and reading level fields")
        elif not self.is_valid_email(self.entry_email):  # Pass the Entry widget directly
            messagebox.showerror("Error", f"The email {self.entry_email.get()} is invalid.")
        elif not self.check_password_validity(self.entry_password.get()):
            # Password validation is handled within check_password_validity
            pass
        else:
            if self.selected_role.get() == "Student":
                self.db_manager.add_student(self.entry_name.get(), self.entry_email.get(), self.entry_password.get(), self.entry_grade.get(), self.reading_level.get())
            else:
                self.db_manager.add_admin(self.entry_name.get(), self.entry_email.get(), self.entry_password.get(), self.entry_key.get())       
            self.open_Login()  
    
    def update_visibility(self,*args):
        """
        Update the visibility of role-specific fields based on the selected role.

        This method shows or hides the grade, reading level, and admin key fields
        depending on whether the user selected 'Student' or 'Admin' role.
        """
        if  self.selected_role.get() == "Student":
            self.grade_label.place(x=219.0, y=430.0)  # Show the "Grade" label
            self.entry_grade.place(x=340.0, y=430.0, width=100.0, height=27.0)  # Show the grade entry
            self.reading_level_menu.place(x=500.0, y=430.0, width=150.0, height=27.0)  # Show the reading level menu
            self.key_label.place_forget()
            self.entry_key.place_forget()
        else:
            self.grade_label.place_forget()  # Hide the "Grade" label
            self.entry_grade.place_forget()  # Hide the grade entry
            self.reading_level_menu.place_forget()  # Hide the reading level menu
            self.key_label.place(x=219.0, y=430.0)
            self.entry_key.place(x=400.0, y=430.0, width=100.0, height=27.0)

    def open_selectStory(self):
        """
        Open the SelectStory window and close the current window.
        """
        self.master.destroy()
        import SelectStory
        SelectStory.main()

    def open_Login(self):
        """
        Open the Login window and close the current window.
        """
        self.master.destroy()  
        from Login import main as Login_main
        Login_main()

def main():
    root = tk.Tk()
    app = SignUp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()




