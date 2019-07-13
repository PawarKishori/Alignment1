import numpy as np
import csv

with open('debug_csv.csv') as file:
    lis = [x.replace('\n', '').split(',') for x in file]

x = np.array(lis)
print(x.T)
with open("debug_csv_invert.csv",'w') as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerows(x.T)
