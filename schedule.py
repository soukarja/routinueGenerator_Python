class Schedule:

    def __init__(self, weekday):
        self.weekDay = weekday
        self.periodList  = []

    def addPeriod(self, period):
        self.periodList.append(period)

    def getPeriodList(self):
        return self.periodList

    

