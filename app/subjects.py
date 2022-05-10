import random

class Subject:
    
    def __init__(self, subject_name, maxAllotments):
        self.subjectName = subject_name
        self.facultyName = []
        # self.allotedTimes = {}
        self.currAllotments = 0
        self.maxAllotments = maxAllotments

    def getSubjectName(self):
        return self.subjectName

    def getFacultyName(self):
        return self.facultyName

    def addFaculty(self, faculty_name):
        self.facultyName.append(faculty_name)

    def getAllFaculty(self):
        return self.facultyName

    def addNewTiming(self, faculty_name, new_timing, facList):
        if self.isTimeConflicting(faculty_name, new_timing, facList):
            return False
            
        # self.allotedTimes[faculty_name].append(new_timing)
        self.addFacultyTiming(faculty_name, facList, new_timing)

        # self.currAllotments += 1
        return True

    def addNewTimingAnyFaculty(self, new_timing, facList):
        faculties = self.getAllFaculty()
        random.shuffle(faculties)
        for fac in faculties:
            if self.addNewTiming(fac, new_timing, facList):
                return True,fac
        return False,""

    
    # def getAllTimings(self):
    #     return self.allotedTimes

    def getFacultyTiming(self, faculty_name, facultyList):
        for fac in facultyList:
            if faculty_name == fac.getFacultyName():
                return fac.getFacultyTiming()

        return []

    def addFacultyTiming(self, faculty_name, facultyList, newTiming):
        for fac in facultyList:
            if faculty_name == fac.getFacultyName():
                return fac.addTiming(newTiming)

        return False

    def isTimeConflicting(self, faculty_name, newTime, facultyList):
        return newTime in self.getFacultyTiming(faculty_name, facultyList) or self.currAllotments >= self.maxAllotments

    # def clearTimings(self):
    #     self.allotedTimes = {}
    #     for fac in self.getAllFaculty():
    #         self.allotedTimes[fac] = []

    def clearAllotments(self):
        self.currAllotments = 0