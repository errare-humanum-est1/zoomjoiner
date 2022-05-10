#!/usr/bin/env python

import time, json, platform
from selenium import * 
from selenium import webdriver

def dicttemplate(teacherName, callName, link): 
    return dict(
        {
                "name": teacherName,
                "call_name": callName,
                "link": link
        }    
)

with open("config.json", "r") as configFile:
    config = json.load(configFile)

#open teachers json
with open("timetable_teachers.json", "r") as teacherFile:
    infoDict = json.load(teacherFile)

#open browser depending on operating system
if platform.system() == "Linux":
    browser = webdriver.Firefox()
elif platform.system() == "Windows":
    browser = webdriver.Chrome("C:\\.programming\\drivers_extra_data\\chromedriver.exe")
else: raise NameError("what sys r u running on mate? try installing firefox!")

browser.get(config["school_website_url"])
time.sleep(3)

#find id and password
browser.find_element_by_name("u").send_keys(config["intranet_username"])
browser.find_element_by_name("p").send_keys(config["intranet_password"])

#click login
browser.find_element_by_xpath("//*[@id='dw__login']/div/fieldset/button").click()

#finding the url's
teacher_element_list = browser.find_elements_by_class_name("urlextern")

#deleting the teacher entrys
infoDict["teachers"].clear()

#formatting the teachers names and writing them in the dict
for element in teacher_element_list:
    if "https://zoom.us/j/" in element.get_attribute("href"):

        print(element.text)
        name = element.text.split()

        name.reverse()
        
        match len(name):
            case 1:
                lastName = shortName = f"{name[0]}"
            case 2:
                shortName = f"{name[0][0]}. {name[1][:-1]}"
                lastName = f"{name[1][:-1]}"
            case 3:
                shortName = f"{name[1]} {name[2][:-1]} {name[0]}"
                lastName = f"{name[2][:-1]}"

        infoDict["teachers"].append(
            dicttemplate(
                shortName, 
                lastName, 
                element.get_attribute('href')
                )
            )

# saving the json file
with open ('timetable_teachers.json', 'w') as teacherFile:
    json.dump(infoDict, teacherFile, indent=4)

browser.quit()