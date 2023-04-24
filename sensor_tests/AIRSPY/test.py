from time import time_ns
from datetime import datetime

nanos = time_ns()
secs = nanos / 1e9
dt = datetime.fromtimestamp(secs)
print(dt.strftime('%H:%M:%S.%f'))