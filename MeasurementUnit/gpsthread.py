from threading import Event
import serial
import time
from enum import IntEnum
import logging

from pyubx2 import UBXReader

from basethread import BaseThread
from datalogger import DataLogger

class NavStatToIntConverter(IntEnum):
    NF = 0
    DR = 1
    G2 = 2
    G3 = 3
    D2 = 4
    D3 = 5
    RK = 6
    TT = 7

class GPSThread(BaseThread):

    def __init__(self, name: str, 
                 start_measurement_event: Event,
                 terminated_event: Event,
                 data_logger: DataLogger,
                 port: str):
        
        super().__init__(name, start_measurement_event, terminated_event)

        self.data_logger = data_logger
        self.measurements = list()
        self._connect(port)
    
    def _connect(self, port):
        """Set up connection to GPS sensor."""
        usb = serial.Serial(port, 38400)
        self.ubr = UBXReader(usb, protfilter=1) # only NMEA messages

    def measurement_loop(self):
        """
            Read messages from GPS sensor and store them to internal data.
            After stopping the measurement, this function saves the data
            permanently to file.
        """
        # measurement ->  [timestamp, lon, lat, sog, status, numSV]
        measurement = [-1] * 6
        while self.start_measurement_event.is_set():
            (raw_data, msg) = self.ubr.read()
            measurement[0] = time.time()
            if msg.identity == "PUBX00":
                self._parse_pubx00_msg(measurement, msg)
            elif msg.identity == "NAV-PVT":
                self._parse_nav_pvt_msg(measurement, msg)
            else:
                logging.warning("Receive unknown message type:", msg.identity)
                continue
            
            self.measurements.append(measurement.copy())

        self._write_data_to_file()
        self.measurements = list()

    def _parse_pubx00_msg(self, measurement, msg):
        """Parse required values from msg into internal list."""
        # measurement -> [timestamp, lon, lat, sog, status, numSV]
        measurement[1] = msg.lon
        measurement[2] = msg.lat
        measurement[3] = msg.SOG
        measurement[4] = int(NavStatToIntConverter[msg.navStat])
        measurement[5] = msg.numSVs

    def _parse_nav_pvt_msg(self, measurement, msg):
        """Parse required values from msg into internal list."""
        # measurement -> [timestamp, lon, lat, sog, status, numSV]
        pass

    def _write_data_to_file(self):
        csv_header = "timestamp,lon,lat,sog,status,numSV"
        self.data_logger.write_measurements_to_file(
            self.measurements, self.name, csv_header
        )
