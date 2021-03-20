try: 
    import data
    import json, os, time, webbrowser, urllib.request, platform
    from edupage_api import *
    from datetime import datetime as dt, timedelta as td
    from termcolor import colored as cl
    if platform.system() == "Windows":
        from pywinauto import Desktop
except ImportError: print("PLEASE READ THE REQUIREMENTS, FOUND IN THE README, AND INSTALL THE MODULES LISTED") 

info = data.info()
userdata = data.userdata

def check_conn(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

def progressBar(current, total, barLength = 20, prefix="Progress: ", color="green"):
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
    except Exception as e: 
        print(cl("there has been an error while connecting", "red"))
        errprint = "error: " + e
        print(cl(errprint, "red"))

internet_connection = check_conn()

if not internet_connection: 
    print("no internet!")
    raise ConnectionError("no internet connection")

with open("tts.json", "r") as f:
    tts = json.load(f)

application_start_time = dt.now()
week_days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
lesson_lengh = 40
my_group = "group 1"
my_username = userdata.edupage_tim_username
my_password = userdata.edupage_tim_password
subdomain = userdata.edupage_subdomain

edupage = Edupage(subdomain, my_username, my_password)

try:
    edupage.login()
except BadCredentialsException:
    print("Wrong username or password!")
except LoginDataParsingException:
    print("Try again or open an issue!")
if not edupage.is_logged_in:
    raise ConnectionError("couldn't connect to edupage")

print("is logged in: ", edupage.is_logged_in)
if edupage.is_logged_in:
    print("my user id:", edupage.get_user_id())

    dates = edupage.get_available_timetable_dates()
    timetable = edupage.get_timetable(dates)
    if timetable == None: pass
    else: print("timetable: ", timetable)

day_finished = False 
weekend = False
curr_conn = []
in_lesson = False
rep = 0
while True:
    now = dt.now()
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")
    
    print("current time: ", now.time())
    if in_lesson:
        print("you are currently connected to %s, subject %s" % (curr_conn[0], curr_conn[1]))

    if platform.system() == "Linux": 
        os.chdir("/mnt/Windows/.programming/programms/zoomjoiner")


        os.system("wmctrl -l > windows.txt")
        with open ("windows.txt", "r") as f:
            windows = f.readlines()
        
        for line in windows:
            if "Zoom Meeting" in line:
                in_lesson = True

    elif platform.system() == "Windows": 
        os.chdir("C:/.programming/programms/zoomjoiner")
        windows = Desktop(backend="uia").windows()

        for w in windows:
            if "Zoom Meeting" in w.window_text():
                in_lesson = True

    if in_lesson == True: print(cl("you are currently in a lesson, we will leave you alone", "yellow"))


    times =[]
    lessonpos = 0
    for t in tts["starttimes"][my_group]:
        t = dt.strptime(t, '%H:%M')
        times.append(t)
    for t in times:
        tend = t + td(minutes = lesson_lengh)
        check_time = is_hour_between(t.time(), tend.time(), now.time())
        if check_time: break
        lessonpos += 1
    
    if check_time and week_days[now.weekday() == "friday"]: 
        last = info.return_last_friday()
        if last == "English":
            lookup_day = "fridayB"
        elif last == "French":
            lookupday = "fridayA"
    else: lookup_day = week_days[int(now.weekday())] + "A"
    
    if week_days[now.weekday() == "saturday"] or week_days[now.weekday() == "sunday"]:
        print("it's saturday you idiot" if now.weekday() == 6 else "it's saturday you idiot")
        weekend = True
        break
    if not weekend and not in_lesson and check_time: 
        lesson = get_lesson(lookup_day, lessonpos)
        if lesson == None: 
            day_finished = True
            break
        if not day_finished:    
            teacher = tts["subjects"][lesson]
            for tea in tts["teachers"]:
                if teacher in tea["name"]:
                    curr_conn = [teacher, lesson]
                    print("you're being connected to %s, and your lesson is %s" % (teacher, lesson))
                    connect(tea["link"])
        
            if week_days[now.weekday() == "friday"] and lesson == "English" or lesson == "French":
                info.set_lastfriday(lesson)
    
    print()
    print("this is rep: ", rep)
    run_time = str(now - application_start_time)
    run_time_stripped = run_time[:9]
    print("programm is on since: ", run_time_stripped)
    print()
    rep += 1

    for l in range(61):
        progressBar(l, 60, 50, "Waiting...")
        time.sleep(1)
    if platform.system() == "Linux": os.system("clear")
    elif platform.system() == "Windows": os.system("cls")


print()
print(cl("good news, you're done for today", "green"))

#TO-DO
#edupage support