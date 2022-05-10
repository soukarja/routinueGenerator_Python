import random

class Subject:
    
    def __init__(self, subject_name, maxAllotments):
        self.subjectName = subject_name
        self.facultyName = []
        self.allotedTimes = {}
        self.currAllotments = 0
        self.maxAllotments = maxAllotments

    def getSubjectName(self):
        return self.subjectName

    def getFacultyName(self):
        return self.facultyName

    def addFaculty(self, faculty_name):
        self.facultyName.append(faculty_name)
        self.allotedTimes[faculty_name] = []

    def getAllFaculty(self):
        return self.facultyName

    def addNewTiming(self, faculty_name, new_timing):
        if self.isTimeConflicting(faculty_name, new_timing):
            return False
            
        self.allotedTimes[faculty_name].append(new_timing)
        # self.currAllotments += 1
        return True

    def addNewTimingAnyFaculty(self, new_timing):
        faculties = self.getAllFaculty()
        random.shuffle(faculties)
        for fac in faculties:
            if self.addNewTiming(fac, new_timing):
                return True,fac
        return False,""

    
    def getAllTimings(self):
        return self.allotedTimes

    def isTimeConflicting(self, faculty_name, newTime):
        return newTime in self.allotedTimes[faculty_name] or self.currAllotments >= self.maxAllotments

    def clearTimings(self):
        self.allotedTimes = {}
        for fac in self.getAllFaculty():
            self.allotedTimes[fac] = []

    def clearAllotments(self):
        self.currAllotments = 0