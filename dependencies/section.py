from typing import List
from schedule import Schedule

class section:

    def __init__(self, sectionNo) -> None:
        # self.periodList = periodList
        self.schedules = []
        self.sectionNumber = sectionNo
    
    def addSchedule(self, schedule):
        self.schedules.append(schedule)

    def getSchedule(self)->List[Schedule]:
        return self.schedules

    def getSectionNumber(self):
        return self.sectionNumber