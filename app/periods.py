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
        return self.formatTimeValue(self.startingTime.hour)+":"+self.formatTimeValue(self.startingTime.minute)

    def getEndingTime(self):
        return self.formatTimeValue(self.endingTime.hour)+":"+self.formatTimeValue(self.endingTime.minute)

    def formatTimeValue(self, timeValue):
        if timeValue >= 10:
            return str(timeValue)
        
        return "0"+str(timeValue)


