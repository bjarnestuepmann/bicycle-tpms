#!/usr/bin/python
import smbus2
import math
import time

def read_word(reg):  #reading values from register
	high = bus.read_byte_data(address, reg)
	low = bus.read_byte_data(address, reg+1)
	value = (high << 8) + low

	if (value >= 0x8000):
		return -((65535 - value) + 1)
	else:
		return value
	
def combine_bytes_to_word(low, high):  #reading values from register
    value = (high << 8) + low

    if (value >= 0x8000):
        return -((65535 - value) + 1)
    else:
        return value
   
def get_distance(a,b):
	return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
	radians = math.atan2(x, get_distance(y,z))
	return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
	radians = math.atan2(y, get_distance(x,z))
	return math.degrees(radians)

def get_z_rotation(x,y,z):
  radians = math.atan2(z, get_distance(x,y))
  return math.degrees(radians)

def get_temperature():
  temp = read_word(0x41)
  return (temp / 340) + 36.53

def get_dlpf_cfg():
	cfg_byte = bus.read_byte_data(address, 0x1A)
	# get last three bits from config 
	mask =  0b00000111
	value = cfg_byte & mask
	return int(value)
	

bus = smbus2.SMBus(1)
address = 0x68 # I2C address
# address = 0x69 # alternative I2C address
bus.write_byte_data(address, 0x6b, 0)  #initialize MPU

byte_list = bus.read_i2c_block_data(address, 0x3b, 14)

print(combine_bytes_to_word(byte_list[1], byte_list[0]), read_word(0x3b))
print(combine_bytes_to_word(byte_list[3], byte_list[2]), read_word(0x3d))
print(combine_bytes_to_word(byte_list[5], byte_list[4]), read_word(0x3f))
print()
print(combine_bytes_to_word(byte_list[7], byte_list[6]), read_word(0x41))
print()
print(combine_bytes_to_word(byte_list[9], byte_list[8]), read_word(0x43))
print(combine_bytes_to_word(byte_list[11], byte_list[10]), read_word(0x45))
print(combine_bytes_to_word(byte_list[13], byte_list[12]), read_word(0x37))
