import os
from distutils.dir_util import copy_tree


RASPBERRY_PI_DATA_DIR = "/Volumes/pi/Documents/iTPMS/MeasurementUnit/data/"
LOCAL_DATA_DIR = "/Users/macbook/Documents/projects/iTPMS-canyon/data_evaluation/data/"
LOCAL_EVAL_DIR = "/Users/macbook/Documents/projects/iTPMS-canyon/data_evaluation/eval/"
EXCLUDE_LIST = ['.DS_Store']


def get_newest_data():
    """
        Copy newest measurement data stored the raspberry pi to local directory.
        Creates a new eval directory for every new mesurement.
        This function requires to connect to samba server on raspberry pi 
        in advanced.
    """
    # Check if Raspberry Pi is connected
    if not os.path.isdir("/Volumes/pi/"):
        raise IOError("Pi not connected.")
    
    dir_list_pi = os.listdir(RASPBERRY_PI_DATA_DIR)
    dir_list_local = os.listdir(LOCAL_DATA_DIR)

    # Get only the directories, that not already exists on local machine.
    new_dirs = list(set(dir_list_pi) - set(dir_list_local))

    # Remove all dirs in exclude list.
    for dir in EXCLUDE_LIST:
        if dir in new_dirs:
            new_dirs.remove(dir)

    if len(new_dirs) == 0:
        print("No new directories found.")
        return
    else:
        print("New directories found. Start to copy:")
        for dir in new_dirs:
            print(dir)
            copy_tree(RASPBERRY_PI_DATA_DIR + dir, LOCAL_DATA_DIR + dir)
            create_new_eval_dir(dir)

        print("Copied",len(new_dirs), "new measurement(s) to local machine.")
        return

def get_latest_dir():
    """Returns the newsest data dir with measurements."""
    dirs = sorted(os.listdir(LOCAL_DATA_DIR))
    if len(dirs)>0:
        return dirs[-1]
    return None

def create_new_eval_dir(dir: str):
    """Creates new folder in eval directory, where figures can be stored."""
    curr_path = LOCAL_EVAL_DIR + dir
    if not os.path.exists(curr_path):
        os.makedirs(curr_path)