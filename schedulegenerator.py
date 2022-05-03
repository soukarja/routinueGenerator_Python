import json
from datetime import datetime, timedelta
import random
import calendar
import sys

sys.path.insert(0, './dependencies')
from subjects import Subject
from schedule import Schedule
from periods import Period
from section import section


def getStartingTime():
    return datetime.strptime("09:30", '%H:%M')


def getDayNameFromNumber(dayNumber):
    return calendar.day_name[dayNumber]


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

    starting_time = getStartingTime()
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
        for s in subjects:
            s.clearAllotments()

        for day in range(totalDays):
            sch = Schedule(day)
            starting_time = getStartingTime()

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
            weekSchedule.addSchedule(sch)
        sectionsList.append(weekSchedule)

    for x in sectionsList:
        print("Section: ", chr(x.getSectionNumber()+65))
        for s in x.getSchedule():
            print("Weekday: ", getDayNameFromNumber(s.getWeekday()))
            for index,t in enumerate(s.getPeriodList()):
                print(f"Period {index+1}) ",t.getSubject(), t.getFaculty(), t.getStartingTime())
            print("\n\n")

    dataFile.close()
