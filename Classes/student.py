class Student():        
    """
    Represents a student user in the reading assistance system.
    """

    def __init__(self,student_id,name,email,password,grade,reading_level): 
        """
        Initialize a Student object.

        Args:
            student_id (str): Unique identifier for the student.
            name (str): Student's name.
            email (str): Student's email address.
            password (str): Student's password.
            grade (int): Student's grade level.
            reading_level (str): Student's current reading level.
        """
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password = password
        self.grade = grade
        self.reading_level = reading_level

    def display_info(self):
        """
        Display the student's information.
        """
        print(f"Student ID: {self.student_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Grade: {self.grade}")
        print(f"Reading Level: {self.reading_level}")


