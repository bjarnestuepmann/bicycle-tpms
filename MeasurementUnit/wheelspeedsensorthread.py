from basethread import BaseThread
from datalogger import DataLogger
from threading import Event
import RPi.GPIO as GPIO
import time
import numpy as np

class WheelSpeedSensorThread(BaseThread):

    def __init__(self, name: str, 
                 start_measurement_event: Event, 
                 terminated_event: Event, 
                 data_logger: DataLogger, 
                 gpio_gnd: int, 
                 gpio_v: int):
        super().__init__(name, start_measurement_event, terminated_event)

        self.data_logger = data_logger
        self.gpio_gnd = gpio_gnd
        self.gpio_v = gpio_v
        
        # Set up GPIO-Pins for measurements.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_v, GPIO.OUT)
        GPIO.setup(self.gpio_gnd, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(self.gpio_v, 1)
        # Prepare internal data.
        self.timestamps = np.zeros(shape=(0,1))
        self.csv_header = "timestamps_rising_edge"

    def measurement_loop(self):
        while self.start_measurement_event.is_set():
            # Wait for an rising edge. Timeout: 1 sec.
            channel = GPIO.wait_for_edge(self.gpio_gnd, GPIO.RISING, timeout=1000)
            if channel is not None:
                # Rising edge detected.
                # Save timestamp.
                timestamp = time.time()
                self.timestamps = np.vstack((self.timestamps, [timestamp]))
        
        # If there are new timestamps, write them to file.
        if self.timestamps.size > 0:
            self.data_logger.write_measurements_to_file(self.timestamps, self.name, self.csv_header)
            # Reset internal data for next measurement.
            self.timestamps = np.delete(arr=self.timestamps, obj=np.s_[:])

        
    def magnet_detected_callback(self):
        pass

    #def clean_up(self):
        #GPIO.cleanup()