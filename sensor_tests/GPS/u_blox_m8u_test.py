from pyubx2 import UBXReader
import serial

port = '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiverD-if00'
usb = serial.Serial(port,34800)
ubr = UBXReader(usb)

from pyubx2 import UBXMessage, GET
msg = UBXMessage(ubxClass=0x10, ubxID=0x10, msgmode=GET)
print(msg)
usb.write(msg.serialize())

(raw_data, parsed_data) = ubr.read()
print(parsed_data)

