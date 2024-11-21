
class Admin():
    """
    Represents an administrator with capabilities to manage stories and students.
    """
    def __init__(self, adminID,name, email, password):
        """
        Initialize an Admin object.

        Args:
            adminID (str): Unique identifier for the admin.
            name (str): Admin's name.
            email (str): Admin's email address.
            password (str): Admin's password.
        """
        self.adminID = adminID
        self.name = name
        self.email = email
        self.password = password
        

    def add_story(self, title: str, excerpt: str, body: str):
        """
        Add a new story to the database.

        Args:
            title (str): Title of the story.
            excerpt (str): Short excerpt or summary of the story.
            body (str): Full text of the story.
        """
        query = "INSERT INTO stories (title, excerpt, body) VALUES (?, ?, ?)"
        self.cursor.execute(query, (title, excerpt, body))
        self.connection.commit()
        print("Story added successfully!")

    def remove_story(self, story_id):
        """
        Remove a story from the database.

        Args:
            story_id (int): Unique identifier of the story to be removed.
        """
        query = "DELETE FROM stories WHERE id = ?"
        self.cursor.execute(query, (story_id,))
        self.connection.commit()
        print(f"Story with ID {story_id} removed successfully!")

    

    