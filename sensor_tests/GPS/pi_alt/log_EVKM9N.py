from pyubx2 import UBXReader
import serial
import os
import RPi.GPIO as GPIO
from datetime import *
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735

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



#port_r = '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00'
port_r = '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_R-if00'
port_a = '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiverA-if00'
port_b = '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00'
port_c = '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiverC-if00'
port_d = '/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiverD-if00'
##usb_1=serial.Serial('/dev/ttyACM0',34800)
usb_r=serial.Serial(port_r,34800)
usb_1=serial.Serial(port_a,34800)
usb_2=serial.Serial(port_b,34800)
usb_3=serial.Serial(port_c,34800)
usb_4=serial.Serial(port_d,34800)
"""
X = 15
while True:

	if not GPIO.input(pin_A): 
		draw.text((5, X), "Remote A", font=font)
		disp.display(img)	
		time.sleep(0.1)	
		X+=10
	if not GPIO.input(pin_B): 
		draw.text((5, X), "Remote B", font=font)
		disp.display(img)
		time.sleep(0.1)	
		X+=10
	if not GPIO.input(pin_C): 
		draw.text((5, X), "Remote C", font=font)
		disp.display(img)
		time.sleep(0.1)	
		X+=10
	if not GPIO.input(pin_D): 
		draw.text((5, X), "Remote D", font=font)
		disp.display(img)
		time.sleep(0.1)	
		X+=10
"""
timeflag=1
led_pin=17
#GPIO.setup(led_pin, GPIO.OUT)
#GPIO.output(led_pin, GPIO.LOW)
#GPIO.output(led_pin, GPIO.HIGH)
#GPIO.output(led_pin, GPIO.LOW)
#print "Please enter Date and Time with format -- WeekDay Month Day hh:mm:ss  : (e.g   Mon Apr 31 20:11:01)"
# current_time=raw_input("Please enter Date and Time with format -- YYYY-MM-DD hh:mm:ss  : e.g  2022-04-31 20:59:55 ")
#
# print(current_time)

#### Initiallize display ####
#GPIO.setup(2, GPIO.OUT)
#GPIO.output(2, True)
disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=128, height=160, rotation=270, invert=False)
width = disp.width
height = disp.height
img = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(img)

image_index = 0

draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
image = Image.open("/home/pi/Display/Canyon5.jpg")
# Scale the image to the smaller screen dimension
image_ratio = image.width / image.height
screen_ratio = width / height
if screen_ratio < image_ratio:
	scaled_width = image.width * height // image.height
	scaled_height = height
else:
	scaled_width = width
	scaled_height = image.height * width // image.width
image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

# Crop and center the image
x = scaled_width // 2 - width // 2
y = scaled_height // 2 - height // 2
image = image.crop((x, y, x + width, y + height))

# Display image.
disp.display(image)
image_array =["canyon1.png", "bild3.png", "bild1.png","bild4.jpg","bild6.png","bild7.png","bild8.png","bild9.png","Canyon_0.jpg", "Canyon5.jpg", "canyon2.png"]


def show_image(image_string):
	image_string = "/home/pi/Display/"+str(image_string)
	draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
	image = Image.open(image_string)#"/home/pi/Display/canyon2.png")
	# Scale the image to the smaller screen dimension
	image_ratio = image.width / image.height
	screen_ratio = width / height
	if screen_ratio < image_ratio:
		scaled_width = image.width * height // image.height
		scaled_height = height
	else:
		scaled_width = width
		scaled_height = image.height * width // image.width
	image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

	# Crop and center the image
	x = scaled_width // 2 - width // 2
	y = scaled_height // 2 - height // 2
	image = image.crop((x, y, x + width, y + height))

	# Display image.
	disp.display(image)
	#time.sleep(2)


while GPIO.input(pin_D): 

	if not GPIO.input(pin_A):
		if image_index == 10:
			image_index = 0
		else:
			image_index += 1
		show_image(image_array[image_index])
		time.sleep(0.2)

	if not GPIO.input(pin_B):
		if image_index == 0:
			image_index = 10
		else:
			image_index -= 1
		show_image(image_array[image_index])
		time.sleep(0.2)





