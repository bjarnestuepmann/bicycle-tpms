import time

values = {
    'temp': 0, 
    'bat': 0,
    'pres': 0
}
time_sec = int(time.time())
data = dict()

##### Add values
# key:      timestamp
# values:   dict with sensor values
data[time_sec] = values

# edit values
data[time_sec]['bat'] = 3

print(data)