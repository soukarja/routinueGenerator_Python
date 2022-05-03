import json
from datetime import datetime, timedelta
import random
from re import sub

from subjects import Subject
from schedule import Schedule
from periods import Period
from section import section


def getFreePeriod(subjectList, timing):
    random.shuffle(subjectList)
    for sub in subjectList:
        resp, facName = sub.addNewTimingAnyFaculty(timing)
        if resp:
            return sub.getSubjectName(), facName
    
    return "empty", "empty"




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

    avgClasses = totalClasses * totalDays / len(subjectsData)
    print("avgClasses", avgClasses)

    subjects = []
    for subj in subjectsData:    
        temp = Subject(subj['subject_name'], avgClasses)
        for fac in subj['faculty_list']:
            temp.addFaculty(fac)
        subjects.append(temp)

    

    sectionsList = []
    for sec in range(totalSections):
        weekSchedule = section(sec)
        for day in range(totalDays):
            sch = Schedule(day)
            starting_time = datetime.strptime("09:30", '%H:%M')

            for s in subjects:
                s.clearTimings()

            for classes in range(totalClasses):
                subjN, facN = getFreePeriod(subjects, starting_time)
                per = Period(
                    subjectName=subjN,
                    facultyName=facN,
                    starting_time=starting_time,
                    ending_time=starting_time+classInterval)

                sch.addPeriod(per)
                starting_time = starting_time+classInterval
            # weekSchedule.append(sch)
            weekSchedule.addSchedule(sch)
        sectionsList.append(weekSchedule)
            # print(per.getSubject().getSubjectName(), per.getSubject().getFacultyName(), per.getSubject().getAllTimings())

    for x in sectionsList:
        print("Section: ", x.getSectionNumber()+1)
        for s in x.getSchedule():
            print("Weekday: ", s.getWeekday()+1)
            for t in s.getPeriodList():
                print(t.getSubject(), t.getFaculty(), t.getStartingTime())
            print("\n\n")

    # for t in weekSchedule

    dataFile.close()
