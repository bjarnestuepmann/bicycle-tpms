import struct

def hex_word_to_float(hex: str, byte_order: str):
    # big-endian float
    # https://docs.python.org/3/library/struct.html#format-characters
    if byte_order == "big":
        return struct.unpack('>f', bytes.fromhex(hex))[0]
    elif byte_order == "little":
        return struct.unpack('<f', bytes.fromhex(hex))[0]
    else:
        return -1

f = open('/home/pi/Documents/iTPMS/sensor_tests/AIRSPY/sensor_values.txt', 'r')
# for hex_data in f:
#     hex_data_no_nl = hex_data.replace('\n', '')
#     print(hex_data_no_nl)
#     data = bytes.fromhex(hex_data_no_nl)
#     if len(data) == 15:
#         raw_man_id = data[0:2]
#         raw_payload = data[2]
#         raw_pressure = data[3:7]
#         raw_temp = data[7:11]
#         raw_battery = data[11:15]
#         print('Temp:', hex_word_to_float(raw_temp.hex()))
#         print('Pressure:', hex_word_to_float(raw_pressure.hex()))

# data = "42100000"
# print(struct.unpack('>f', bytes.fromhex(data))[0])

for hex_data in f:
    hex_data_no_nl = hex_data.replace('\n', '')
    print(hex_data_no_nl)
    # l = len(hex_data_no_nl)
    # if hex_data_no_nl[l-4:l] == "1e0d":
    #     print("Temp:", hex_word_to_float(hex_data_no_nl[0:4*2], "little"))
    #     print("Battery:", hex_word_to_float(hex_data_no_nl[7*2:11*2], "little"))
    byte_data = bytes.fromhex(hex_data_no_nl)
    if len(byte_data) == 15:
        for i in range(len(byte_data)-3):
            word = byte_data[i:i+4]
            print(word)
            print(f"[{i}:{i+4}]", hex_word_to_float(word.hex(), byte_order="little"))
        print("________________")