import RPi.GPIO as GPIO            # import RPi.GPIO module  
import time
import numpy as np
import os

GPIO_OUTPUT_PIN = 21 # VOLTAGE
GPIO_INPUT_PIN = 20 # GND
WHEEL_CIRCUMFENCES = 2224 # [mm]
DEBOUNCE_TIME = 25
old_ts_ms = int(time.time() * 1e3)
durations = list()
counter = 0


def sensorCallback(channel):
    # Called if magnet is detected.
    global old_ts_ms, durations, counter
    new_ts_ms = int(time.time() * 1e3)
    duration = new_ts_ms - old_ts_ms
    old_ts_ms = new_ts_ms
    durations.append(duration)
    print(f'{counter}: {duration} ms')
    counter += 1

def write_durations_to_file():
    curr_dir = "/home/pi/Documents/iTPMS/sensor_tests/wheel_speed/data/"
    file_name = curr_dir  + "durations_" + str(int(time.time())) + ".txt"
    with open(file_name, 'a') as file:
        for d in durations:
            file.write(str(d) + "\n")

def main():
    try:  
        GPIO.output(GPIO_OUTPUT_PIN, 1)
        
        while True:  
           if len(durations) > 1000:
               durations.pop(0)
               write_durations_to_file()
               break
           time.sleep(1)

        GPIO.cleanup()
        
    except KeyboardInterrupt:
        print('\nCtrl+C: Program terminated by user...')
        GPIO.cleanup()


GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(GPIO_OUTPUT_PIN, GPIO.OUT)           # set GPIO24 as an output 
GPIO.setup(GPIO_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(GPIO_INPUT_PIN, GPIO.FALLING, callback=sensorCallback, bouncetime=DEBOUNCE_TIME)

if __name__=="__main__":
   main()