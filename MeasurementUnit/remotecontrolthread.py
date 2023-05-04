from threading import Event
import logging

import RPi.GPIO as GPIO 

from basethread import BaseThread


class RemoteControlThread(BaseThread):

    def __init__(self, name: str,
                 start_measurement_event: Event,
                 terminated_event: Event,
                 pinA: int, pinB: int, pinC:int, pinD: int):
        super().__init__(name, start_measurement_event, terminated_event)

        self.pinA = pinA
        self.pinB = pinB
        self.pinC = pinC
        self.pinD = pinD
        self._setup()
        
    def _setup(self):
        """Initialize GPIO Pins and register falling edge as event."""
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(self.pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pinC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # GPIO.setup(self.pinD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def run(self):
        """Wait for user input with buttons and
        throw events for starting and stopping measurement.
        """
        GPIO.add_event_detect(self.pinA, GPIO.FALLING)
        while(not self.terminated_event.is_set()):
            if self.start_measurement_event.is_set():
                # Measurement is running.
                # Wait for stop measurement input.
                GPIO.wait_for_edge(self.pinC, GPIO.FALLING, timeout=1000)
                if GPIO.event_detected(self.pinC):
                    logging.info("Button C was pressed.")
                    self.start_measurement_event.clear()
                    GPIO.remove_event_detect(self.pinC)
                    GPIO.add_event_detect(self.pinA, GPIO.FALLING)
            else:
                # No measurement is running.
                # Wait for start measurement input.
                GPIO.wait_for_edge(self.pinA, GPIO.FALLING, timeout=1000)
                if GPIO.event_detected(self.pinA):
                    logging.info("Button A was pressed.")
                    self.start_measurement_event.set()
                    GPIO.remove_event_detect(self.pinA)
                    GPIO.add_event_detect(self.pinC, GPIO.FALLING)



        