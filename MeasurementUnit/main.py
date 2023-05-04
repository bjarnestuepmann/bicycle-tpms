from threading import Event
from time import sleep, time
import logging
import logging.handlers
import sys

from displaythread import DisplayThread
from datalogger import DataLogger
from remotecontrolthread import RemoteControlThread
from mpu6050thread import MPU6050Thread
from wheelspeedsensorthread import WheelSpeedSensorThread
from airspythread import AirspyThread
from gpsthread import GPSThread


def config_logging():
    log_file_dir = "/home/pi/Documents/iTPMS/MeasurementUnit/logs"
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter("%(asctime)s::%(levelname)s::%(threadName)s::%(message)s")

    # Logging to File
    rot_file_handler = logging.handlers.RotatingFileHandler(
        filename=f"{log_file_dir}/measurement_unit.log",
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
    config_logging()

    start_measurement_event = Event()
    terminated_event = Event()

    # Display
    dsp = DisplayThread(
        "DisplayThread", 
        start_measurement_event, terminated_event,
        port=0, cs=0, dc=9, rst=25
    )
    
    # # Data Logger
    # dl = DataLogger(
    #     "DataLogger",
    #     start_measurement_event, terminated_event,
    #     "/home/pi/Documents/iTPMS/MeasurementUnit/data"
    # )
    
    # Remote Controller
    rmt_ctr_thread = RemoteControlThread(
        "RemoteControlThread",
        start_measurement_event, terminated_event,
        pinA= 13, pinB= 12, pinC= 5, pinD= 6
    )

    # MPU6050
    # mpu_1 = MPU6050Thread(
    #     "MPU_1",
    #     start_measurement_event, terminated_event,
    #     data_logger=dl,
    #     i2c_bus=5, address=0x68
    # )
    # mpu_2 = MPU6050Thread(
    #     "MPU_2",
    #     start_measurement_event, terminated_event,
    #     data_logger=dl,
    #     i2c_bus=5, address=0x69
    # )
    # mpu_3 = MPU6050Thread(
    #     "MPU_3",
    #     start_measurement_event, terminated_event,
    #     data_logger=dl,
    #     i2c_bus=3, address=0x68
    # )
    # mpu_4 = MPU6050Thread(
    #     "MPU_4",
    #     start_measurement_event, terminated_event,
    #     data_logger=dl,
    #     i2c_bus=3, address=0x69
    # )
    # mpu_5 = MPU6050Thread(
    #     "MPU_5",
    #     start_measurement_event, terminated_event,
    #     data_logger=dl,
    #     i2c_bus=4, address=0x68
    # )

    # Wheel Speed Sensor
    # wss = WheelSpeedSensorThread(
    #         'WheelSpeed',
    #         start_measurement_event, terminated_event,
    #         data_logger=dl,
    #         gpio_gnd=20,
    #         gpio_v=21
    # )

    # air_front = AirspyThread("Airspy_front",
    #                          start_measurement_event,
    #                          terminated_event,
    #                          dl,
    #                          "d4:65:7f:6a:a3:10")

    # gps_ref = GPSThread("GpsRef",
    #                     start_measurement_event,
    #                     terminated_event,
    #                     dl,
    #                     '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_R-if00')
    # gps_imu = GPSThread("Gpsimu",
    #                     start_measurement_event,
    #                     terminated_event,
    #                     dl,
    #                     '/dev/serial/by-id/'\
    #                         'usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00')

    logging.info("Start all threads.")
    # Start threads.
    dsp.start()
    # dl.start()
    rmt_ctr_thread.start()
    # mpu_1.start()
    # mpu_2.start()
    # mpu_3.start()
    # mpu_4.start()
    # mpu_5.start()
    # wss.start()
    # air_front.start()
    # gps_ref.start()
    # gps_imu.start()


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
    
    dsp.join()
    # dl.join()
    rmt_ctr_thread.join()
    # mpu_1.join()
    # mpu_2.join()
    # mpu_3.join()
    # mpu_4.join()
    # mpu_5.join()
    # wss.join()
    # air_front.join()
    # gps_ref.join()
    # gps_imu.join()
    logging.info("Exit programm.")


if __name__ == '__main__':
    main()

    