from displaythread import DisplayThread
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from utils import FixTypeTranslator, SensorToIndexTranlator, CalibstatusToColorTranslator, GPSConfig

class ConfigScreen():

    def __init__(self, display: DisplayThread):
        
        self.display = display

        self.height = display.height
        self.width = display.width

        self.config = GPSConfig()

        self.initialize()
        self.show_welcome_screen()

    def initialize(self):
        self.img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.fnt = ImageFont.truetype("/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf", 10)
        self.hdr_fnt = ImageFont.truetype("/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf", 9)

        self.sensor_states = {(0,0): (0xef,0x43, 0x47), (1,0): (0x28,0x7d, 0xa1),
                              (0,1): (0xef,0x43, 0x47), (1,1): (0xf9,0xc7, 0x50),
                              (0,2): (0x90,0xbe, 0x6d), (1,2): (0x28,0x7d, 0xa1)}

    def show_welcome_screen(self):
        self.draw.text((self.width//2, self.height//2), "Welcome!",
                       anchor="mm")
        self.show()
        sleep(5)

    def refresh(self):
        self.clear()
        self.refresh_header()
        self.refresh_calib()
        self.show()

    def refresh_header(self):
        # Background
        self.draw.rectangle([(0,0),(self.width,16)], fill=(0xbc,0xb8, 0xb1))
        # Left
        self.draw.text((5,8), f"Fix: {FixTypeTranslator[self.config.fix_type]}",
                       anchor="lm", font=self.hdr_fnt)
        self.draw.text((35,8), f"SV: {str(self.config.sv)}",  anchor="lm",
                       font=self.hdr_fnt)
        # Center
        self.draw.text((self.width//2, 8), f"{self.config.clk_h}:{self.config.clk_min}",
                       anchor="mm", font=self.hdr_fnt)
        # Right
        self.draw.text((self.width-5,8), f"FM: {str(self.config.fusion_mode)}",
                       anchor="rm", font=self.hdr_fnt)

    def refresh_calib(self):
        # Background
        self.draw.rectangle([(0,16),(self.width, 81)], fill=(0x34,0x3a, 0x40))
        # Heading
        self.draw.text((5,20), "CalibStatus", font=self.fnt)
        # Sensor Label
        self.draw.multiline_text((25,35), "GYRO-X\nGYRO-Y\nGYRO-Z", spacing=2, font=self.fnt)
        self.draw.multiline_text((85,35), "ACCEL-X\nACCEL-Y\nACCEL-Z", spacing=2, font=self.fnt)
        
        # Sensor State
        self.update_sensor_colors()
        lamp_x_coord = 65
        lamp_y_coord = 38
        x_offset = 127-lamp_x_coord
        y_offset = 13
        lamp_radius = 7
        
        for x_idx in range(2):
            for y_idx in range(3):
                self.draw.rounded_rectangle([(lamp_x_coord+x_idx*x_offset, 
                                    lamp_y_coord+y_offset*y_idx),
                                    (lamp_x_coord+lamp_radius+x_idx*x_offset, 
                                    lamp_y_coord+lamp_radius+y_offset*y_idx)],
                                    radius=lamp_radius/2, 
                                    fill=self.sensor_states[(x_idx,y_idx)])

    def update_sensor_colors(self):
        for sensor_type, calib_status in self.config.calib_states.items():
            self.sensor_states[SensorToIndexTranlator[sensor_type]] = \
                CalibstatusToColorTranslator[calib_status]

    def show(self):
        self.display.img = self.img.copy()

    def clear(self):
        self.draw.rectangle([(0,0),(self.width,self.height)], fill=(255,255,255))

    def set_config(self, config: GPSConfig):
        self.config = config


    