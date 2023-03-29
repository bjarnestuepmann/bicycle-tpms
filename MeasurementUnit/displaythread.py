from basethread import BaseThread
from threading import Event
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7735
import time



class DisplayThread(BaseThread):
    """Control Thread for Display"""
    
    def __init__(self, name: str, start_measurement_event: Event, terminated_event: Event, port: int, cs: int, dc: int, rst: int):
        """Create new Thread and passing arguments to class instance"""
        super(DisplayThread, self).__init__(name, start_measurement_event, terminated_event)
        
        self.port = port
        self.cs = cs
        self.dc = dc
        self.rst = rst
        
        # Connect to display.
        self.disp = ST7735.ST7735(port=self.port, cs=self.cs, dc=self.dc, backlight=None, rst=self.rst, width=128, height=160, rotation=270, invert=False)
        # Prepare internal data.
        self.height = self.disp.height
        self.width = self.disp.width
        self.img = Image.new('RGB', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.img)
        self.font_small = ImageFont.truetype(font="/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf", size=20)
        self.font_big = ImageFont.truetype(font="/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf", size=60)
    
    def measurement_loop(self):
        """Displays timer while measurement."""
        #print("DisplayThread: display_timer()")
        start_time = time.perf_counter()
        while self.start_measurement_event.is_set():
            current_time = time.perf_counter()
            elapsed_time = current_time - start_time
            self.display_text_center(f"{elapsed_time//60:.0f}:{int(elapsed_time%60):02d}", self.font_big)
            time.sleep(0.8)

        self.clear_display()

    def clear_image(self):
        self.draw.rectangle(xy=[0, 0 ,self.width, self.height], fill=(0, 0, 0))

    def clear_display(self):
        self.clear_image()
        self.disp.display(self.img)

    def display_text_center(self, text: str, font: ImageFont):
        #print("DisplayThread: display_text_center()")
        self.clear_image()
        self.draw.text((self.width//2,self.height//2), text, font=font, anchor="mm")
        self.disp.display(self.img)


