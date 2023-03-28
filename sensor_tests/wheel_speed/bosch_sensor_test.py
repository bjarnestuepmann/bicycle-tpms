import RPi.GPIO as GPIO            # import RPi.GPIO module  
import time         
import datetime                     # lets us have a delay  

GPIO_OUTPUT_PIN = 21 # VOLTAGE
GPIO_INPUT_PIN = 20 # GND

def sensorCallback(channel):
  # Called if sensor output changes
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  print("Falling Edge detected  " + stamp)
  

def main():
    try:  
        GPIO.output(GPIO_OUTPUT_PIN, 1)
        
        while True:  
           time.sleep(1)
  
    except KeyboardInterrupt:
        print('\nCtrl+C: Program terminated by user...')
        GPIO.cleanup()


GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(GPIO_OUTPUT_PIN, GPIO.OUT)           # set GPIO24 as an output 
GPIO.setup(GPIO_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(GPIO_INPUT_PIN, GPIO.FALLING, callback=sensorCallback, bouncetime=300)

if __name__=="__main__":
   main()