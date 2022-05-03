from typing import List
from periods import Period
class Schedule:

    def __init__(self, weekday):
        self.weekDay = weekday
        self.periodList  = []

    def addPeriod(self, period):
        self.periodList.append(period)

    def getPeriodList(self)->List[Period]:
        return self.periodList

    def getWeekday(self):
        return self.weekDay

    