while True:
	show_image("Canyon_0.jpg")
	time.sleep(1)
	draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
	# Load default font.
	font = ImageFont.load_default()
	# Write some text
	draw.text((5, 5), "Starting GPS Test...", font=font, fill=(255, 255, 255))
	# Write buffer to display hardware, must be called to make things visible on the
	# display!
	disp.display(img)
	################################################################




	#readedText = ser.readline()
	draw.text((5, 15), "Waiting for GPS FIX...", font=font)
	disp.display(img)


	while timeflag:
		ubr_usb_r = UBXReader(usb_r)
		(raw_data, parsed_data) = ubr_usb_r.read()
		if parsed_data.identity == "GNZDA":
			time_start = str(parsed_data.time)
			time_start = str(time_start).replace(':','')
			date = str(parsed_data.day) + str(parsed_data.month) + str(parsed_data.year)
			os.system("sudo date +%T --set="+"\""+str(parsed_data.time)+"\"")
			print(date)
			print(time_start)
			timeflag=0
		else:
			continue

	c=[0,0,0,0,0]
	lat_init=[0,0,0,0,0]
	long_init=[0,0,0,0,0]

	while c[0] != 1:
		try: 
			ubr_usb_r = UBXReader(usb_r)
			(raw_data, parsed_data) = ubr_usb_r.read()
			if parsed_data.identity == "GNGGA":
				if parsed_data.quality > 0:
					c[0]=1
					lat_init[0]=parsed_data.lat
					long_init[0]=parsed_data.lon
				else:
					continue
			else:
				continue
		except Exception as e:
			print("Reference error: "+str(e))
	print("R OK")
	draw.text((5, 25), "R ", font=font)
	while c[1] != 1:
		ubr_usb_1 = UBXReader(usb_1)
		(raw_data, parsed_data) = ubr_usb_1.read()
		if parsed_data.identity == "GNGGA":
			if parsed_data.quality > 0:
				c[1]=1
				lat_init[1]=parsed_data.lat
				long_init[1]=parsed_data.lon
			else:
				continue
		else:
			continue
	print("1 OK")
	draw.text((15, 25), "1 ", font=font)
	while c[2] != 1:
		ubr_usb_2 = UBXReader(usb_2)
		(raw_data, parsed_data) = ubr_usb_2.read()
		if parsed_data.identity == "GNGGA":
			if parsed_data.quality > 0:
				c[2]=1
				lat_init[2]=parsed_data.lat
				long_init[2]=parsed_data.lon
			else:
				continue
		else:
			continue

	print("2 OK")
	draw.text((25, 25), "2 ", font=font)
	while c[3] != 1:
		ubr_usb_3 = UBXReader(usb_3)
		(raw_data, parsed_data) = ubr_usb_3.read()
		if parsed_data.identity == "GNGGA":
			if parsed_data.quality > 0:
				c[3]=1
				lat_init[3]=parsed_data.lat
				long_init[3]=parsed_data.lon
			else:
				continue
		else:
			continue
    
	print("3 OK")
	draw.text((35, 25), "3 ", font=font)
	while c[4] != 1:
		ubr_usb_4 = UBXReader(usb_4)
		(raw_data, parsed_data) = ubr_usb_4.read()
		if parsed_data.identity == "GNGGA":
			if parsed_data.quality > 0:
				c[4]=1
				lat_init[4]=parsed_data.lat
				long_init[4]=parsed_data.lon
			else:
				continue
		else:
			continue
	print("4 OK")
	draw.text((45, 25), "4-OK", font=font)
	print('OK position fixed on all channels')
	draw.text((5, 35), "All GPS FIXED", font=font)
	disp.display(img)
	#GPIO.output(led_pin, GPIO.HIGH)

	#Create a folder per each test
	test_counter=0


	for name in os.listdir("/home/pi/"):
		if os.path.isdir("/home/pi/"+name):
			if name[0:9] == "GPS_TEST_":
				test_counter+=1


	draw.text((5, 45), "Start test "+str(test_counter)+"?", font=font)
	disp.display(img)
	while GPIO.input(pin_A): 
		time.sleep(0.2)

	test_folder="GPS_TEST_"+str(test_counter)+"_{0}".format(time_start+date)
	print(test_folder)
	if not os.path.exists('/home/pi/'+test_folder):
		os.makedirs('/home/pi/'+test_folder)
	error_log=open('/home/pi/'+test_folder+'/{0}.txt'.format('error_'+str(test_counter)+'_'+time_start+date),'w')
	log_file_r=open('/home/pi/'+test_folder+'/{0}.txt'.format('usb_r_'+str(test_counter)+'_'+time_start+date),'w')
	log_file_1=open('/home/pi/'+test_folder+'/{0}.txt'.format('usb_1_'+str(test_counter)+'_'+time_start+date),'w')
	log_file_2=open('/home/pi/'+test_folder+'/{0}.txt'.format('usb_2_'+time_start+date),'w')
	log_file_3=open('/home/pi/'+test_folder+'/{0}.txt'.format('usb_3_'+str(test_counter)+'_'+time_start+date),'w')
	log_file_4=open('/home/pi/'+test_folder+'/{0}.txt'.format('usb_4_'+str(test_counter)+'_'+time_start+date),'w')

	draw.text((5, 55), "Test "+str(test_counter)+" running", font=font)
	disp.display(img)

	while GPIO.input(pin_B): 
	#while True:
		if usb_r.inWaiting():
			tnow=datetime.now()
			try: 
				ubr_usb_r = UBXReader(usb_r)
				(raw_data_r, parsed_data_r) = ubr_usb_r.read()
				data_r = tnow.strftime("%H:%M:%S")+','+str(parsed_data_r)+"\n"
				data_r = data_r.replace("<NMEA(","")
				data_r = data_r.replace(")>","")
				log_file_r.write(data_r)
			except Exception as e:
				data_e = tnow.strftime("%H:%M:%S")+', USB_R: ,'+str(e)+"\n"
				error_log.write(data_e)
				print("USB_R: " + str(e))

			try: 		
				ubr_usb_1 = UBXReader(usb_1)
				(raw_data_1, parsed_data_1) = ubr_usb_1.read()
				data_1 = tnow.strftime("%H:%M:%S")+','+str(parsed_data_1)+"\n"
				data_1 = data_1.replace("<NMEA(","")
				data_1 = data_1.replace(")>","")
				log_file_1.write(data_1)
			except Exception as e:
				data_e=tnow.strftime("%H:%M:%S")+', USB_1:'+str(e)+"\n"
				error_log.write(data_e)
				print("USB_1: " + str(e))
			
			try: 		
				ubr_usb_2 = UBXReader(usb_2)
				(raw_data_2, parsed_data_2) = ubr_usb_2.read()
				#		print (tnow.strftime("%H:%M:%S"))
				data_2=tnow.strftime("%H:%M:%S")+','+str(parsed_data_2)+"\n"
				data_2 = data_2.replace("<NMEA(","")
				data_2 = data_2.replace(")>","")
				log_file_2.write(data_2)
			except Exception as e:
				data_e=tnow.strftime("%H:%M:%S")+', USB_2:'+str(e)+"\n"
				error_log.write(data_e)
				print("USB_2: " + str(e))
			

			try: 		
				ubr_usb_3 = UBXReader(usb_3)
				(raw_data_3, parsed_data_3) = ubr_usb_3.read()
				data_3 = tnow.strftime("%H:%M:%S")+','+str(parsed_data_3)+"\n"
				data_3 = data_3.replace("<NMEA(","")
				data_3 = data_3.replace(")>","")
				log_file_3.write(data_3)
			except Exception as e:
				data_e=tnow.strftime("%H:%M:%S")+', USB_3:'+str(e)+"\n"
				error_log.write(data_e)
				print("USB_3: " + str(e))

			try: 		
				ubr_usb_4 = UBXReader(usb_4)
				(raw_data_4, parsed_data_4) = ubr_usb_4.read()
				data_4 = tnow.strftime("%H:%M:%S")+','+str(parsed_data_4)+"\n"
				data_4 = data_4.replace("<NMEA(","")
				data_4 = data_4.replace(")>","")
				log_file_4.write(data_4)
			except Exception as e:
				data_e=tnow.strftime("%H:%M:%S")+', USB_4:'+str(e)+"\n"
				error_log.write(data_e)
				print("USB_4: " + str(e))


		#		print(data_r)
		#	   	data_2=tnow.strftime("%H:%M:%S")+','+usb_2.readline()
		#	   	data_3=tnow.strftime("%H:%M:%S")+','+usb_3.readline()
		#	   	data_4=tnow.strftime("%H:%M:%S")+','+usb_4.readline()
		#		log_file_r.write(data_r)
		#		log_file_1.write(data_1)
		#		log_file_2.write(data_2)
		#		log_file_3.write(data_3)
		#		log_file_4.write(data_4)
				#print(data)



