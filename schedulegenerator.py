import json
from datetime import datetime, timedelta
import random

from subjects import Subject
from schedule import Schedule
from periods import Period


def getFreePeriod(subjectList, timing):
    random.shuffle(subjectList)
    for sub in subjectList:
        if sub.addNewTiming(timing):
            return sub
    
    return Subject("", "")




if __name__ == "__main__":

    dataFile = open('data.json')
    data = json.load(dataFile)

    duration = data['duration']
    totalClasses = data['no_of_classes']
    totalDays = data['no_of_days']
    totalSections = data['no_of_section']
    subjectsData = data['subjects']

    starting_time = datetime.strptime("09:30", '%H:%M')
    # dateTimeObj = datetime().now().time()
    classInterval = timedelta(minutes=duration)



    subjects = []
    for subj in subjectsData:    
        for fac in subj['faculty_list']:
            temp = Subject(subj['subject_name'], fac)
            subjects.append(temp)

    weekSchedule = []
    for day in range(totalDays):
        sch = Schedule(day)
        for classes in range(totalClasses):
            
            per = Period(
                subject=getFreePeriod(subjects, starting_time),
                starting_time=starting_time,
                ending_time=starting_time+classInterval)

            sch.addPeriod(per)
            starting_time = starting_time+classInterval
            weekSchedule.append(sch)
        # print(per.getSubject().getSubjectName(), per.getSubject().getFacultyName(), per.getSubject().getAllTimings())

    for t in weekSchedule[0].getPeriodList():
        print(t.getSubject().getSubjectName(), t.getSubject().getFacultyName())


    # for t in weekSchedule

    dataFile.close()
