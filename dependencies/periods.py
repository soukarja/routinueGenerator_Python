class Period:
    def __init__(self, subjectName, facultyName, starting_time, ending_time):
        self.subjectName = subjectName
        self.facultyName = facultyName
        self.startingTime = starting_time
        self.endingTime = ending_time

    def getSubject(self):
        return self.subjectName

    def getFaculty(self):
        return self.facultyName

    def getStartingTime(self):
        return str(self.startingTime.hour)+":"+str(self.startingTime.minute)

    def getEndingTime(self):
        return str(self.endingTime.hour)+":"+str(self.endingTime.minute)

