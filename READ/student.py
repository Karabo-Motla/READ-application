from person import Person

class Student(Person):

    def __init__(self,name,email,password,role): #age,studentID,grade,readingLevel
        super().__init__(name,email,password,role)
        #self.studentID = studentID
        #self.grade = grade
        #self.readingLevel = readingLevel

    def selectStory(self,storyID):
        print("")

    
    def PracticeReading(self,storyID): #start a session
        pass
    
    def startReading(self): #start recording audio
        pass

    def stopReading(self): #stop recording audio
        pass

    def endSession(self):  #end reading session
        pass

    def viewProgress(self): #extra feature to view pass and present stats
        pass

    #def getStudentID(self):
    #    pass

    #def setGrade(self):
    #    self.grade = grade

    #def setReadingLevel(self):
    #    self.readingLevel= readingLevel


