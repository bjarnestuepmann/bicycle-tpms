from displaythread import DisplayThread
from datalogger import DataLogger
from mpu6050thread import MPU6050Thread
from wheelspeedsensorthread import WheelSpeedSensorThread
from threading import Event
from time import sleep

def main():

    start_measurement_event = Event()
    terminated_event = Event()

    # Display
    dsp = DisplayThread("DisplayThread", 
                            start_measurement_event,
                            terminated_event,
                            port=0,
                            cs=0,
                            dc=24,
                            rst=25
                            )
    # Data Logger
    dl = DataLogger("DataLogger",
                    start_measurement_event,
                    terminated_event,
                    "/home/pi/Documents/iTPMS/MeasurementUnit/data"
                    )

    # MPU6050
    mpu_1 = MPU6050Thread("MPU_1",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=5,
                          address=0x68
                         )
    mpu_2 = MPU6050Thread("MPU_2",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=5,
                          address=0x69
                         )
    mpu_3 = MPU6050Thread("MPU_3",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=3,
                          address=0x68
                         )
    mpu_4 = MPU6050Thread("MPU_4",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=3,
                          address=0x69
                         )
    mpu_5 = MPU6050Thread("MPU_5",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=4,
                          address=0x68
                         )

    # Wheel Speed Sensor Thread
    wss = WheelSpeedSensorThread('WheelSpeed',
                                         start_measurement_event,
                                         terminated_event,
                                         dl,
                                         20,
                                         21)

    # Start threads.
    dsp.start()
    dl.start()
    mpu_1.start()
    mpu_2.start()
    mpu_3.start()
    mpu_4.start()
    mpu_5.start()
    wss.start()

    try:
        duration = 30
        print("Start measurement for " + str(duration) + " seconds.")
        start_measurement_event.set()
        sleep(duration)

    except KeyboardInterrupt:
        print(": Terminated by User")

    finally:
        print("Stop measurement.")
        start_measurement_event.clear()
        terminated_event.set()
    
    print("Wait for other threads!")
    dsp.join()
    dl.join()
    mpu_1.join()
    mpu_2.join()
    mpu_3.join()
    mpu_4.join()
    mpu_5.join()
    wss.join()
    print("Exit programm.")


if __name__ == '__main__':
    main()

    