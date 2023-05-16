from threading import Event
from time import sleep, perf_counter
import logging
import logging.handlers
from collections import deque

from PIL import Image, ImageDraw, ImageFont
import ST7735

from measurementunitcomponent import MeasurementUnitComponent


class DisplayThread(MeasurementUnitComponent):
    """Control Thread for Display"""
    
    def __init__(self, name: str, 
                 start_measurement_event: Event, terminated_event: Event,
                 port: int, cs: int, dc: int, rst: int):
        """Create new Thread and passing arguments to class instance"""
        super(DisplayThread, self).__init__(name, start_measurement_event, terminated_event)

        self.disp = ST7735.ST7735(
            port=port, cs=cs, dc=dc, rst=rst, 
            width=128, height=160, rotation=90,
            invert=False, backlight=None)
        
        self.height = self.disp.height
        self.width = self.disp.width
        self.img = Image.new('RGB', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.img)
        self.font_small = ImageFont.truetype(
            font="/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf",
            size=10
        )
        self.font_big = ImageFont.truetype(
            font="/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf",
            size=60
        )
        
        self.clear_display()

    def run(self):
        """Show the logging messages before regular run() is called."""
        self._display_logs()
        super(DisplayThread, self).run()
    
    def _display_logs(self):
        """Register a new custom logging handler, which displays
        new logging messages on the display.
        Stops when first measurement is started 
        or when programm gets terminated.
        """
        log_view = LogDisplayWriter(
            display=self,
            format="%(levelname)s::%(threadName)s::%(message)s"
        )
        while (not self.start_measurement_event.is_set()) \
              and (not self.terminated_event.is_set()):
            self.start_measurement_event.wait(timeout=1)

        logging.getLogger().removeHandler(log_view)


    def measurement_loop(self):
        """Displays timer while measurement."""
        #print("DisplayThread: display_timer()")
        start_time = perf_counter()
        while self.start_measurement_event.is_set():
            current_time = perf_counter()
            elapsed_time = current_time - start_time
            self.display_text_center(
                f"{elapsed_time//60:.0f}:{int(elapsed_time%60):02d}",
                self.font_big)
            sleep(0.8)

        self.clear_display()
        self._display_logs()

    def clear_image(self):
        """Overwrite internal image with black rectangle."""
        self.draw.rectangle(
            xy=[0, 0 ,self.width, self.height],
            fill=(0, 0, 0)
        )

    def clear_display(self):
        """Show black rectangle on display."""
        self.clear_image()
        self.disp.display(self.img)

    def display_text_center(self, text: str, font: ImageFont):
        """Show text in the center of the display."""
        self.clear_image()
        self.draw.text((self.width//2,self.height//2),
                       text, font=font, anchor="mm")
        self.disp.display(self.img)

    def display_multiple_line(self, lines: list):
        """Show multiples lines on display."""
        self.clear_image()
        for line_idx, line in enumerate(lines):
            self.draw.text((4, 4 + (10*line_idx)), line, 
                           font=self.font_small)
        self.disp.display(self.img)

    
class LogDisplayWriter(logging.Handler):
    """Custom logging handler, which shows the 
    current logging messages on the display.
    """

    def __init__(self, *args, **kwargs):
        logging.Handler.__init__(self, *args)

        # Parse init() arguments.
        for key, value in kwargs.items():
            if "{}".format(key) == "format":
                formater = logging.Formatter(value)
                self.setFormatter(formater)
            if "{}".format(key) == "display":
                self.display = value

        logging.getLogger().addHandler(self)
        
        # Because of its size, the display can only show 12 lines.
        # All lines are saved in this queue.
        # If a a new line is appended, when maxlen is reached, the queue
        # deletes oldest line at the top and append the new line at
        # the bottom.
        self.log_queue = deque(maxlen=12)

    def emit(self, record):
        """Overload of logging.Handler method.
        All new logging messages are appended to queue.
        After appending, the updated queue is shown on display.
        """
        msg = self.format(record)
        self.log_queue.append(msg)
        self.display.display_multiple_line(
            list(self.log_queue)
        )
