# credits: https://github.com/semuconsulting/pyubx2/blob/master/examples/ubxpoller.py

from enum import Enum
from sys import platform
from threading import Thread, Event, Lock
from queue import Queue
from time import sleep
from serial import Serial
from pyubx2 import UBXReader, UBXMessage, POLL, UBX_PROTOCOL


class FusionMode(Enum):
    INITIALIZING = 0
    FUSION = 1
    SUSPENDED = 2
    DISABLED = 3

class CalibStatus(Enum):
    INITIALIZING = 0
    CALIBRATING = 1
    CALIBRATED = 2

class ImuInitStatus(Enum):
    INITIALIZING = 1
    INITIALIZED = 2

class MntAlgStatus(Enum):
    INITIALIZING = 1
    INITIALIZED = 2

class InsInitStatus(Enum):
    INITIALIZING = 1
    INITIALIZED = 2

class EsfAlgStatus(Enum):
    OTHER = 0
    FINE = 4

FUSION_MODE = FusionMode.INITIALIZING
CALIB_STAUTS = CalibStatus.INITIALIZING
IMU_INIT_STATUS = ImuInitStatus.INITIALIZING
MNT_ALG_STATUS = MntAlgStatus.INITIALIZING
INS_INIT_STATUS = InsInitStatus.INITIALIZING
ESF_ALG_STATUS = EsfAlgStatus.OTHER

SLEEP_TIME = 1

def read_status(
    stream: object,
    ubr: UBXReader,
    queue: Queue,
    lock: Lock,
    stop: Event,
):
    """
    Read and parse incoming UBX data and place
    raw and parsed data on queue
    """
    # pylint: disable=unused-variable, broad-except
    print(f"\nStart read status...\n")

    while not stop.is_set():
        if stream.in_waiting:
            try:
                lock.acquire()
                (raw_data, parsed_data) = ubr.read()
                lock.release()
                if parsed_data:
                    queue.put((raw_data, parsed_data))
            except Exception as err:
                print(f"\n\nSomething went wrong {err}\n\n")
                continue


def poll_status(stream: object, lock: Lock, stop: Event):
    """
    Read queue and send UBX message to device
    """
    print(f"\nStart polling status...\n")

    msg_poll_status = UBXMessage("ESF", "ESF-STATUS", POLL)
    msg_poll_alg = UBXMessage("ESF", "ESF-ALG", POLL)

    while not stop.is_set():
        lock.acquire()
        stream.write(msg_poll_status.serialize())
        stream.write(msg_poll_alg.serialize())
        lock.release()
        sleep(SLEEP_TIME)


def update_status(queue: Queue, stop: Event):
    """
    Get UBX data from queue and display.
    """
    # pylint: disable=unused-variable,
    print(f"\nStart updating status...\n")

    while not stop.is_set():
        if queue.empty() is False:
            (raw, parsed) = queue.get()

            # differentiate between messages
            if(parsed.msg_cls == b'\x10' and parsed.msg_id == b'\x10'):
                # ESF-Status
                update_status_esf_status(parsed)
            elif(parsed.msg_cls == b'\x10' and parsed.msg_id == b'\x14'): 
                # ESF-ALG
                update_status_esf_alg(parsed)
            else:
                print("Other UBX Mesage")

            queue.task_done()

def update_status_esf_status(msg: UBXMessage):
    """
    Update internal state with incoming ESF-STATUS message.
    """
    # 1x Fusion Mode
    if msg.fusionMode == 0:
        print("Fusion Mode: Initializing")
        FUSION_MODE = FusionMode.INITIALIZING
    elif msg.fusionMode == 1:
        print("Fusion Mode: Fusion")
        FUSION_MODE = FusionMode.FUSION
    else:
        print("Error: Fusion Mode: ", msg.fusionMode)

    calibStatusList = []
    for sensor_id in range(1, msg.numSens+1): 
        calibStatusList.append(getattr(msg, "calibStatus_0" + str(sensor_id)))

    if min(calibStatusList) == 0:
        print("CALIB_STAUTS: INITIALIZING")
        CALIB_STAUTS = CalibStatus.INITIALIZING
    elif min(calibStatusList) == 1:
        print("CALIB_STAUTS: CALIBRATING")
        CALIB_STAUTS = CalibStatus.CALIBRATING
    else:
        print("CALIB_STAUTS: CALIBRATED")
        CALIB_STAUTS = CalibStatus.CALIBRATED

    # a) 3x imuInitStatus


    # b) 3x mntAlgStatus


    # b) 3x insInitStatus


