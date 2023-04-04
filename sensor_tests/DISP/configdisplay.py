from PIL import Image, ImageDraw, ImageFont
import ST7735

# create an image
width = 160
height = 128
out = Image.new("RGB", (width, height), (255, 255, 255))
# get a font
fnt = ImageFont.truetype("/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf", 10)
# get a drawing context
draw = ImageDraw.Draw(out)

####### Header
hdr_fnt = ImageFont.truetype("/usr/share/fonts/truetype/pyboto/Piboto-Bold.ttf", 9)
draw.rectangle([(0,0),(width,16)], fill=(0xbc,0xb8, 0xb1))
# left
fix = "3D"
draw.text((5,8), f"Fix: {str(fix)}", anchor="lm", font=hdr_fnt)
sv = 3
draw.text((35,8), f"SV: {str(sv)}",  anchor="lm", font=hdr_fnt)
# middle
hour = 22
minute = 22
draw.text((width//2, 8), f"{hour}:{minute}", anchor="mm", font=fnt)
# right
fm = 2
draw.text((width-5,8), f"FM: {str(sv)}", anchor="rm", font=hdr_fnt)

####### CalibStatus
draw.rectangle([(0,16),(width, 81)], fill=(0x34,0x3a, 0x40))
draw.text((5,20), "CalibStatus", font=fnt)

draw.multiline_text((25,35), "GYRO-X\nGYRO-Y\nGYRO-Z", spacing=2, font=fnt)
draw.multiline_text((85,35), "ACCEL-X\nACCEL-Y\nACCEL-Z", spacing=2, font=fnt)
lamp_x_coord = 65
lamp_y_coord = 38
x_offset = 127-lamp_x_coord
y_offset = 13
lamp_radius = 7

#       0         1
# 0     GYRO-X    ACCEL-X
# 1     GYRO-Y    ACCEL-Y
# 2     GYRO-Z    ACCEL-Z

# red:      (0xef,0x43, 0x47)
# blue:     (0x28,0x7d, 0xa1)
# yellow:   (0xf9,0xc7, 0x50)
# green:    (0x90,0xbe, 0x6d)

sensor_states = dict()
sensor_states = {(0,0): (0xef,0x43, 0x47), (1,0): (0x28,0x7d, 0xa1),
                 (0,1): (0xef,0x43, 0x47), (1,1): (0xf9,0xc7, 0x50),
                 (0,2): (0x90,0xbe, 0x6d), (1,2): (0x28,0x7d, 0xa1)}

for x_idx in range(2):
    for y_idx in range(3):
        draw.rounded_rectangle([(lamp_x_coord+x_idx*x_offset, 
                              lamp_y_coord+y_offset*y_idx),
                             (lamp_x_coord+lamp_radius+x_idx*x_offset, 
                             lamp_y_coord+lamp_radius+y_offset*y_idx)],
                            radius=lamp_radius/2, fill=sensor_states[(x_idx,y_idx)])

# Display
disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, 
                     width=128, height=160, rotation=270, invert=False)
disp.display(out)