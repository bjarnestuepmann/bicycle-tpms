from pyubx2 import UBXReader, SET
from datetime import datetime

import serial

port = '/dev/serial/by-id/'\
        'usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00'
usb = serial.Serial(port,38400)
ubr = UBXReader(usb, quitonerror=2)


try:
    # for (raw_data, msg) in ubr:
    #     if msg.identity == "PUBX00":
    #         ts_str = datetime.now().strftime("%H:%M:%S")
    #         print(ts_str, msg.time)
    #         #print(f'{ts_str} -> lon: {msg.lon}, lat: {msg.lat}, SOG: {msg.SOG}, '+\
    #         #       f'status: {msg.navStat}, numSVs: {msg.numSVs}')

    while True:
        (raw_data, msg) = ubr.read()
        print(msg)
            

except KeyboardInterrupt:
    print("KeyboardInterrupt")