def update_status_esf_alg(msg: UBXMessage):
    """
    Update internal state with incoming ESF-ALG message.
    """
    if(msg.status == 4):
        print("ESF_ALG_STATUS: FINE")
        ESF_ALG_STATUS = EsfAlgStatus.FINE
    else:
        print("ESF_ALG_STATUS: OTHER")
        ESF_ALG_STATUS = EsfAlgStatus.OTHER

if __name__ == "__main__":
    # set port, baudrate and timeout to suit your device configuration
    # set port, baudrate and timeout to suit your device configuration
    port = '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00'
    baudrate = 34800
    timeout = 0.1

    with Serial(port, baudrate, timeout=timeout) as serial_stream:
        ubxreader = UBXReader(serial_stream, protfilter=UBX_PROTOCOL)

        serial_lock = Lock()
        read_queue = Queue()
        stop_event = Event()

        read_thread = Thread(
            target=read_status,
            args=(
                serial_stream,
                ubxreader,
                read_queue,
                serial_lock,
                stop_event,
            ),
        )
        write_thread = Thread(
            target=poll_status,
            args=(
                serial_stream,
                serial_lock,
                stop_event,
            ),
        )
        display_thread = Thread(
            target=update_status,
            args=(
                read_queue,
                stop_event,
            ),
        )

        print("\nStarting handler processes. Press Ctrl-C to terminate...")
        read_thread.start()
        write_thread.start()
        display_thread.start()

        # loop until user presses Ctrl-C
        while not stop_event.is_set():
            try:
                if(CALIB_STAUTS == CalibStatus.INITIALIZING):
                    print("1. Initialization Phase")

                    print("1.1 IMU initialization")
                    while(IMU_INIT_STATUS is ImuInitStatus.INITIALIZING):
                        sleep(SLEEP_TIME)
                    print("Done\n")

                    print("1.2 IMU-mount alignment initialization")
                    while(MNT_ALG_STATUS is MntAlgStatus.INITIALIZING):
                        sleep(SLEEP_TIME)
                    print("Done\n")

                    print("1.3 INS initialization")
                    while(INS_INIT_STATUS is InsInitStatus.INITIALIZING):
                        sleep(SLEEP_TIME)
                    print("Done\n")

                elif(CALIB_STAUTS == CalibStatus.CALIBRATING):
                    print("2. Calibration Phase")
                    print("2.1 IMU-mount alignment calibration")
                    while(ESF_ALG_STATUS is not EsfAlgStatus.FINE):
                        sleep(SLEEP_TIME)
                    print("Done\n")

                    print("2.2 IMU calibration (gyroscope and accelerometer)")
                    while(CALIB_STAUTS is CalibStatus.CALIBRATING):
                        sleep(SLEEP_TIME)
                    print("Done\n")

                else:
                    print("3. Navigation Phase\n")
                    if(FUSION_MODE is FusionMode.FUSION):
                        print("Done\n")

                    elif(FUSION_MODE is FusionMode.SUSPENDED):
                        print("Fusion Mode is SUSPENDED")

                    else:
                        print("Fusion Mode is DISABLED.")
                    
                    stop_event.set()

            except KeyboardInterrupt:  # capture Ctrl-C
                print("\n\nTerminated by user.")
                stop_event.set()

        print("\nStop signal set. Waiting for threads to complete...")
        read_thread.join()
        write_thread.join()
        display_thread.join()
        print("\Stop configuration")