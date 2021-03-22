import json, platform
from datetime import datetime as dt

now = dt.now()

class userdata:
    intranet_username = "username"
    intranet_password = "password"
    
    edupage_subdomain = "your_subdomain"
    edupage_username = "your_username"
    edupage_password = "your_password"


class info:
    def school_website_url():
        return 'link to your schools website'