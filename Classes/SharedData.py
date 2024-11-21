from typing import Optional
from student import Student

class SharedData:
    _instance = None
    _student: Optional[Student] = None
    _admin = None
    _session_status = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedData, cls).__new__(cls)
        return cls._instance

    @classmethod
    def set_student(cls, student: Student):
        cls._student = student

    @classmethod
    def get_student(cls) -> Optional[Student]:
        return cls._student

    @classmethod
    def set_admin(cls, admin):
        cls._admin = admin

    @classmethod
    def get_admin(cls):
        return cls._admin
    
    @classmethod
    def get_session_status(cls):
        return cls._session_status
    
    @classmethod
    def set_session_status(cls,status):
        cls._session_status = status