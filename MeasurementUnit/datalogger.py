from threading import Event, Lock
import os
import time
import logging

import numpy as np

from measurementunitcomponent import MeasurementUnitComponent

class DataLogger(MeasurementUnitComponent):

    def __init__(self, name: str, start_measurement_event: Event, terminated_event: Event, dir: str):
        super(DataLogger, self).__init__(name, start_measurement_event, terminated_event)
        
        self.dir = dir

        self.lock = Lock()
        # Check if data directory already exist, otherwise create new one.
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)

    def measurement_loop(self):
        """ Create new directory for current measurement
        and prepare internal variables for incoming 
        write_measurements_to_file calls."""
        # Create new folder for measurement with current timestamp.
        self.current_timestr = time.strftime("%Y%m%d-%H%M%S")
        self.current_dir = self.dir + "/" + self.current_timestr
        try:
            os.makedirs(self.current_dir)
        except FileExistsError:
            logging.exception("Directory '", self.current_dir , "' already exists.")
        finally:
            # Folder must be created only once per measurement. 
            # Check every second if the measurement is still running.
            while self.start_measurement_event.is_set():
                time.sleep(1)

        
    def write_measurements_to_file(self, data: np.array, device_name: str, csv_header: str):
        """
            Saves multidimensinal numpy array to csv file.
            This method is called by other sensor threads
            after they have collected their data.
        """
        with self.lock:
            file_name = device_name + "_" + self.current_timestr + ".csv"
            file_path = self.current_dir + "/" + file_name
            np.savetxt(file_path, data, header=csv_header, delimiter=",", comments="")
            logging.info(f"Write {len(data)} measurements to file.")
            