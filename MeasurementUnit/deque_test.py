from collections import deque
from time import sleep

q = deque(maxlen=5)
for idx in range(10):
    q.append(idx)
    print(list(q))
    sleep(0.5)
