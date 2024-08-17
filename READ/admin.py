from person import Person

class Admin(Person):

    def __init__(self,name,email,password,role): #adminID, assignedStudents
        super().__init__(name,email,password,role)
        #self.adminID = adminID
        #self.assignedStudents = []

    
    def addStory(self, story):
        pass

    def removeStory(self, story):
        pass

    def GeneratePDF(self):
        pass

    def searchForStudent(self,student):
        pass

    def viewStatitics(self):  #view stats of all assigned students
        pass

    def addStudentToList(self, student): #add student to assigned list of students
        pass

    