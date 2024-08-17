class ReadingMaterial:
    
    def __init__(self):
        self.stories = []

    def addStory(self, story):
        self.stories.append(story)

    def removeStory(self, story):
        self.stories.remove(story)

    def viewReadingMaterial(self):
        return self.stories