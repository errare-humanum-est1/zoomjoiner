#!/usr/bin/env python

import os, platform
try: 
    import data
    import json, time, webbrowser, urllib.request, platform, pyautogui
    from edupage_api import *
    from datetime import datetime as dt, timedelta as td
    from termcolor import colored as cl
    import logging as lg
    if platform.system() == "Windows":
        from pywinauto import Desktop  # type: ignore (this makes pylance stfu and not show me a warning :) )
except ImportError:  
    if platform.system() == "Windows": os.system("pip install -r requirements.txt")
    elif platform.system() == "Linux": os.system("pip3 install -r requirements.txt")
    try:
        import data
        import json, time, webbrowser, urllib.request, platform, pyautogui
        from edupage_api import *
        from datetime import datetime as dt, timedelta as td #type:ignore
        from termcolor import cprint as cl #type:ignore
        import logging as lg
        if platform.system() == "Windows":
            from pywinauto import Desktop  # type: ignore (this makes pylance stfu and not show me a warning :) )
    except ImportError:
        print("TRY TO INSTALL THE REQUIREMENTS WITH: pip install -r requirements.txt !!!")

execdir = os.getcwd()

if not os.path.exists("logs"): os.mkdir("logs")
os.chdir(execdir + "/logs")

counter = 0
logtime = ""
unformattet = str(dt.now())
print("before: ", unformattet)
for x in unformattet: 
    if x == " ":
        x = "_"
    elif x == ".":
        break
    elif x == ":":
        x = "."
    logtime += x
    counter += 1
print("after: ", logtime)
logname = "log" + logtime + ".log"

# Create a custom logger
logger = lg.getLogger(__name__)

# Create handlers
c_handler = lg.StreamHandler()
f_handler = lg.FileHandler(logname)
c_handler.setLevel(lg.DEBUG)
f_handler.setLevel(lg.DEBUG)

# Create formatters and add it to handlers
c_format = lg.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = lg.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

os.chdir(execdir)

logger.debug("Programm Started.")

