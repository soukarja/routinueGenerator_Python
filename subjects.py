class Subject:
    
    def __init__(self, subject_name, faculty_name):
        self.subjectName = subject_name
        self.facultyName = faculty_name
        self.allotedTimes = []

    
    def getSubjectName(self):
        return self.subjectName

    def getFacultyName(self):
        return self.facultyName

    def addNewTiming(self, new_timing):
        if self.isTimeConflicting(new_timing):
            return False
            
        self.allotedTimes.append(new_timing)
        return True
    

    def getAllTimings(self):
        return self.allotedTimes

    def isTimeConflicting(self, newTime):
        return newTime in self.allotedTimes