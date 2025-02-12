import psutil
import time
import playsound
import shutil
import os

from pptx.media import Video


def insert_listener():
    """Plays 'insert.mp3' if a USB or SD card is detected, then waits 5 sec and plays 'removenow.mp3'."""
    if any('removable' in p.opts for p in psutil.disk_partitions(all=True)):
        playsound.playsound("assets/audio/insert.mp3")


def move_files():
    #get drive logic
    source_dir = "Videos/"
    dest_dir = "Destination/"

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    while any(f.endswith((".mp4", ".mkv", ".MP4")) for f in os.listdir(source_dir)):
        for filename in os.listdir(source_dir):
            if filename.endswith((".mp4", ".mkv", ".MP4")):
                path = os.path.join("Videos/", filename)
                shutil.move(os.path.join(source_dir, filename), os.path.join(dest_dir, filename))

""" Plans:
        Insert listener:
            func that checks for dirs named GOPRO100 or MEDIA100 or similar (source dirs)
            Destination dir should be a folder named e.g. Vids or smth
                Inside the dest dir there should be a folder generated with the date of video creation
                    The video should be moved to the folder with the date of creation
                        If the folder with the date of creation already exists, the video should be moved there
        
        Web Interface:
            Simple button with either "move" or "Stream"
            If "move" is clicked, the insert listener should be activated
            If "Stream" is clicked, it should start another webserver with a Kodi-like interface
                That interface should get all connected Drives (USB, SD, HDD, SSD etc.) these should be displayed in a drop down menu
                    When clicked videos and folders should be shown like in explorer
                    Also there should be an actual Video player that can play the videos
"""



move_files()




