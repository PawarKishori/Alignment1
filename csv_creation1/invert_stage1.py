import numpy as np
import csv
import re
filename="debug.csv"

with open(filename,'r') as file:
    lis = [x.replace('\n', '').split(',') for x in file]

x = np.array(lis)
print(x.T)
with open("debug_invert.csv",'w') as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerows(x.T)
