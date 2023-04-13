from threading import Thread, Event
from pyubx2 import UBXReader, UBXMessage, SET
import serial
from utils import SensorTypeTranslator, GPSConfig


class GPSSensorReader(Thread):

    def __init__(self, stop_event: Event):
        super(GPSSensorReader, self).__init__()

        self.stop_event = stop_event

        self.config = GPSConfig()

        self.connect()
        self.initialize()
        

    def connect(self):
        """ Connect the thread to the GPS sensor"""
        port = '/dev/serial/by-id/usb-u-blox_AG_-_'\
        'www.u-blox.com_u-blox_GNSS_receiver-if00'
        self.usb = serial.Serial(port,34800)
        self.ubr = UBXReader(self.usb, protfilter=2)
    

    def initialize(self):
        """
            Send configuration messages to the sensor so that it
            periodically sends the desired messages to the USB port. 
        """
        messages = []
        # UBX-NAV-PVT
        messages.append(UBXMessage(ubxClass=0x06, ubxID=0x01,  msgmode=SET, 
                        msgClass=0x01, msgID=0x07, rateUSB=1))
        # UBX-ESF-STATUS
        messages.append(UBXMessage(ubxClass=0x06, ubxID=0x01,  msgmode=SET, 
                        msgClass=0x10, msgID=0x10, rateUSB=1))
        # UBX-ESF-ALG
        messages.append(UBXMessage(ubxClass=0x06, ubxID=0x01,  msgmode=SET, 
                        msgClass=0x10, msgID=0x14, rateUSB=1))
        for msg in messages:
            self.usb.write(msg.serialize())


    def run(self):
        while not self.stop_event.is_set():
            (raw_data, msg) = self.ubr.read()
            #print(msg)
            if msg.identity == "ESF-ALG":
                self.process_esf_alg_msg(msg)
            elif msg.identity == "ESF-STATUS":
                self.process_esf_status_msg(msg)
            elif msg.identity == "NAV-PVT":
                self.process_nav_pvt_msg(msg)
            else:
                print("No prcoess routine for UBX message " + msg.identity)


    def process_nav_pvt_msg(self, msg: UBXMessage):
        """ Store sensor values in local variables. """
        self.config.clk_h = msg.hour
        self.config.clk_min = msg.min
        self.config.fix_type = msg.fixType
        self.config.sv = msg.numSV


    def process_esf_status_msg(self, msg: UBXMessage):
        """ Store sensor values in local variables. """
        self.config.fusion_mode = msg.fusionMode
        # iterate over available sensors.
        for loop_idx, sens_id in enumerate(range(1,msg.numSens+1)):
            sens_type = SensorTypeTranslator[
                getattr(msg, "type_0" + str(sens_id))]
            self.config.calib_states[sens_type] = \
                getattr(msg, "calibStatus_0" + str(sens_id))


    def process_esf_alg_msg(self, msg: UBXMessage):
        """ Store sensor values in local variables. """
        self.config.alg_status = msg.status

    def get_config(self):
        return self.config