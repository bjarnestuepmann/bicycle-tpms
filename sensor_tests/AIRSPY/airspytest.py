from bluepy.btle import Peripheral, DefaultDelegate, ADDR_TYPE_RANDOM
from time import sleep
from airspybytedecoding import hex_word_to_float
from time import time, sleep
from datetime import datetime

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.f = open("/home/pi/Documents/iTPMS/sensor_tests/AIRSPY/sensor_values.txt", "a")

    def handleNotification(self, cHandle, data):
        #print(data.hex())
        #self.f.write(data.hex() + '\n')
        nanos = int(time() * 1e9)
        secs = nanos / 1e9
        dt = datetime.fromtimestamp(secs)
        dt_str = dt.strftime('%H:%M:%S.%f')
        hex_data = data.hex()
        if hex_data.endswith('00002e'):
            print(dt_str, 'Presure', hex_word_to_float(data[8:12].hex(), 'little'))
        elif hex_data.endswith('001e0d'):
            pass
            #print(dt_str, 'Temp', hex_word_to_float(data[0:4].hex(), 'little'))
            #print(dt_str, 'Battery', hex_word_to_float(data[7:11].hex(), 'little'))
        else:
            print("Received invalid message.")
    
    def closeFile(self):
        self.f.close()


# addr = "ee:0d:0c:41:30:be" # rear: AIRSPY-16375
addr = "d4:65:7f:6a:a3:10" # front: AIRSPY-16801
subscribe_str = b'\x01\x00'
unsubscribe_str = b'\x00\x00'

# Connect to Airspy.
try:
    print("Connect to device", addr)
    p = Peripheral(addr, ADDR_TYPE_RANDOM)
    # p.connect(addr, ADDR_TYPE_RANDOM)
    d = MyDelegate()
    p = p.withDelegate(d)

    # Notify to characteristic with handle
    # Write b'\x01\x00' to Client Characteristic Config
    # on handle 20 (char_handle+1)
    # https://stackoverflow.com/questions/32807781/ble-subscribe-to-notification-using-gatttool-or-bluepy
    print("Connected.")

    while True:
        try:
            print("Subscribe to Service for 5 seconds.")
            p.writeCharacteristic(20, subscribe_str)
            sleep(5)

            print("Unsubscribe to Service for 5 seconds.")
            p.writeCharacteristic(20, unsubscribe_str)
            sleep(5)

        except KeyboardInterrupt:
            print("Disconnect.")
            p.disconnect()
            d.closeFile()
            break

except Exception as e:
    print("Error:", e)