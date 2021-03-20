import time, json, platform
import data
from selenium import webdriver

def dicttemplate(tn, cn, l): 
    return dict(
        {
                "name": tn,
                "call_name": cn,
                "link": l
        }    
)
#get login id
my_username = data.userdata.intranet_tim_username
my_password = data.userdata.intranet_tim_password
#open teachers json
with open("tts.json", "r") as teacherf:
    file = json.load(teacherf)
#open browser depending on operating system
if platform.system() == "Linux":
    browser = webdriver.Firefox()
elif platform.system() == "Windows":
    browser = webdriver.Chrome("C:\\.programming\\drivers_extra_data\\chromedriver.exe")
else: raise NameError("what sys r u running on mate? try installing firefox!")
browser.get(data.info.school_website_url())
time.sleep(3)
#find id and password
id_box = browser.find_element_by_name('u')
pass_box = browser.find_element_by_name('p')
#send login info
id_box.send_keys(my_username)
pass_box.send_keys(my_password)
#click login
login_button = browser.find_element_by_xpath("//*[@id='dw__login']/div/fieldset/button")
login_button.click()
#finding the url's
teacher_element_list = browser.find_elements_by_class_name("urlextern")
#deleting the teacher entrys
for l in range(len(file["teachers"])):
    file["teachers"].pop(0)
#formatting the teachers names and writing them in the dict
for element in teacher_element_list:
    if "," in element.text:
        print(element.text)
        t = element.text
        comma = t.find(",")
        fl = t[comma + 2]
        n = t[:comma]
        
        nice_name = fl + ". " + n
        call_name = t
        link = element.get_attribute('href')
        
        teacherd = dicttemplate(nice_name, call_name, link)
        file["teachers"].append(teacherd)
# saving the json file
with open ('tts.json', 'w') as teacherf:
    json.dump(file, teacherf, indent=4)
browser.quit()