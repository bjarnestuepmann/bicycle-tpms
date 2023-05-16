import RPi.GPIO as GPIO            # import RPi.GPIO module  
import time         
import datetime                     # lets us have a delay  

GPIO_SIGNAL_PIN = 2
# GPIO_SIGNAL_PIN = 3

def sensorCallback(channel):
  # Called if sensor output changes
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  print("Falling Edge detected  " + stamp)
  

def main():
    try:  
        while True:  
           time.sleep(1)
  
    except KeyboardInterrupt:
        print('\nCtrl+C: Program terminated by user...')
        GPIO.cleanup()


GPIO.setmode(GPIO.BCM)          
GPIO.setup(GPIO_SIGNAL_PIN, GPIO.IN)

GPIO.add_event_detect(GPIO_SIGNAL_PIN, GPIO.FALLING, callback=sensorCallback, bouncetime=300)

if __name__=="__main__":
   main()