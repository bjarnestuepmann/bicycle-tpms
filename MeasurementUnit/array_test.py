import numpy as np

measurement_count = 7

data = np.zeros(shape=(0,measurement_count), dtype=int)
current_data = np.zeros(shape=measurement_count, dtype=int)

for i in range(10):
    np.put(current_data, 0, 0)
    np.put(current_data, 1, 1)
    np.put(current_data, 2, 2)
    np.put(current_data, 3, 3)
    np.put(current_data, 4, 4)
    np.put(current_data, 5, 5)
    np.put(current_data, 6, 6)

    data = np.vstack((data, current_data))

print(data)