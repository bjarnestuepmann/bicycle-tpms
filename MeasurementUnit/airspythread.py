from struct import unpack
from time import time, sleep
import logging

from bluepy.btle import Peripheral, DefaultDelegate, ADDR_TYPE_RANDOM
import numpy as np
import zmq

from Documents.iTPMS.MeasurementUnit.sensorreader import SensorReader
from threading import Event, Lock
from datalogger import DataLogger


class AirspyDelegate(DefaultDelegate):
    def __init__(self, data: dict):
        super().__init__()

        self.data = data
        self.lock = Lock()
        self.new_data_arrived = Event()

    def handleNotification(self, cHandle, data):
        """
            Store incoming sensor values in internal data.
            Function is called asynchronously when new data arrives.
            Differentiates between two messages:
            -> Message 1: Pressure
            -> Message 2: Battery, Temperature
            Store all three values in the internal dictionary with the
            current number of seconds as key.
        """
        with self.lock:
            # Check if there is already data saved for this timestamp.
            # If not, create data entry.
            time_sec = int(time())
            if time_sec not in self.data:
                self.data[time_sec] = {'temp': None, 'bat': None,'pres': None}
            
            hex_data = data.hex()
            if hex_data.endswith('00002e'):
                # contains pressure value
                self.data[time_sec]['pres'] = self._hex_word_to_float(
                    hex_data[16:24]
                )
                self._inform_about_new_data(time_sec)
            
            elif hex_data.endswith('001e0d'):
                # contains temperature and battery information
                self.data[time_sec]['temp'] = self._hex_word_to_float(
                    hex_data[0:8]
                )
                self.data[time_sec]['bat'] = self._hex_word_to_float(
                    hex_data[14:22]
                )
                self._inform_about_new_data(time_sec)
            
            else:
                logging.warning("Receive invalid messages from sensor.")

    def _hex_word_to_float(self, hex: str):
        """Convert 32-bit little endian hex value to float."""
        # little-endian float
        # https://docs.python.org/3/library/struct.html#format-characters
        return unpack('<f', bytes.fromhex(hex))[0]
    
    def _inform_about_new_data(self, timestamp):
        """Check if data is already complete.
        If yes, inform AirspyReader that new data is available."""
        measurements = self.data[timestamp]
        inform = True
        # Check if measurement contains default value None.
        # If yes, some data is missing -> don't inform thread.
        for value in measurements:
            if value == None:
                inform = False

        if inform: self.new_data_arrived.set()

class AirspyReader(SensorReader):

    def __init__(self, name: str,
                 start_measurement_event: Event, 
                 terminated_event: Event, 
                 data_logger: DataLogger, 
                 address: str):
        
        super().__init__(name, start_measurement_event, terminated_event)

        self.data_logger = data_logger
        self.data_dict = dict()
        self.data_list = list()
        self.device = Peripheral()
        self.address = address
        self.connected = False
        self.delegate = AirspyDelegate(self.data_dict)

        # Prepare socket for sensor data publishing.
        context = zmq.Context()
        self.pub_sock = context.socket(zmq.PUB)
        self.pub_sock.bind("ipc://sensor." + self.name)

    def run(self):
        """Try to connect, when the thread starts."""
        self.connect(self.address)
        if self.connected:
            super(AirspyReader, self).run()

    def connect(self, address: str):
        """Setup Bluetooth Low Energy connection to AIRSPY sensor."""
        while (not self.connected) \
              and (not self.terminated_event.is_set()):
            try:
                logging.info("Try to connect to sensor.")
                self.device.connect(address, ADDR_TYPE_RANDOM)
                self.device = self.device.withDelegate(self.delegate)
                logging.info("Connected to sensor.")
                self.connected = True

            except Exception as e:
                logging.warning("Failed to connect to sensor. " \
                                + "Try again in 3 seconds.")
                sleep(3)
            

    def disconnect(self):
        """Disconnect from Sensor."""
        self.device.disconnect()

    def subscribe(self):
        """
            Subscribe to characteristic that cotains sensor values.
            After subscribing, handleNotification() is called when
            new data arrives from sensor each second.
        """
        print(f'{self.name}: Subscribe.')
        self.device.writeCharacteristic(20, b'\x01\x00')

    def unsubscribe(self):
        """
            Unsubscribe from characteristic.
            After unsubscribing, handleNotification() is not called
            when new data arrives.
        """
        print(f'{self.name}: Unsubscribe.')
        self.device.writeCharacteristic(20, b'\x00\x00')

    def measurement_loop(self):
        """
            Subscribe to sensor values while measurement event is set.
        """
        self.subscribe()
        while self.start_measurement_event.is_set():
            if self.device.waitForNotifications(1.5):
                # handleNotification() was called asynchronousy.
                continue
            logging.info("No data for more than 1.5 seconds.")
        
        # Stop measurement.
        self.unsubscribe()
        self.prepare_data_for_data_logger()
        self.data_logger.write_measurements_to_file(
            np.array(self.data_list),
            self.name, 
            "timestamp,battery,temperatur,pressure"
        )
        self.reset_data()
        
    def streaming_loop(self):
        curr_measurement = list()
        self.subscribe()
        while not self.start_measurement_event.is_set():
            self.delegate.new_data_arrived.wait(timeout=1)
            if self.delegate.new_data_arrived.is_set():
                # Get the newest element of dictionary.
                timestamp, measurement_dict = self.data_dict.items()[0]
                
                # Prepare data for publishing.
                curr_measurement.append(timestamp)
                curr_measurement.append(measurement_dict['bat'])
                curr_measurement.append(measurement_dict['temp'])
                curr_measurement.append(measurement_dict['pres'])

                self.pub_sock.send_pyobj(curr_measurement)
                
                self.delegate.new_data_arrived.clear()
                curr_measurement.clear()
        
        self.unsubscribe()
        self.delegate.data.clear()

    def prepare_data_for_data_logger(self):
        """TODO: Documentation"""
        curr_data = [0] * 4
        for timestamp, values in self.data_dict.items():
            curr_data[0] = float(timestamp)
            curr_data[1] = values['bat']
            curr_data[2] = values['temp']
            curr_data[3] = values['pres']

            self.data_list.append(curr_data.copy())

    def reset_data(self):
        """Prepare internal data for next measurement."""
        self.data_dict.clear()
        self.data_list.clear()

    def clean_up(self):
        """Disconnect from sensor, before this thread terminates."""
        logging.info('Disconnect.')
        self.disconnect()

