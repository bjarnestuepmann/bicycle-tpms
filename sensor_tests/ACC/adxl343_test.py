import time
import board
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_adxl34x


print("Board ID: ", board.board_id)

i2c_bus_1 = I2C(1, frequency=400_000)
#i2c_bus_1 = board.I2C()

acc_1 = adafruit_adxl34x.ADXL343(i2c_bus_1, 0x53)
acc_2 = adafruit_adxl34x.ADXL343(i2c_bus_1, 0x1d)

acc = [acc_1, acc_2]
# # set data rate and range
# accelerometer.data_rate = adafruit_adxl34x.DataRate.RATE_3200_HZ
# accelerometer.range = adafruit_adxl34x.Range.RANGE_4_G

# # check for success
# # enum is numerated: print shows only the id of value, not the Hz-value
# #print("data_rate: ", accelerometer.data_rate)
# #print("range: ", accelerometer.range)

while True:
    
    print(acc_1.acceleration, acc_2.acceleration)
    time.sleep(0.2)