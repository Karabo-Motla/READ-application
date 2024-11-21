from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, Toplevel, StringVar, OptionMenu, ttk, messagebox, Frame
from StoryDatabaseManager import StoryDatabaseManager
from DatabaseManager import DatabaseManager
from tkcalendar import DateEntry
from datetime import datetime
import re

class AdminHomePage:
    """
    A class representing the admin home page of the application.
    """

    def __init__(self, master):
        """
        Initialize the AdminHomePage class, set up the main window's geometry, 
        background color, and title, and instantiate database managers for 
        stories and students.

        Args:
            master (Tk): The main window (root) of the Tkinter application.
        """
        self.master = master
        self.master.geometry("934x575")
        self.master.configure(bg="#FFFFFF")
        self.master.title("Admin Home Page")

        self.story_db = StoryDatabaseManager()
        self.student_db = DatabaseManager()
        self.student_db.add_dummy_data()
        
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

        self.load_images()
        self.create_ui()

    def load_images(self):
        """
        Load and initialize the image assets required for the UI.
        """
        self.assets_path = Path(__file__).parent / Path(r"assets\frame6")
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.button_images = [
            PhotoImage(file=self.relative_to_assets(f"button_{i}.png"))
            for i in range(1, 8)
        ]
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))

    def relative_to_assets(self, path: str) -> Path:
        """
        Return the path to the asset directory for the images used in the UI.

        Args:
            path (str): Relative path to the asset file.

        Returns:
            Path: Full path to the requested asset file.
        """
        return self.assets_path / Path(path)

    def create_ui(self):
        """
        Create and arrange all the UI elements on the Admin Home Page.
        Calls helper methods to create the background, buttons, and header.
        """
        self.create_background()
        self.create_buttons()
        self.create_header()

    def create_background(self):
        """
        Create the background for the admin home page using a Canvas widget.
        """
        self.canvas.create_rectangle(0, 0, 934, 582, fill="#D9D9D9", outline="")
        self.canvas.create_image(472, 320, image=self.image_1)

    def create_buttons(self):
        """
        Create and configure the buttons on the Admin Home Page. 
        Each button is linked to a specific function to handle the 
        corresponding task.
        """
        button_configs = [
            (89, 362, 163, 167, self.open_add_story_window),
            (368, 141, 163, 171, self.open_view_admins_window),
            (667, 141, 163, 172, self.view_all_stats),
            (667, 362, 163, 171, self.open_view_story_window),
            (368, 362, 163, 169, self.open_delete_story_window),
            (89, 141, 163, 169, self.open_view_students_window),
        ]

        for i, (x, y, width, height, command) in enumerate(button_configs):
            Button(
                self.master,
                image=self.button_images[i],
                borderwidth=0,
                highlightthickness=0,
                command=command,
                relief="flat"
            ).place(x=x, y=y, width=width, height=height)

    def create_header(self):
        """
        Create the header section for the Admin Home Page.
        """
        self.canvas.create_rectangle(0, 0, 934, 64, fill="#F8F7F2", outline="")
        self.canvas.create_image(466, 32, image=self.image_2)
        

    def open_add_story_window(self):
        """
        Open a new window that allows the admin to add a new story to the database.
        The window contains input fields for the story title, difficulty, excerpt, and full text.
        """
        add_window = Toplevel(self.master)
        add_window.geometry("400x450")
        add_window.title("Add New Story")

        # Labels
        Label(add_window, text="Title:").pack(pady=5)
        title_entry = Entry(add_window, width=40)
        title_entry.pack(pady=5)

        difficulty_var = StringVar(add_window)
        difficulty_var.set("Medium")  # default value

        Label(add_window, text="Difficulty:").pack(pady=5)
        difficulty_var = StringVar()
        difficulty_var.set("Medium") # Default
        difficulty_entry = OptionMenu(add_window, difficulty_var, "Easy", "Medium", "Hard")
        difficulty_entry.pack(pady=5)

        Label(add_window, text="Excerpt:").pack(pady=5)
        excerpt_entry = Entry(add_window, width=40)
        excerpt_entry.pack(pady=5)

        Label(add_window, text="Text:").pack(pady=5)
        text_entry = Text(add_window, height=10, width=30)
        text_entry.pack(pady=5)

        def submit_story():
            title = title_entry.get().strip()  
            excerpt = excerpt_entry.get().strip()
            text = text_entry.get("1.0", "end-1c").strip()  
            difficulty = difficulty_var.get().strip()  
            
            if not title or not excerpt or not text or not difficulty:
                messagebox.showerror("Input Error", "All fields must be filled out.")
                return  
            
            # Add the story via the Admin class
            self.story_db.add_story(title, excerpt, text, difficulty)
            
            # Close the database connection
            self.story_db.close_connection()
            add_window.destroy()

        # Submit button
        submit_button = Button(add_window, text="Add Story", command=submit_story)
        submit_button.pack(pady=10)

    def open_view_story_window(self):
        """
        Open a new window that displays all the stories stored in the database in a table format.
        Uses a Treeview widget to show each story's ID, title, excerpt, body, and difficulty.
        """
        view_window = Toplevel(self.master)
        view_window.geometry("800x500")
        view_window.title("View Stories")

        # Label for the window
        Label(view_window, text="Stories", font=("Arial", 14)).pack(pady=10)

        # Create a Treeview widget to display the stories in a table
        columns = ("ID", "Title", "Excerpt", "Body", "Difficulty")

        tree = ttk.Treeview(view_window, columns=columns, show="headings", height=15)
        tree.heading("ID", text="ID")
        tree.heading("Title", text="Title")
        tree.heading("Excerpt", text="Excerpt")
        tree.heading("Body", text="Body" )
        tree.heading("Difficulty", text="Difficulty")

        tree.column("ID", width=50, anchor='center')
        tree.column("Title", width=200, anchor='center')
        tree.column("Excerpt", width=300, anchor='center')
        tree.column("Body", width= 300, anchor='center')
        tree.column("Difficulty", width=100, anchor='center')
        
        tree.pack(pady=20)

        # Database connection to retrieve stories
        self.story_db.cursor.execute("SELECT * FROM stories")  # Fetch all stories
        stories = self.story_db.cursor.fetchall()

        # Insert the stories into the Treeview
        for story in stories:
            tree.insert("", "end", values=story)

    def open_delete_story_window(self):
        """
        Open a new window where the admin can delete a story by entering its ID.
        This method also checks for the validity of the ID and confirms the deletion.
        """
        delete_window = Toplevel(self.master)
        delete_window.geometry("300x150")
        delete_window.title("Delete Story")

        # Label
        Label(delete_window, text="Enter Story ID to Delete:").pack(pady=10)

        # Entry for Story ID
        id_entry = Entry(delete_window, width=30)
        id_entry.pack(pady=10)

        def delete_story():
            story_id = id_entry.get()

            if not story_id.isdigit():
                print("Invalid ID. Please enter a numeric ID.")
                return

            self.story_db.remove_story(int(story_id))
            self.story_db.close_connection()
            delete_window.destroy()

        # Delete button
        delete_button = Button(delete_window, text="Delete Story", command=delete_story)
        delete_button.pack(pady=10)

    def open_view_students_window(self):
        """
        Open a new window that displays all students in a table format.
        Allows for searching, adding, and removing students using a Treeview widget.
        """
        view_window = Toplevel(self.master)
        view_window.geometry("800x500")
        view_window.title("Manage Users")

        # Label for the window
        Label(view_window, text="All Students", font=("Arial", 14)).pack(pady=10)

        # Create a frame for search and buttons
        search_frame = Frame(view_window)
        search_frame.pack(pady=10, fill='x')

        # Label for the search bar
        search_label = Label(search_frame, text="Search:", font=("Arial", 10))
        search_label.grid(row=0, column=0, padx=10)

        # Create a search bar
        search_var = StringVar()
        entrybox = Entry(search_frame, textvariable=search_var, font=("Arial", 10))
        entrybox.grid(row=0, column=1, padx=10)

        # Add and Remove buttons on the right side
        add_button = Button(search_frame, text="Add Student", font=("Arial", 10), command=lambda: self.open_add_student_window(tree, view_window))
        add_button.grid(row=0, column=2, padx=20, sticky='e')

        remove_button = Button(search_frame, text="Remove Student", font=("Arial", 10), command=lambda: self.remove_student(tree))
        remove_button.grid(row=0, column=3, padx=10, sticky='e')

        # Create a Treeview widget to display the stories in a table
        columns = ("StudentID", "Name", "Email", "Grade", "ReadingLevel")

        tree = ttk.Treeview(view_window, columns=columns, show="headings", height=15)
        tree.heading("StudentID", text="Student ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Grade", text="Grade")
        tree.heading("ReadingLevel", text="Reading Level")

        tree.column("StudentID", width=100, anchor='center')
        tree.column("Name", width=150, anchor='center')
        tree.column("Email", width=200, anchor='center')
        tree.column("Grade", width=50, anchor='center')
        tree.column("ReadingLevel", width=100, anchor='center')

        tree.pack(pady=20)

        # Database connection to retrieve students
        self.student_db.cursor.execute("SELECT StudentID, Name, Email, Grade, ReadingLevel FROM students")  
        students = self.student_db.cursor.fetchall()

        # Insert the students into the Treeview
        for student in students:
            tree.insert("", "end", values=student)

        
        # Function to filter students
        def check(e):
            for item in tree.get_children():
                tree.delete(item)

            typed = search_var.get().lower()

            filtered_students = []
            for student in students:
                if (typed in str(student[0]).lower() or  
                    typed in student[1].lower() or  
                    typed in student[2].lower() or  
                    typed in str(student[3]).lower() or  
                    typed in student[4].lower()):  
                    filtered_students.append(student)

            for student in filtered_students:
                tree.insert("", "end", values=student)

        # Bind the search function to the Entry widget
        entrybox.bind("<KeyRelease>", check)

    def open_add_student_window(self, tree, view_window):
        """
        Open a window where the admin can add a new student to the system by filling out the form.
        The window contains fields for the student's name, email, password, grade, and reading level.

        Args:
            tree (ttk.Treeview): The Treeview widget displaying the list of students.
            view_window (Toplevel): The window in which the student information is shown.
        """
        add_window = Toplevel(self.master)
        add_window.geometry("300x300")
        add_window.title("Add Student")

        # Student details input fields
        Label(add_window, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        name_var = StringVar()
        Entry(add_window, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)

        Label(add_window, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        email_var = StringVar()
        Entry(add_window, textvariable=email_var).grid(row=1, column=1, padx=10, pady=10)

        Label(add_window, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        password_var = StringVar()
        Entry(add_window, textvariable=password_var, show="*").grid(row=2, column=1, padx=10, pady=10)

        Label(add_window, text="Grade:").grid(row=3, column=0, padx=10, pady=10)
        grade_var = StringVar()
        Entry(add_window, textvariable=grade_var).grid(row=3, column=1, padx=10, pady=10)

        reading_level_var = StringVar(add_window)
        reading_level_var.set("Intermediate")  # default value
        Label(add_window, text="Reading Level:").grid(row=4, column=0, pady=5, padx=10, sticky='e')
        reading_level_option = OptionMenu(add_window, reading_level_var, "Beginner", "Intermediate", "Advanced")
        reading_level_option.grid(row=4, column=1, pady=5, padx=10)

        # Function to add a new student to the database and update the tree
        def save_student():
            name = name_var.get()
            email = email_var.get()
            password = password_var.get()
            grade = grade_var.get()
            reading_level = reading_level_var.get()

            if not (re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)):
                messagebox.showinfo("Invalid", "The email is invalid.")
                return

            if name and email and password and grade and reading_level:
                # Add student to the database
                studentID = self.student_db.add_student(name, email, password, grade, reading_level)
                tree.insert("", "end", values=(studentID, name, email, int(grade), reading_level))
                # student_db.close_connection()
                view_window.destroy()
                self.open_view_students_window()

                add_window.destroy()

        Button(add_window, text="Save", command=save_student).grid(row=5, column=0, columnspan=2, pady=10)

    def remove_student(self, tree):
        """
        Remove a selected student from the database after confirming with the admin.
        Updates the Treeview to reflect the change.

        Args:
            tree (ttk.Treeview): The Treeview widget displaying the list of students.
        """
        selected_item = tree.selection()
        
        if selected_item:
            for item in selected_item:
                student_id = tree.item(item, 'values')[0]
                
                response = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this student?")
                
                if response:
                    try:
                        success = self.student_db.remove_student(student_id)
                        
                        if success:
                            tree.delete(item)
                        else:
                            messagebox.showerror("Error", "Failed to delete student from the database.")
                    except Exception as e:
                        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
                else:
                    messagebox.showinfo("Cancelled", "Delete action cancelled.")

    def open_view_admins_window(self):
        """
        Open a new window that displays a list of all admins in a table format.
        Includes functionality for searching through the admin records.
        """
        view_window = Toplevel(self.master)
        view_window.geometry("800x500")
        view_window.title("View Admins")

        # Label for the window
        Label(view_window, text="All Admins", font=("Arial", 14)).pack(pady=10)

        # Create a frame for search
        search_frame = Frame(view_window)
        search_frame.pack(pady=10, fill='x')

        # Label for the search bar
        search_label = Label(search_frame, text="Search:", font=("Arial", 10))
        search_label.grid(row=0, column=1, padx=10)

        # Create a search bar
        search_var = StringVar()
        entrybox = Entry(search_frame, textvariable=search_var, font=("Arial", 10))
        entrybox.grid(row=0, column=2, padx=10)

        # Create a Treeview widget to display the stories in a table
        columns = ("AdminID", "Name", "Email")

        tree = ttk.Treeview(view_window, columns=columns, show="headings", height=15)
        tree.heading("AdminID", text="Admin ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")

        tree.column("AdminID", width=100, anchor='center')
        tree.column("Name", width=150, anchor='center')
        tree.column("Email", width=200, anchor='center')

        tree.pack(pady=20)

    # Database connection to retrieve admins
        admins = self.student_db.view_admins()  
        # admins = self.student_db.cursor.fetchall()

        # Insert the admins into the Treeview
        for admin in admins:
            tree.insert("", "end", values=admin)

        # Function to filter admins
        def check(e):
            # Clear existing rows in the Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Get the current input from the search bar
            typed = search_var.get().lower()

            # Filter admins by checking if the typed input is in any of the columns (AdminID, Name, Email)
            filtered_admins = []
            for admin in admins:
                if (typed in str(admin[0]).lower() or  # AdminID
                    typed in admin[1].lower() or  # Name
                    typed in admin[2].lower()):  # Email
                    filtered_admins.append(admin)

            # Insert the filtered admins into the Treeview
            for admin in filtered_admins:
                tree.insert("", "end", values=admin)

        # Bind the search function to the Entry widget
        entrybox.bind("<KeyRelease>", check)

    def view_all_stats(self):
        """
        Open a window that displays various statistics related to student reading sessions and stories.
        """
        view_window = Toplevel(self.master)
        view_window.geometry("900x600")
        view_window.title("View All Statistics")

        # Label for the window
        Label(view_window, text="All Session Statistics", font=("Arial", 14)).pack(pady=10)

        # Create a frame for search and date selection
        search_frame = Frame(view_window)
        search_frame.pack(pady=10, fill='x')

        # Label and entry for student search
        Label(search_frame, text="Search Student ID:", font=("Arial", 10)).grid(row=0, column=0, padx=10)
        search_var = StringVar()
        Entry(search_frame, textvariable=search_var, font=("Arial", 10)).grid(row=0, column=1, padx=10)

        # Date selection for improvement tracking
        Label(search_frame, text="Start Date:", font=("Arial", 10)).grid(row=0, column=2, padx=10)
        start_date = DateEntry(search_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        start_date.grid(row=0, column=3, padx=10)

        Label(search_frame, text="End Date:", font=("Arial", 10)).grid(row=0, column=4, padx=10)
        end_date = DateEntry(search_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        end_date.grid(row=0, column=5, padx=10)

        # Button to trigger improvement search
        Button(search_frame, text="View Improvement", command=lambda: self.show_improvement(search_var.get(), start_date.get_date(), end_date.get_date())).grid(row=0, column=6, padx=10)

        # Create a Treeview widget to display the statistics in a table
        columns = ("ID", "StudentID", "AvgReadingSpeed", "AvgAccuracy", "Date")

        tree = ttk.Treeview(view_window, columns=columns, show="headings", height=20)
        tree.heading("ID", text="ID")
        tree.heading("StudentID", text="Student ID")
        tree.heading("AvgReadingSpeed", text="Avg Reading Speed (WPM)")
        tree.heading("AvgAccuracy", text="Avg Accuracy (%)")
        tree.heading("Date", text="Date")

        tree.column("ID", width=50, anchor='center')
        tree.column("StudentID", width=100, anchor='center')
        tree.column("AvgReadingSpeed", width=150, anchor='center')
        tree.column("AvgAccuracy", width=150, anchor='center')
        tree.column("Date", width=100, anchor='center')

        tree.pack(pady=20, padx=20, expand=True, fill='both')

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(view_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)

        # Fetch and display all stats
        stats = self.student_db.fetch_all_stats()
        for stat in stats:
            tree.insert("", "end", values=stat)

        # Add search functionality
        def search_stats(event):
            query = search_var.get().lower()
            tree.delete(*tree.get_children())
            for stat in stats:
                if query in str(stat[1]).lower():  # Search in StudentID
                    tree.insert("", "end", values=stat)

        search_var.trace_add("write", lambda name, index, mode, sv=search_var: search_stats(None))

        # Display aggregated stats
        agg_stats = self.student_db.fetch_aggregated_stats()
        if agg_stats:
            Label(view_window, text=f"Overall Avg Speed: {agg_stats[0]:.2f} WPM, Overall Avg Accuracy: {agg_stats[1]:.2f}%", font=("Arial", 12)).pack(pady=10)

    def show_improvement(self, student_id, start_date, end_date):
        if not student_id:
            messagebox.showwarning("Warning", "Please enter a Student ID")
            return

        improvement_data = self.student_db.fetch_user_improvement(student_id, start_date, end_date)
        
        if not improvement_data:
            messagebox.showinfo("Info", "No data found for the given period")
            return

        improvement_window = Toplevel(self.master)
        improvement_window.geometry("600x300")
        improvement_window.title(f"Improvement for Student {student_id}")

        # Create a Treeview for improvement data
        columns = ("Date", "AvgSpeed", "AvgAccuracy")
        tree = ttk.Treeview(improvement_window, columns=columns, show="headings", height=15)
        tree.heading("Date", text="Date")
        tree.heading("AvgSpeed", text="Avg Speed (WPM)")
        tree.heading("AvgAccuracy", text="Avg Accuracy (%)")

        tree.column("Date", width=100, anchor='center')
        tree.column("AvgSpeed", width=150, anchor='center')
        tree.column("AvgAccuracy", width=150, anchor='center')

        tree.pack(pady=20, padx=20, expand=True, fill='both')

        for data in improvement_data:
            tree.insert("", "end", values=(data[2], f"{data[0]:.2f}", f"{data[1]:.2f}"))

        # Calculate overall improvement
        if len(improvement_data) > 1:
            speed_improvement = improvement_data[-1][0] - improvement_data[0][0]
            accuracy_improvement = improvement_data[-1][1] - improvement_data[0][1]
            Label(improvement_window, text=f"Speed Improvement: {speed_improvement:.2f} WPM", font=("Arial", 12)).pack()
            Label(improvement_window, text=f"Accuracy Improvement: {accuracy_improvement:.2f}%", font=("Arial", 12)).pack()

def main():
    root = Tk()
    app = AdminHomePage(root)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()