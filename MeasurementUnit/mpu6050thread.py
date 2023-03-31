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

        # Connect to device.
        self.bus = smbus2.SMBus(self.i2c_bus)
        # Initialize MPU.
        self.bus.write_byte_data(self.address, 0x6b, 0)
        # Prepare internal data.
        self.measurement_count = 8
        self.data_header = "timestamp,RAW_ACCEL_X,RAW_ACCEL_Y,RAW_ACCEL_Z,RAW_TEMP,RAW_GYRO_X,RAW_GYRO_Y,RAW_GYRO_Z"
        self.raw_data = dict()
        self.data = []

    def measurement_loop(self):
        """
            Reads raw values from sensor and store them in temp data storage.
            After measurement: Postprocessing the raw data and store them to
            file.
        """
        while self.start_measurement_event.is_set():
            timestamp = time.time()
            raw_values = self.bus.read_i2c_block_data(self.address, 0x3b, 14)
            self.raw_data[timestamp] = raw_values.copy()

        self.postprocess_raw_data()
        self.data_logger.write_measurements_to_file(np.array(self.data), self.name, self.data_header)
        self.reset_internal_data()
    
    def postprocess_raw_data(self):
        """
            Takes the raw byte values and bring them into right order.
            Store them in python list to write them to file.
        """
        current_data = [0] * self.measurement_count
        for timestamp, raw_values in self.raw_data.items():
            current_data[0] = timestamp
            for idx in range(self.measurement_count-1):
                current_data[idx+1] = self.combine_bytes_to_word(raw_values[idx*2+1], raw_values[idx*2])
            self.data.append(current_data.copy())

    def combine_bytes_to_word(self, low, high):
        """Concate two bytes and convert to integer."""
        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value
        
    def reset_internal_data(self):
        """Resets internal data for next measurement."""
        self.raw_data.clear()
        self.data.clear()