#defs
def check_conn(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except Exception:
        logger.warning("no internet connection recognized, check your connection or restart the programm")
        return False

def progressBar(current, total, barLength = 20, prefix="Progress: "):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print(prefix, '[%s%s] %d/ %d sec' % (arrow, spaces, current, total), end='\r')

def is_hour_between(start, end, fnow):
    is_between = False

    is_between |= start <= fnow <= end
    is_between |= end < start and (start <= fnow or fnow <= end)

    return is_between

def get_lesson(wday, lpos):
    if len(tts["timetable"][wday]) < lpos:
        return None
    else: return tts["timetable"][wday][lpos]

def connect(url):
    try:
        webbrowser.open(url, new = 2, autoraise = False) 
        print(cl("connecting...", "green"))
        logger.debug("connecting to: %s" % teacher)
    except Exception as e: 
        print(cl("there has been an error while connecting", "red"))
        print(e)
    if not got_shouted_at and breakup_logic:    
        print("hey sweetie, hope you have fun in ", lesson, " \U0001F618")

internet_connection = check_conn()
#checks for internet connection
if not internet_connection: 
    print("no internet!")
    raise ConnectionError("no internet connection")
#loads info json
my_path = os.getcwd()
with open(my_path + "/tts.json", "r") as f:
    tts = json.load(f)

#access to information script 
info = data.info()
userdata = data.userdata
#declaring some variables
application_start_time = dt.now()
week_days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

pre_connect = 2
conn_period = 30
lesson_lengh = 40
my_group = "group 1"
my_username = userdata.edupage_username
my_password = userdata.edupage_password
subdomain = userdata.edupage_subdomain

picture = 'pictures/waiting_for_teacher.png'
breakup_logic = False
curr_conn = []
day_finished = False 
got_shouted_at = False
rep = 0

#logs into edupage
edupage = Edupage(subdomain, my_username, my_password)
try:
    edupage.login()
except BadCredentialsException:
    print("Wrong username or password!")
    logger.debug("@edupage wrong credentials")
except LoginDataParsingException:
    print("@edupage something is wrong with the edupage api, contact the system administrator")
if not edupage.is_logged_in:
    raise ConnectionError("couldn't connect to edupage")
#checks if logged in in edupage and if there's timetables available
print("is logged in: ", edupage.is_logged_in)
if edupage.is_logged_in:
    print("my user id:", edupage.get_user_id())

    dates = edupage.get_available_timetable_dates()
    timetable = edupage.get_timetable(dates)
    if timetable == None: pass
    else: print("timetable: ", timetable)

now = dt.now()
print("start time: ", now.time())
active = False
while active:
    #sets time, clears output
    now = dt.now()
    in_lesson = False
    weekend = False
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")
    
    print("current time: ", now.time())

    #looks up your open windows(linux)
    if platform.system() == "Linux": 
        os.chdir(os.getcwd())
        os.system("wmctrl -l > windows.txt")
        with open ("windows.txt", "r") as f:
            windows = f.readlines()
        
        for line in windows:
            if "Zoom Meeting" in line or "Room" in line:
                in_lesson = True
                logger.debug("is on meeting")

        os.system("rm windows.txt")
    #looks up your open windows (windows)
    elif platform.system() == "Windows": 
        os.chdir(os.getcwd())
        windows = Desktop(backend="uia").windows()
        for w in windows:
            #checks if you're in a lesson
            if "Zoom Meeting" in w.window_text() or "Breakout" in w.window_text():
                in_lesson = True
                logger.debug("is in meeting")


    if pyautogui.locateOnScreen(picture) != None:
        in_lesson = True
        logger.debug("is in meeting")

    if in_lesson:
        try: 
            print("you are currently connected to %s, subject %s" % (curr_conn[0], curr_conn[1]))
        except IndexError: 
            if not got_shouted_at and breakup_logic:
                print(cl("DID YOU CHEAT ON ME?!", "red"))
                print(cl("YOU'RE CONNECTED BUT DIDN'T CONNECT USING ME?!", "red"))
                print(cl("I'M BREAKING UP WITH YOU!", "red"))
                print()
                got_shouted_at = True
            elif breakup_logic: print("you are single")

    #reads and formats the times
    times =[]
    lessonpos = 0
    for t in tts["starttimes"][my_group]:
        t = dt.strptime(t, '%H:%M')
        times.append(t)
    #checks for lessontime
    for t in times:
        tend = t + td(minutes = conn_period)
        t = t - td(minutes=pre_connect)
        check_time = is_hour_between(t.time(), tend.time(), now.time())
        if check_time: break
        lessonpos += 1
    
    #the goddamn friday eception
    if check_time and week_days[now.weekday()] == "friday": 
        last = info.return_last_friday()
        if last == "English":
            lookup_day = "fridayB"
        elif last == "French":
            lookupday = "fridayA"
        logger.debug("its friday")
    elif week_days[now.weekday()] == "friday": lookup_day = week_days[int(now.weekday())] + "A"
    else: lookup_day = week_days[int(now.weekday())]
    
    #weekend detection
    if week_days[now.weekday()] == "saturday" or week_days[now.weekday()] == "sunday":
        print("it's saturday you idiot" if now.weekday() == 6 else "it's saturday you idiot")
        weekend = True
        break
    
    #looks up lesson
    if not weekend and not in_lesson and check_time: 
        lesson = get_lesson(lookup_day, lessonpos)
        if lesson == None: 
            day_finished = True
            break
        #gets teacher
        if not day_finished:    
            teacher = tts["subjects"][lesson]
            for tea in tts["teachers"]:
                if teacher in tea["name"]:
                    #connects to teacher
                    curr_conn = [teacher, lesson]
                    print("you're being connected to %s, and your lesson is %s" % (teacher, lesson))
                    connect(tea["link"])
        
            if week_days[now.weekday()] == "friday" and lesson == "English" or lesson == "French":
                info.set_lastfriday(lesson)
    #tells you how long programm has been runnung
    print()
    print("this is rep: ", rep)
    run_time = str(now - application_start_time)
    run_time_stripped = run_time[:9]
    print("programm is on since: ", run_time_stripped)
    print()
    rep += 1
    #that fancy-ass progressbar
    for l in range(60):
        progressBar(l, 60, 50, "Waiting...")
        time.sleep(1)
    if platform.system() == "Linux": os.system("clear")
    elif platform.system() == "Windows": os.system("cls")
#tells you that you're done, if you're done
print()
print(cl("good news, you're done for today", "green"))