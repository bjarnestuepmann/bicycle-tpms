import time

temp_data = dict()
curr_data = [0]*10
for idx in range(10):
    curr_data[idx] = idx

for idx in range(10):
    timestamp = time.time()
    for idx, value in enumerate(curr_data):
        curr_data[idx] = value+1
    
    temp_data[timestamp] = curr_data.copy()

print(temp_data)
