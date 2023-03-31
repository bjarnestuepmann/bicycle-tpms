import numpy as np
import time

dim = 2

data = []
curr = [2]*dim

for cntr in range(10):
    curr[0] = time.time()
    curr[1] = cntr
    data.append(curr.copy())

print(data)