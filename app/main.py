import json
from datetime import datetime, timedelta
import random
import calendar
import sys
from flask import Flask, request
from flask_cors import CORS

from subjects import Subject
from schedule import Schedule
from periods import Period
from section import section
from faculty import Faculty

app = Flask(__name__)
CORS(app)

def getStartingTime():
    return datetime.strptime("09:30", '%H:%M')


def getDayNameFromNumber(dayNumber):
    return calendar.day_name[dayNumber]


def getFreePeriod(subjectList, timing, facList):
    random.shuffle(subjectList)
    for sub in subjectList:
        resp, facName = sub.addNewTimingAnyFaculty(timing, facList)
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
    return json.dumps(jsonData)


def loadDataFromJson(data):

    duration = data['duration']
    totalClasses = data['no_of_classes']
    totalDays = data['no_of_days']
    totalSections = data['no_of_section']
    subjectsData = data['subjects']

    return duration, totalClasses, totalDays, totalSections, subjectsData


def copyFacultyList(facList):
    newList = []
    for fac in facList:
        temp = Faculty(fac.getFacultyName())
        newList.append(temp)
    return newList


def addBreakTime(currentTime, normalPeriodDuration, noOfClasses, breakDuration=30):
    noc = noOfClasses
    if noc%2!=0:
        noc+=1
    startingTime = getStartingTime() + timedelta(minutes=noc *
                                                 normalPeriodDuration/2)
    if currentTime != startingTime:
        return None
    endTiming = startingTime + timedelta(minutes=breakDuration)
    return Period(
        subjectName="Break Time",
        facultyName="",
        starting_time=startingTime,
        ending_time=endTiming)

@app.route("/generate", methods=['POST'])
def main():
    duration, totalClasses, totalDays, totalSections, subjectsData = loadDataFromJson(request.get_json())

    starting_time = getStartingTime()
    classInterval = timedelta(minutes=duration)

    avgClasses = totalClasses * totalDays / len(subjectsData)

    subjects = []
    facultyList = []

    for subj in subjectsData:
        temp = Subject(subj['subject_name'], avgClasses)
        for fac in subj['faculty_list']:
            temp.addFaculty(fac)
            facultyList.append(Faculty(fac))
        subjects.append(temp)

    subjects2 = []
    facList = []
    for _ in range(totalDays):
        subjects2.append(subjects)
        facList.append(copyFacultyList(facultyList))
        

    sectionsList = []
    for sec in range(totalSections):
        weekSchedule = section(sec)

        for s in subjects:
            s.clearAllotments()

        for day in range(totalDays):
            sch = Schedule(day)
            starting_time = getStartingTime()
            subjects = subjects2[day]

            if day>0:
                subjects = subjects2[day-1]

            for classes in range(totalClasses):

                breakTime = addBreakTime(
                    currentTime=starting_time,
                    normalPeriodDuration=duration,
                    noOfClasses=totalClasses)
                if breakTime != None:
                    sch.addPeriod(breakTime)
                    starting_time = breakTime.endingTime

                subjN, facN = getFreePeriod(subjects, starting_time, facList[day])
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

    rt = displayData(sectionsList)
    return rt


if __name__ == "__main__":
    app.run()
