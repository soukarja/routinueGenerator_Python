from subjects import Subject

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
        return self.startingTime

    def getEndingTime(self):
        return self.endingTime


