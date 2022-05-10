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


def displayData(sectionsList):
    jsonData = {}
    jsonData['schedule'] = []
    for x in sectionsList:
        print("Section: ", chr(x.getSectionNumber()+65))
        temp = {}
        temp['section_no'] = x.getSectionNumber()
        temp['section_name'] = chr(x.getSectionNumber()+65)
        temp['days'] = []
        for s in x.getSchedule():
            print("Weekday: ", getDayNameFromNumber(s.getWeekday()))
            t2 = []
            for index, t in enumerate(s.getPeriodList()):
                t3 = {}
                print(f"Period {index+1}) ", t.getSubject(),
                      t.getFaculty(), t.getStartingTime())
                t3['period_no'] = index
                t3['subject_name'] = t.getSubject()
                t3['faculty_name'] = t.getFaculty()
                t3['starting_time'] = t.getStartingTime()
                t3['ending_time'] = t.getEndingTime()
                t2.append(t3)
            temp['days'].append(t2)
            print("\n\n")
        jsonData['schedule'].append(temp)
    print(json.dumps(jsonData))


def loadDataFromJson():
    dataFile = open('data.json')
    data = json.load(dataFile)

    duration = data['duration']
    totalClasses = data['no_of_classes']
    totalDays = data['no_of_days']
    totalSections = data['no_of_section']
    subjectsData = data['subjects']
    dataFile.close()

    return duration, totalClasses, totalDays, totalSections, subjectsData


def addBreakTime(currentTime, normalPeriodDuration, noOfClasses, breakDuration=30):
    startingTime = getStartingTime() + timedelta(minutes=noOfClasses *
                                                 normalPeriodDuration//2)
    if currentTime != startingTime:
        return None
    endTiming = startingTime + timedelta(minutes=breakDuration)
    return Period(
        subjectName="Break Time",
        facultyName="",
        starting_time=startingTime,
        ending_time=endTiming)


if __name__ == "__main__":

    duration, totalClasses, totalDays, totalSections, subjectsData = loadDataFromJson()

    starting_time = getStartingTime()
    classInterval = timedelta(minutes=duration)

    avgClasses = totalClasses * totalDays / len(subjectsData)
    # print("avgClasses", avgClasses)

    subjects = []
    for subj in subjectsData:
        temp = Subject(subj['subject_name'], avgClasses)
        for fac in subj['faculty_list']:
            temp.addFaculty(fac)
        subjects.append(temp)

    subjects2 = []
    for _ in range(totalDays):
        subjects2.append(subjects)
        

    sectionsList = []
    for sec in range(totalSections):
        weekSchedule = section(sec)

        for s in subjects:
            s.clearAllotments()

        for day in range(totalDays):
            sch = Schedule(day)
            starting_time = getStartingTime()
            subjects = subjects2[day]
            for s in subjects:
                s.clearTimings()

            for classes in range(totalClasses):

                breakTime = addBreakTime(
                    currentTime=starting_time,
                    normalPeriodDuration=duration,
                    noOfClasses=totalClasses)
                if breakTime != None:
                    sch.addPeriod(breakTime)
                    starting_time = breakTime.endingTime

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
        subjects2[day] = subjects

    displayData(sectionsList)
