import os
import shutil
from distutils.dir_util import copy_tree


RASPBERRY_PI_DATA_DIR = "/Volumes/pi/Documents/iTPMS/MeasurementUnit/data"
LOCAL_DATA_DIR = "/Users/macbook/Documents/projects/iTPMS-canyon/data_evaluation/data"


def get_newest_data():
    """
        Copy newest measurement data stored the raspberry pi to local directory.
        This function requires to connect to samba server on raspberry pi 
        in advanced.
    """
    # Check if Raspberry Pi is connected
    if not os.path.isdir("/Volumes/pi/"):
        print("Raspberry Pi is not conncted.")
        return
    
    dir_list_pi = os.listdir(RASPBERRY_PI_DATA_DIR)
    dir_list_local = os.listdir(LOCAL_DATA_DIR)

    # Get only the directories, that not already exists on local machine.
    new_dirs = list( set(dir_list_pi) - set(dir_list_local))

    if len(new_dirs) == 0:
        print("No new directories found.")
        return
    else:
        print(len(new_dirs), "new directories found. Start to copy:")
        for dir in new_dirs:
            print(dir)
            copy_tree(RASPBERRY_PI_DATA_DIR + "/" + dir, LOCAL_DATA_DIR + "/" + dir)
        print("Copied", len(new_dirs), "new measurement to local machine.")
        
        return

get_newest_data()