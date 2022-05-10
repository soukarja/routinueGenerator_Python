class Faculty:
    def __init__(self, facultyName) -> None:
        self.facultyName = facultyName
        self.timimg = []

    def addTiming(self, newTime):
        if not self.isBusy(newTime):
            self.timimg.append(newTime)
            return True

        return False

    def isBusy(self, newTime):
        return newTime in self.timimg

    def getFacultyName(self):
        return self.facultyName

    def getFacultyTiming(self):
        return self.timimg
