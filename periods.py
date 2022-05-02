from subjects import Subject

class Period:
    def __init__(self, subject, starting_time, ending_time):
        self.subject = subject
        self.startingTime = starting_time
        self.endingTime = ending_time

    def getSubject(self)->Subject:
        return self.subject