log_file.flush()
#usb_r.close()
#usb_1.close()
#usb_2.close()
usb_3.close()
usb_4.close()
#log_file_r.close()
#log_file_1.close()
#log_file_2.close()
log_file_3.close()
log_file_4.close()
GPIO.cleanup()


###################################################################
###################################################################

while timeflag:
	ubr = UBXReader(usb_r)
	if parsed_data.identity == "GNZDA":
		time = parsed_data.time
	os.system("sudo date +%T --set="+"\""+timenew+"\"")
	if usb_r.inWaiting():
		#data=usb_r.readline()
		if data.find("$GNZDA") > -1:
			datacheck=data.split(",")[1]
			print(datacheck)
			if datacheck != '':
				timeflag=0
				data=data.replace('$GNZDA,','')
				data=data.replace(',','')
				curr_time=data.replace('.','')
				time=data[0:data.find(".")]
				time=data.split(".")[0]
				date=data.split(".")[1]
				date=date[2:10]
				timenew=time[0:2]+':'+time[2:4]+':'+time[4:6]
				print(timenew)
				print(date)
				os.system("sudo date +%T --set="+"\""+timenew+"\"")
				#os.system("sudo date --set="+"\""+date+time+"\"")
				#os.system("sudo date +%T --set="+"\""+timenew+"\"")
				#log_file=open('{0}.txt'.format('usb_'+time+date),'w')
		else:
		     	continue

