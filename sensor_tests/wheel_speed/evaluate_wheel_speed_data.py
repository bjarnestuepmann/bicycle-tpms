
import numpy as np
import matplotlib.pyplot as plt


def read_durations_from_file(file_name):
    durations = list()
    with open(file_name, 'r') as file:
        for line in file:
            durations.append(int(line.replace("\n","")))
    
    return durations


def main():
    current_dir = "/home/pi/Documents/iTPMS/sensor_tests/wheel_speed/data/"
    file_name = current_dir + "durations_ 1682415082.txt"
    durations = read_durations_from_file(file_name)
    print(durations[0])
    
if __name__=="__main__":
   main()