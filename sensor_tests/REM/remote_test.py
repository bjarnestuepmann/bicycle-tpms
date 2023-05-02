from time import sleep, time
from datetime import datetime
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)

############ Set Remote #####################################
pin_A= 13
pin_B= 12
pin_C= 5
pin_D= 6
GPIO.setup(pin_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_D, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#############################################################


def button_pressed_callback(channel):
    timestamp = time()
    stamp = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    if(channel==pin_A):
        print(stamp + ": Button A was pressed!")
    elif(channel==pin_B):
        print(stamp + ": Button B was pressed!")
    elif(channel==pin_C):
        print(str(stamp) + ": Button C was pressed!")
    elif(channel==pin_D):
        print(str(stamp) + ": Button D was pressed!")
    else:
        print(stamp + ": Unknown channel was triggered.")


GPIO.add_event_detect(pin_A, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300) 
GPIO.add_event_detect(pin_B, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300) 
GPIO.add_event_detect(pin_C, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300) 
GPIO.add_event_detect(pin_D, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300) 

while True:
    try:
        sleep(1)
    
    except KeyboardInterrupt:
        print(": Terminated by User")
        break

print("Exit program.")
GPIO.cleanup()  
