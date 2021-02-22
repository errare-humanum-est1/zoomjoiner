import os
import time
import json
import userdata
import datetime
from selenium import webdriver

link_changed = False
#get login id
my_username = userdata.intranet_tim.username()
my_password = userdata.intranet_tim.password()
#open teachers json
with open("teachers.json", "r") as teacherf:
    teacher = json.load(teacherf)
#open browser
driver = webdriver.Chrome("C:\\.programming\\drivers_extra_data\\chromedriver.exe")
driver.get('https://intern.kreisgymnasium-neuenburg.de/schueler/start')
time.sleep(3)
#find id and password
id_box = driver.find_element_by_name('u')
pass_box = driver.find_element_by_name('p')
#send login info
id_box.send_keys(my_username)
pass_box.send_keys(my_password)
#click login
login_button = driver.find_element_by_xpath("//*[@id='dw__login']/div/fieldset/button")
login_button.click()

for curr_teacher in teacher["teachers"]:
    print(curr_teacher["call_name"])
    #finding teachers link
    teachers_link_id = driver.find_element_by_link_text(curr_teacher["call_name"])
    teachers_link = teachers_link_id.get_attribute('href')
    #if link changed
    if teachers_link != curr_teacher["link"]:
        #change link
        curr_teacher["link"] = teachers_link
        #add the last link change time 
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        teacher["meta"]["last link change"] = str(now)
        print("link changed")
        link_changed = True
    print(curr_teacher["link"])
    print("")
#tell user that a link changed
print("AT LEAST ONE OF THE LINKS HAS CHANGED!")
#saving the json file
with open ('teachers.json', 'w') as teacherf:
    json.dump(teacher, teacherf, indent=4)