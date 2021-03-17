import data, connection
import json
from edupage_api import *
from datetime import datetime


internet_connection = connection.connect()
print("connected" if internet_connection else "no internet!")
if not internet_connection: raise ConnectionError("no internet connection")

with open("tts.json", "r") as f:
    tts = json.load(f)

my_group = "group 1"
my_username = data.edupage_tim.username()
my_password = data.edupage_tim.password()
subdomain = data.edupage.subdomain()

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
if data.system() == "Windows":
    now = datetime.datetime.now()
elif data.system() == "Linux":
    now = datetime.now()


while not timetable: 
    for meeting_time in tts ["starttimes"][my_group]:
        if meeting_time in now.strftime("%H:%M"):
            print("wake up, it's time for school man, c'mon")