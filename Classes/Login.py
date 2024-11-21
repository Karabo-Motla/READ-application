import tkinter as tk
from tkinter import messagebox, StringVar
from pathlib import Path
from PIL import Image, ImageTk
from DatabaseManager import DatabaseManager
from SharedData import SharedData

class Login:
    """
    A class representing the login interface for the Read App.

    This class creates a window where users can log in as either an admin or a student,
    and also provides functionality for password reset.
    """

    def __init__(self, master):
        """
        Initialize the Login interface.

        Args:
            master (tk.Tk): The root window for this interface.
        """
        self.master = master
        self.db_manager = DatabaseManager()
        self.master.geometry("934x575")
        self.master.configure(bg="#FFFFFF")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(
            self.master,
            bg="#FFFFFF",
            height=575,
            width=934,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.selected_role = StringVar(value="Admin")
        self.email_entry = None
        self.password_entry = None

        self.load_assets()
        self.create_ui()

    def load_assets(self):
        """Load image assets for the interface."""
        self.assets_path = Path(__file__).parent / "assets/frame1"
        self.images = {
            "background": self.load_image("image_1.png"),
            "email_field": self.load_image("image_2.png"),
            "password_field": self.load_image("image_3.png"),
            "signin_button": self.load_image("button_2.png")
        }

    def load_image(self, filename):
        """
        Load an image file.

        Args:
            filename (str): The name of the image file to load.

        Returns:
            ImageTk.PhotoImage: The loaded image.
        """
        return ImageTk.PhotoImage(Image.open(self.assets_path / filename))

    def create_ui(self):
        """Create and setup all UI elements."""
        self.create_background()
        self.create_header()
        self.create_login_form()
        self.create_role_selection()
        self.create_email_field()
        self.create_password_field()
        self.create_signin_button()
        self.create_forgot_password_button()

    def create_background(self):
        """Create the background elements of the UI."""
        self.canvas.create_rectangle(0, 0, 934, 582, fill="#D9D9D9", outline="")
        self.canvas.create_image(468, 289, image=self.images["background"])
        self.canvas.create_rectangle(196, 118, 736, 530, fill="#AAC0F6", outline="")

    def create_header(self):
        """Create the header section of the UI."""
        self.canvas.create_rectangle(165, 33, 769, 96, fill="#AAC0F6", outline="")
        self.canvas.create_text(
            467, 65, anchor="center", text="WELCOME TO THE READ APP",
            fill="#000000", font=("Kadwa Regular", 24)
        )

    def create_login_form(self):
        """Create the main login form section."""
        self.canvas.create_rectangle(220, 186, 703, 187, fill="#000000", outline="")
        self.canvas.create_text(
            467, 160, anchor="center", text="Login",
            fill="#000000", font=("Kadwa Regular", 24)
        )

    def create_role_selection(self):
        """Create the role selection radio buttons."""
        self.canvas.create_text(
            262, 235, anchor="nw", text="Role",
            fill="#000000", font=("Kadwa Regular", 19)
        )
        tk.Radiobutton(self.master, text="Admin", variable=self.selected_role, value="Admin", indicatoron=True).place(x=358, y=240, width=85, height=17)
        tk.Radiobutton(self.master, text="Student", variable=self.selected_role, value="Student", indicatoron=True).place(x=485, y=240, width=85, height=18)

    def create_email_field(self):
        """Create the email input field."""
        self.canvas.create_text(
            250, 295, anchor="nw", text="Email",
            fill="#000000", font=("Kadwa Regular", 19)
        )
        self.canvas.create_image(373, 308, image=self.images["email_field"])
        self.email_entry = tk.Entry(bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
        self.email_entry.place(x=387, y=295, width=220, height=27)

    def create_password_field(self):
        """Create the password input field."""
        self.canvas.create_text(
            215, 350, anchor="nw", text="Password",
            fill="#000000", font=("Kadwa Regular", 19)
        )
        self.canvas.create_image(373, 364, image=self.images["password_field"])
        self.password_entry = tk.Entry(bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0, show="*")
        self.password_entry.place(x=387, y=350, width=220, height=27)

    def create_signin_button(self):
        """Create the sign-in button."""
        signin_button = tk.Button(
            image=self.images["signin_button"],
            borderwidth=0,
            highlightthickness=0,
            command=self.check_entries,
            relief="flat"
        )
        signin_button.place(x=371, y=420, width=171, height=46)

    def create_forgot_password_button(self):
        """Create the 'forgot password' button."""
        forgot_password_button = tk.Button(
            text="forgot password",
            fg="blue",
            borderwidth=0,
            highlightthickness=0,
            command=self.forgot_password,
            relief="flat"
        )
        forgot_password_button.place(x=400, y=490, width=100, height=22)

    def check_entries(self):
        """
        Validate the login credentials and proceed with login if valid.
        """
        email = self.email_entry.get()
        password = self.password_entry.get()    
        role = self.selected_role.get()

        if not email.strip() or not password.strip():
            messagebox.showwarning("Warning", "One or both fields are empty")
            return

        db_manager = DatabaseManager()
        valid = db_manager.check_login_credentials(role, email, password)
        
        if valid[0]:
            if role == "Student":
                student = db_manager.get_user(role, email, password)
                SharedData.set_student(student)
                self.open_select_story()
            else:
                admin = db_manager.get_user(role, email, password)
                SharedData.set_admin(admin)
                self.open_AdminHomePage()
        else: 
            messagebox.showerror("Error", valid[1])
        
        db_manager.close_connection()
    
    def open_select_story(self):
        """Open the SelectStory window and close the current window."""
        self.master.destroy()
        from SelectStory import main as select_story_main
        select_story_main()       

    def open_AdminHomePage(self):
        """Open the AdminHomePage window and close the current window."""
        self.master.destroy()
        from AdminHomePage import main as admin_homepage_main
        admin_homepage_main()

    def forgot_password(self):
        """Open a new window for password reset."""
        self.reset_window = tk.Toplevel(self.master)
        self.reset_window.title("Reset Password")

        tk.Label(self.reset_window, text="New Password:").pack(pady=5)
        self.new_password_entry = tk.Entry(self.reset_window, show="*")
        self.new_password_entry.pack(pady=5)

        tk.Label(self.reset_window, text="Confirm New Password:").pack(pady=5)
        self.confirm_password_entry = tk.Entry(self.reset_window, show="*")
        self.confirm_password_entry.pack(pady=5)

        tk.Button(self.reset_window, text="Submit", command=self.reset_password).pack(pady=20)

    def reset_password(self):
        """
        Reset the user's password after validating the new password.
        """
        email = self.email_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        role = self.selected_role.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not self.db_manager.check_if_user_exists(email, role):
            messagebox.showerror("Error", "No user found with this email!")
            return
        
        from SignUp import SignUp
        if not SignUp.check_password_validity(self, new_password):
            return  # The check_password_validity function will show an error message if the password is invalid

        self.db_manager.update_password(role, email, new_password)
        messagebox.showinfo("Success", "Password updated successfully!")
        self.reset_window.destroy()

def main():
    """
    Main function to run the Login application.
    """
    root = tk.Tk()
    app = Login(root)
    root.mainloop()

if __name__ == "__main__":
    main()