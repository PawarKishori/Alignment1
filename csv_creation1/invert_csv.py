import numpy as np
import csv

with open('H_alignment_parserid.csv') as file:
    lis = [x.replace('\n', '').split(',') for x in file]

x = np.array(lis)

with open('H_alignment_wordid.csv') as file:
    lis = [y.replace('\n', '').split(',') for y in file]

y = np.array(lis)


#print(x)
print(x.T)
with open("H_alignment_parserid_invert.csv",'w') as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerows(x.T)

print(y.T)
with open("H_alignment_wordid_invert.csv",'w') as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerows(y.T)