c=[0,0,0,0,0]
lat_init=[0,0,0,0,0]
long_init=[0,0,0,0,0]

while c[0] != 1:
	if usb_r.inWaiting():
		fix=usb_r.readline()
		#print(fix)
		if fix.find("$GNGGA") > -1:
			#print(fix)
			fixcheckR=fix.split(",")[3]
			if fixcheckR != '':
				c[0]=1
				lat_init[0]=fix.split(',')[3]
				long_init[0]=fix.split(',')[5]
				#print('\nRiferimento lat:',lat[0],' e long:', long[0])
				#print(fix)
			else:
				continue
	else:
		continue
"""
while c[1] != 1:
	if usb_1.inWaiting():
		fix=usb_1.readline()
		if fix.find("$GNGGA") > -1:
			fixcheck1=fix.split(",")[3]
			if fixcheck1 != '':
				c[1]=1
				lat_init[1]=fix.split(',')[3]
				long_init[1]=fix.split(',')[5]
				#print('\nUsbA lat:',lat[1],'e long:',long[1])
				#print(fix)
			else:
				continue
		else:
			continue

"""






"""
while c[2] != 1:
	if usb_2.inWaiting():
		fix = usb_2.readline()
		if fix.find("$GNGGA") > -1:
			fixcheck2=fix.split(",")[3]
			if fixcheck2 != '':
				c[2]=1
				lat_init[2]=fix.split(',')[3]
				long_init[2]=fix.split(',')[5]
				#print('\nUsbB lat:',lat[2],'e long:',long[2])
				#print(fix)
			else:
				continue
	else:
		continue



while c[3] != 1:
	if usb_3.inWaiting():
		fix = usb_3.readline()
		if fix.find("$GNGGA") > -1:
			fixcheck3=fix.split(",")[3]
			if fixcheck3 != '':
				c[3]=1
				lat_init[3]=fix.split(',')[3]
				long_init[3]=fix.split(',')[5]
				#print('\nUsbC lat:',lat[3],'e long:',long[3])
				#print(fix)
			else:
				continue
		else:
			continue


while c[4] != 1:
	if usb_4.inWaiting():
		fix = usb_4.readline()
		if fix.find("$GNGGA") > -1:
			fixcheck4=fix.split(",")[3]
			if fixcheck4 != '':
				c[4]=1
				lat_init[4]=fix.split(',')[3]
				long_init[4]=fix.split(',')[5]
				#print('\nUsbD lat:',lat[4],'e long:',long[4])
			else:
				continue
		else:
			continue

"""
print('OK position fixed on all channels')
GPIO.output(led_pin, GPIO.HIGH)
log_file_r=open('/home/pi/{0}.txt'.format('usb_r_'+time+date),'w')
log_file_1=open('/home/pi/{0}.txt'.format('usb_1_'+time+date),'w')
#log_file_2=open('/home/pi/{0}.txt'.format('usb_2_'+time+date),'w')
#log_file_3=open('/home/pi/{0}.txt'.format('usb_3_'+time+date),'w')
#log_file_4=open('/home/pi/{0}.txt'.format('usb_4_'+time+date),'w')
#log_file.write(lat)
#log_file.write(long)
#log_file.close



while True:
	if usb_r.inWaiting():
		tnow=datetime.now()
#		print (tnow.strftime("%H:%M:%S"))
		data_r=tnow.strftime("%H:%M:%S")+','+usb_r.readline()
		data_1=tnow.strftime("%H:%M:%S")+','+usb_1.readline()
		print(data_1)
#	   	data_2=tnow.strftime("%H:%M:%S")+','+usb_2.readline()
#	   	data_3=tnow.strftime("%H:%M:%S")+','+usb_3.readline()
#	   	data_4=tnow.strftime("%H:%M:%S")+','+usb_4.readline()
		log_file_r.write(data_r)
		log_file_1.write(data_1)
#		log_file_2.write(data_2)
#		log_file_3.write(data_3)
#		log_file_4.write(data_4)
		#print(data)

log_file.flush()
usb_r.close()
usb_1.close()
#usb_2.close()
#usb_3.close()
#usb_4.close()
log_file_r.close()
log_file_1.close()
#log_file_2.close()
#log_file_3.close()
#log_file_4.close()
GPIO.cleanup()
