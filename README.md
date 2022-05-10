# zoomjoiner

rename the example files to config.json and timetable.json

add your timetable to the timetable list in timetable.json
add the names of the teachers for the subjects you put in your timetable list
either add the links to those teachers manually or use the "get_zoom_links" script after specifying your information in the config.json file

change the start times for your lessons in the timetable.json file to the times where your lessons start.
you can add an unlimited amount of lessons, but you need to make sure to add empty strings if you dont have a lesson in beteen of to lessons
you dont need to add empty strings at the end of the list

then run the zoom_connector.py script
it will automatically open the link to your lesson, the browser will transfer into the zoom app on your device

# requirements:

you can install the requirements from your commandline/ terminal with:

`cd zoomjoiner/`
and then:
`pip install -r requirements.txt`
