from threading import Thread, Event
import ST7735
from time import sleep


class DisplayThread(Thread):
    
    def __init__(self, refresh_rate_hz: int, stop_event: Event):
        super().__init__()

        self.stop_event = stop_event

        self.width = 160
        self.height = 128
        self.img = None

        self.refresh_time = 1 / refresh_rate_hz
        self.connect()

    def connect(self):
        """ Setup display connection. """
        self.disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, 
                                  rst=25, width=self.height, 
                                  height=self.width, rotation=270,
                                  invert=False)
    
    def run(self):
        """ Display internal image with given refresh rate. """
        while not self.stop_event.is_set():
            if self.img is not None:
                self.disp.display(self.img)
        
            sleep(self.refresh_time)