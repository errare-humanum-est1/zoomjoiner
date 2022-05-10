#!/usr/bin/env python

import os, platform

systemArchitecture = platform.system()

if systemArchitecture == "Windows":
    from pywinauto import Desktop #type: ignore

import json, time, webbrowser, urllib.request, platform, pyautogui, subprocess
from edupage_api import *
from datetime import datetime as dt, timedelta as td
from termcolor import colored as cl


#defs
def clearTerminal():
    os.system("cls" if systemArchitecture == "Windows" else "clear")

def connectToMeeting(link):
    try:
        webbrowser.open(link, new = 2, autoraise = False) 
        print(cl("connecting...", "green"))
    
    except Exception as e: 
        print(cl("there has been an error while connecting", "red"))
        print(e)

def connection():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except Exception:
        return False

def progressBar(current, total, barLength = 20, prefix="Progress: ", postfix="sec"):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print(f"{prefix}[{arrow}{spaces}] {current}/ {total} {postfix}", end='\r')



clearTerminal()


#checks for internet connection, doesnt let go unless its there
while True:
    if connection():
        break
    time.sleep(30)

#loads info json
with open(f"{os.getcwd()}/timetable_teachers.json", "r") as f:
    info = json.load(f)

#access to information 
with open(f"{os.getcwd()}/config.json", "r") as file:
    config = json.load(file)

#declaring some variables
application_start_time = dt.now()
week_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

print("start time: ", dt.now().time())

rep = 0
while True:
    now = dt.now()
    in_lesson = False
    #looks up your open windows(linux)
    if systemArchitecture == "Linux": 
        proc = subprocess.Popen(["wmctrl -l"], stdout=subprocess.PIPE, shell=True, text=True)
        (out, err) = proc.communicate()
        
        if "Zoom Meeting" in out or "Room" in out:
            in_lesson = True

    #looks up your open windows (windows)
    elif systemArchitecture == "Windows": 
        os.chdir(os.getcwd())
        windows = Desktop(backend="uia").windows()
        for w in windows:
            #checks if you're in a lesson
            if "Zoom Meeting" in w.window_text() or "Breakout" in w.window_text():
                in_lesson = True

    if pyautogui.locateOnScreen('pictures/waiting_for_teacher.png') != None:
        in_lesson = True

    if in_lesson: 
        print("you are currently connected to %s, subject %s" % (currentConnection[0], currentConnection[1]))

    currentConnection = []

    #weekend detection
    if week_days[now.weekday()] == "saturday" or week_days[now.weekday()] == "sunday":
        print("it's saturday you idiot" if now.weekday() == 6 else "it's saturday you idiot")
        weekend = True
        break
    
    lessonpos = 0
    if not in_lesson:
        #sets time, clears output
        joinTime = False
        clearTerminal()
                
        print("current time: ", now.time())
        
        #checks if its time to join a lesson
        for index, lessonStartTime in enumerate(info["starttimes"][config["group"]]):
            lessonStartTime = dt.strptime(lessonStartTime, '%H:%M')

            if (lessonStartTime - td(minutes=config["pre_connect"])).time() <= now.time() <= (lessonStartTime + td(minutes=config["conn_period"])).time():
                lookup_day = week_days[int(now.weekday())]
                lessonpos = index
                joinTime = True
                break

        #looks up lesson
        if joinTime:
            if len(info["timetable"][lookup_day]) < lessonpos: break

            lesson = info["timetable"][lookup_day][lessonpos]

            #gets teacher
            connectToTeacher = info["subjects"][lesson]
            
            for teacher in info["teachers"]:
                if not connectToTeacher in teacher["name"]:
                    continue
                
                #connects to teacher
                currentConnection = [connectToTeacher, lesson]
                connectToMeeting(teacher["link"])
                print("you're being connected to %s, and your lesson is %s" % (connectToTeacher, lesson))
                
    
    #tells you how long programm has been runnung
    print(f"\nthis is rep: {rep}")
    run_time = str(now - application_start_time)
    run_time_stripped = run_time[:9]
    print(f"programm is on since: {run_time_stripped}\n")
    rep += 1

    #that fancy-ass progressbar
    for l in range(60):
        progressBar(l, 60, 50, "Waiting...")
        time.sleep(1)
    if platform.system() == "Linux": clearTerminal()
    elif platform.system() == "Windows": clearTerminal()                        


#tells you that you're done, if you're done
print()
print(cl("good news, you're done for today", "green"))
time.sleep(5)
os.exit(1)