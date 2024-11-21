class Story:
    
    def __init__(self,storyID,title,difficultyLevel):
        self.storyID = storyID
        self.title = title
        self.difficultyLevel = difficultyLevel

    def breakUpStory(self):
        pass
    def getStoryTitle(self):
        return self.title
    
    def getStoryDifficulty(self):
        return self.difficultyLevel
    
    def getStoryID(self):
        return self.storyID
    
    def setStoryDifficulty(self, difficulty):
        self.difficultyLevel = difficulty

    def setStoryTitle(self,title):
        self.title = title