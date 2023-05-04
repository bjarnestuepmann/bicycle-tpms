from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
import RPi.GPIO as GPIO

import ST7735

disp = ST7735.ST7735(port=0, cs=0, dc=9, backlight=None, rst=25, width=128, height=160, rotation=270, invert=False)

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)

# Load default font.
#font = ImageFont.load_default()
font_small = ImageFont.truetype(font="/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf", size=20)
font_big = ImageFont.truetype(font="/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf", size=60)

# Write some text
dspText = "Countdown"
draw.text((WIDTH//2,HEIGHT//2), dspText, font=font_small, anchor="mm")

# Write buffer to display hardware, must be called to make things visible on the
# display!
disp.display(img)
sleep(3)

for i in reversed(range(11)):
	draw.rectangle(xy=[0,0,160,128], fill=(0,0,0))
	draw.text((WIDTH//2,HEIGHT//2), str(i), font=font_big, anchor="mm")
	disp.display(img)
	sleep(1)

GPIO.cleanup()