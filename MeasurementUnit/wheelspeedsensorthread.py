from Documents.iTPMS.MeasurementUnit.sensorreader import SensorReader
from datalogger import DataLogger
from threading import Event
import RPi.GPIO as GPIO
import time
import numpy as np

class WheelSpeedSensorReader(SensorReader):

    def __init__(self, name: str, 
                 start_measurement_event: Event, 
                 terminated_event: Event, 
                 data_logger: DataLogger, 
                 gpio_signal_pin: int):
        super().__init__(name, start_measurement_event, terminated_event)

        self.data_logger = data_logger
        self.gpio_signal_pin = gpio_signal_pin
        
        # Set up GPIO-Pins for measurements.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_signal_pin, GPIO.IN)
        # Prepare internal data.
        self.timestamps = list()
        self.csv_header = "timestamps_rising_edge"

    def measurement_loop(self):
        while self.start_measurement_event.is_set():
            # Wait for an rising edge. Timeout: 1 sec.
            channel = GPIO.wait_for_edge(self.gpio_signal_pin, GPIO.FALLING, timeout=1000)
            if channel is not None:
                # Rising edge detected.
                # Save timestamp.
                timestamp = time.time()
                self.timestamps = self.timestamps.append(timestamp)
        
        # If there are new timestamps, write them to file.
        if len(self.timestamps) > 0:
            self.data_logger.write_measurements_to_file(
                np.array(self.timestamps),
                self.name,
                self.csv_header
            )
            # Reset internal data for next measurement.
            self.timestamps.clear()

        
    def magnet_detected_callback(self):
        pass

    #def clean_up(self):
        #GPIO.cleanup()