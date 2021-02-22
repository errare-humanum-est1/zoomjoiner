import userdata
from edupage_api import Edupage

#my_username = userdata.edupage_tim.username
#my_password = userdata.edupage_tim.password

my_username = "xtialbe5"
my_password = "pzyyj1"


edupage = Edupage(my_username, my_password)
print(edupage.login())