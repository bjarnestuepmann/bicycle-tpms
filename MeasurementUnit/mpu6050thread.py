from basethread import BaseThread
from datalogger import DataLogger
from threading import Event
import smbus2
import numpy as np
import time

class MPU6050Thread(BaseThread):

    ACCEL_XOUT_ADDRESS = 0x3b
    ACCEL_YOUT_ADDRESS = 0x3d
    ACCEL_ZOUT_ADDRESS = 0x3f
    
    GYRO_XOUT_ADDRESS = 0x43
    GYRO_YOUT_ADDRESS = 0x45
    GYRO_ZOUT_ADDRESS = 0x47

    def __init__(self, name: str, start_measurement_event: Event, terminated_event: Event, data_logger: DataLogger, i2c_bus: int, address: int):
        super(MPU6050Thread, self).__init__(name, start_measurement_event, terminated_event)

        self.data_logger = data_logger
        self.i2c_bus = i2c_bus
        self.address = address

    def initilize(self):
        self.bus = smbus2.SMBus(self.i2c_bus)
        # Initialize MPU.
        self.bus.write_byte_data(self.address, 0x6b, 0)
        
        self.measurement_count = 7
        self.data_header = "timestamp,ACCEL_X,ACCEL_Y,ACCEL_Z,GYRO_X,GYRO_Y,GYRO_Z"
        self.data = np.zeros(shape=(0,self.measurement_count))

    def start_measurement(self):
        current_data = np.zeros(shape=self.measurement_count)
        raw_values = self.bus.read_i2c_block_data(self.address, 0x3b, 14)

        while self.start_measurement_event.is_set():
            np.put(current_data, 0, time.time())
            np.put(current_data, 1, self.combine_bytes_to_word(raw_values[1], raw_values[0]))
            np.put(current_data, 2, self.combine_bytes_to_word(raw_values[3], raw_values[2]))
            np.put(current_data, 3, self.combine_bytes_to_word(raw_values[5], raw_values[4]))
            np.put(current_data, 4, self.combine_bytes_to_word(raw_values[9], raw_values[8]))
            np.put(current_data, 5, self.combine_bytes_to_word(raw_values[11], raw_values[10]))
            np.put(current_data, 6, self.combine_bytes_to_word(raw_values[13], raw_values[12]))
            
            self.data = np.vstack((self.data, [current_data]))

        # Write measurement to file.
        self.data_logger.write_measurements_to_file(self.data, self.name, self.data_header)
        # Reset internal data for next measurement.
        self.data = np.delete(arr=self.data, obj=np.s_[:])
        
    def combine_bytes_to_word(self, low, high):
        """Concate two bytes and convert to integer."""
        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value