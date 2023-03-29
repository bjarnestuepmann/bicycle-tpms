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
    display = DisplayThread("DisplayThread", 
                            start_measurement_event,
                            terminated_event,
                            port=0,
                            cs=0,
                            dc=24,
                            rst=25
                            )
    display.initilize()

    # Data Logger
    dl = DataLogger("DataLogger",
                    start_measurement_event,
                    terminated_event,
                    "/home/pi/Documents/iTPMS/MeasurementUnit/data"
                    )
    dl.initialize()

    # MPU6050
    mpu_1 = MPU6050Thread("MPU_1",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=1,
                          address=0x68
                         )
    mpu_1.initilize()
    mpu_2 = MPU6050Thread("MPU_2",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=1,
                          address=0x69
                         )
    mpu_2.initilize()
    mpu_3 = MPU6050Thread("MPU_3",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=3,
                          address=0x68
                         )
    mpu_3.initilize()
    mpu_4 = MPU6050Thread("MPU_4",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=3,
                          address=0x69
                         )
    mpu_4.initilize()
    mpu_5 = MPU6050Thread("MPU_5",
                          start_measurement_event,
                          terminated_event,
                          data_logger=dl,
                          i2c_bus=4,
                          address=0x68
                         )
    mpu_5.initilize()

    # Wheel Speed Sensor Thread
    whl_spd_sensor = WheelSpeedSensorThread('WheelSpeed',
                                         start_measurement_event,
                                         terminated_event,
                                         dl,
                                         20,
                                         21)
    whl_spd_sensor.initilize()

    # Start threads.
    display.start()
    dl.start()
    mpu_1.start()
    mpu_2.start()
    mpu_3.start()
    mpu_4.start()
    mpu_5.start()
    whl_spd_sensor.start()

    try:
        print("Start measurement for 10 seconds.")
        start_measurement_event.set()
        sleep(300)

    except KeyboardInterrupt:
        print(": Terminated by User")

    finally:
        print("Stop measurement.")
        start_measurement_event.clear()
        terminated_event.set()
    
    print("Wait for other threads!")
    display.join()
    dl.join()
    mpu_1.join()
    print("Exit programm.")


if __name__ == '__main__':
    main()

    