#!/usr/bin/env python

import os, shutil, platform

if platform.system() == "Linux": 
    dir = os.environ["HOME"]
    folder = dir + "/.zoomjoiner"

elif platform.system() == "Windows": 
    dir = "C:/Programms"
    folder = dir + "/zoomjoiner"

get_directory = os.getcwd()

if os.path.exists(folder):
    shutil.rmtree(folder)

shutil.copytree(get_directory, folder)

if platform.system() == "Linux":
    dr = dir+"/.config/autostart/"
    file = dr+"zoomjoiner.desktop"
    exec = "Exec=./" + folder + "/start_the_thingy.sh"
    launcher = ["[Desktop Entry]", 
                "Name=Zoomjoiner", 
                "Comment=Automatically connects you to your zoom lessons, gets data from given timetable",
                exec, 
                "Type=Application", 
                "X-GNOME-Autostart-enabled=true"]

    if not os.path.exists(dr):
        os.makedirs(dr)

    if os.path.exists(file):
        os.remove(file)

    with open(file, "wt") as out:     
        for l in launcher:
            out.write(l+"\n")
elif platform.system() == "Windows": 
    print("has to create a link to the programm, not working yet")
    pass

print("finished")