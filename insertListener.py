import psutil
import time
import playsound
import shutil
import os
from pptx.media import Video


def insert_listener():
    if any('removable' in p.opts for p in psutil.disk_partitions(all=True)):
        move_files()
        playsound.playsound("assets/audio/insert.mp3")
    else:
        playsound.playsound("assets/audio/error-1.mp3")



def move_files():
    source_dirs = ["Videos/", "GOPRO100/", "MEDIA100/"]
    dest_dir = "Destination/"

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate over the source directories
    while any(f.endswith((".mp4", ".mkv", ".MP4")) for d in source_dirs if os.path.exists(d) for f in os.listdir(d)):
        for source_dir in source_dirs:
            # Skip if the directory doesn't exist
            if not os.path.exists(source_dir):
                continue

            for filename in os.listdir(source_dir):
                if filename.endswith((".mp4", ".mkv", ".MP4")):
                    timestamp = os.path.getmtime(source_dir + filename)
                    formatted_time = time.strftime("%d-%m-%Y", time.localtime(timestamp))
                    print(formatted_time)
                    destination_folder = os.path.join(dest_dir, formatted_time)
                    os.makedirs(destination_folder, exist_ok=True)
                    shutil.move(os.path.join(source_dir, filename), os.path.join(destination_folder, filename))
                    print(f"Moving {filename} to {dest_dir}...")


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



