from threading import Event, current_thread
from time import sleep, time
import logging
import logging.handlers
import sys

from displaythread import DisplayThread
from datalogger import DataLogger
from remotecontrolthread import RemoteControlThread
from mpu6050thread import ImuReader
from wheelspeedsensorthread import WheelSpeedSensorReader
from airspythread import AirspyReader
from gpsthread import GpsReader


def config_logging():
    log_file_dir = "/home/pi/Documents/iTPMS/MeasurementUnit/logs"
    log_file_name = f"{log_file_dir}/measurement_unit.log"
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter("%(asctime)s::%(levelname)s::%(threadName)s::%(message)s")

    # Logging to File
    rot_file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file_name,
    )
    rot_file_handler.setFormatter(log_formatter)
    rot_file_handler.setLevel(logging.INFO)
    root_logger.addHandler(rot_file_handler)
    
    # Logging to console.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)


def main():
    # Set thread name.
    this_thread = current_thread()
    this_thread.name = "main"
    
    config_logging()

    start_measurement_event = Event()
    terminated_event = Event()

    threads = list()
    dsp = DisplayThread(
        "display", 
        start_measurement_event, terminated_event,
        port=0, cs=0, dc=9, rst=25
    )
    threads.append(dsp)
    dsp.start()
    
    # Data Logger
    dl = DataLogger(
        "datalogger",
        start_measurement_event, terminated_event,
        "/home/pi/Documents/iTPMS/MeasurementUnit/data"
    )
    threads.append(dl)
    dl.start()
    
    # Remote Controller
    rmt_ctr_thread = RemoteControlThread(
        "remote_ctr",
        start_measurement_event, terminated_event,
        pinA= 13, pinB= 12, pinC= 5, pinD= 6
    )
    threads.append(rmt_ctr_thread)
    rmt_ctr_thread.start()

    # MPU6050
    mpu_1 = ImuReader(
        "imu1",
        start_measurement_event, terminated_event,
        data_logger=dl,
        i2c_bus=5, address=0x68
    )
    threads.append(mpu_1)
    mpu_1.start()

    mpu_2 = ImuReader(
        "imu2",
        start_measurement_event, terminated_event,
        data_logger=dl,
        i2c_bus=5, address=0x69
    )
    threads.append(mpu_2)
    mpu_2.start()

    mpu_3 = ImuReader(
        "imu3",
        start_measurement_event, terminated_event,
        data_logger=dl,
        i2c_bus=3, address=0x68
    )
    threads.append(mpu_3)
    mpu_3.start()

    mpu_4 = ImuReader(
        "imu4",
        start_measurement_event, terminated_event,
        data_logger=dl,
        i2c_bus=3, address=0x69
    )
    threads.append(mpu_4)
    mpu_4.start()

    mpu_5 = ImuReader(
        "imu5",
        start_measurement_event, terminated_event,
        data_logger=dl,
        i2c_bus=4, address=0x68
    )
    threads.append(mpu_5)
    mpu_5.start()

    mpu_6 = ImuReader(
        "imu6",
        start_measurement_event, terminated_event,
        data_logger=dl,
        i2c_bus=4, address=0x69
    )
    threads.append(mpu_6)
    mpu_6.start()
    
    mpu_7 = ImuReader(
        "imu7",
        start_measurement_event, terminated_event,
        data_logger=dl,
        i2c_bus=6, address=0x68
    )
    threads.append(mpu_7)
    mpu_7.start()

    # Wheel Speed Sensor
    ws_front = WheelSpeedSensorReader(
            'ws_front',
            start_measurement_event, terminated_event,
            data_logger=dl,
            gpio_signal_pin=3
    )
    threads.append(ws_front)
    ws_front.start()

    ws_rear = WheelSpeedSensorReader(
            'ws_rear',
            start_measurement_event, terminated_event,
            data_logger=dl,
            gpio_signal_pin=2
    )
    threads.append(ws_rear)
    ws_rear.start()

    # air_front = AirspyReader("Airspy_front",
    #                          start_measurement_event,
    #                          terminated_event,
    #                          dl,
    #                          "d4:65:7f:6a:a3:10")
    # threads.append(air_front)
    # air_front.start()
    
    # air_rear = AirspyReader("Airspy_rear",
    #                          start_measurement_event,
    #                          terminated_event,
    #                          dl,
    #                          "ee:0d:0c:41:30:be")
    # threads.append(air_rear)
    # air_rear.start()

    # gps_ref = GpsReader(
    #     "gps_ref",
    #     start_measurement_event,
    #     terminated_event,
    #     dl,
    #     '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_R-if00')
    # threads.append(gps_ref)
    # gps_ref.start()

    # gps_imu = GpsReader(
    #     "gps_imu",
    #     start_measurement_event,
    #     terminated_event,
    #     dl,
    #     '/dev/serial/by-id/'\
    #         'usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00')
    # threads.append(gps_imu)
    # gps_imu.start()
    
    logging.info(f"{len(threads)} threads are started.")

    try:
        # Wait for keyboard interrupt.
        while True:
            sleep(1)

    except KeyboardInterrupt:
        logging.info("Terminated by user.")

    finally:
        start_measurement_event.clear()
        terminated_event.set()
    
    logging.info("Wait for other threads.")
    for thread in threads:
        thread.join()
    
    logging.info("Exit programm.")


if __name__ == '__main__':
    main()

    