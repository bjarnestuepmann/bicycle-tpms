import RPi.GPIO as GPIO            # import RPi.GPIO module  
import time
import numpy as np
import os

GPIO_OUTPUT_PIN = 21 # VOLTAGE
GPIO_INPUT_PIN = 20 # GND
WHEEL_CIRCUMFENCES = 2224 # [mm]
DEBOUNCE_TIME = 50 # [ms]

def main():
    try:  
        old_ts_ms = int(time.time() * 1e3)
        GPIO.output(GPIO_OUTPUT_PIN, 1)
        old_duration = 0

        while True:
            channel = GPIO.wait_for_edge(GPIO_INPUT_PIN, GPIO.FALLING, 
                                         timeout=1000, 
                                         bouncetime=DEBOUNCE_TIME)
            if channel is None:
                #print(f"---- ms | {0:2.2f} km/h")
                continue
            else:
                    new_ts_ms = int(time.time() * 1e3)
                    duration = new_ts_ms - old_ts_ms
                    old_ts_ms = new_ts_ms
                    
                    # -- Filter outliers. --
                    # If the duration has more halved within one wheel turn, 
                    # i.e. the speed has more than doubled within one turn, 
                    # then this must be an outlier.
                    # One exception is a fast start-up at low speeds. 
                    # But these do not play a role in my measurements.
                    if duration < old_duration / 2:
                        #print("Outlier")
                        pass
                    else:
                        if duration != 0:
                            speed_kmh = WHEEL_CIRCUMFENCES / (duration) * 3.6
                            print(f"{duration:4} ms | {speed_kmh:2.2f} km/h")
                    
                    old_duration = duration


    except KeyboardInterrupt:
        print('\nCtrl+C: Program terminated by user...')
        GPIO.cleanup()


GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(GPIO_OUTPUT_PIN, GPIO.OUT)           # set GPIO24 as an output 
GPIO.setup(GPIO_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO.add_event_detect(GPIO_INPUT_PIN, GPIO.FALLING, callback=sensorCallback, bouncetime=300)

if __name__=="__main__":
   main()