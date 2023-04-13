from pyubx2 import UBXReader, UBXMessage, SET
import serial

port = '/dev/serial/by-id/usb-u-blox_AG_-_'\
        'www.u-blox.com_u-blox_GNSS_receiver-if00'
usb = serial.Serial(port,34800)
ubr = UBXReader(usb, protfilter=2)

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
    usb.write(msg.serialize())

for (raw_data, msg) in ubr:
    print(msg)
    if msg.identity == "ESF-ALG":
        print("Status of the IMU-mount alignment: ", end = "")
        if(msg.status == 0):
            print("0: user-defined/fixed angles are used.\n")
        elif(msg.status == 1):
            print("1: IMU-mount roll/pitch angles alignment is ongoing.\n")
        elif(msg.status == 2):
            print(" 2: IMU-mount roll/pitch/yaw angles alignment is ongoing.\n")
        elif(msg.status == 3):
            print("3: coarse IMU-mount alignment are used.\n")
        elif(msg.status == 4):
            print("4: fine IMU-mount alignment are used.\n")
        else:
            print("?: Unknown.")

    elif msg.identity == "ESF-STATUS":
        print(msg)
        print("Fusion Mode: ", end = "")
        if msg.fusionMode == 0:
            print("0: Initialization mode: receiver is initializing some "\
                  "unknown values required for doing sensor fusion.")
        elif msg.fusionMode == 1:
            print("1: Fusion mode: GNSS and sensor data are used for "\
                  "navigation solution computation.")
        elif msg.fusionMode == 2:
            print("2: Suspended fusion mode: sensor fusionis temporarily "\
                  "disabled due to e.g. invalid sensor data or detected ferry.")
        elif msg.fusionMode == 3:
            print("3: Disabled fusion mode: sensor fusion is permanently "\
                  "disabled until receiver reset due e.g. to sensor error.")
        else:
            print("?: Unkown.")