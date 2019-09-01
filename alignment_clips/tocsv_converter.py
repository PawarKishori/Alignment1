import os
import pandas as pd
import operator
import collections
path = "save_facts1"
path2 = "save_facts2"
open_file = open(path,'r')
open_file2=open(path2,'r')
lis = open_file.readlines()
lis2 = open_file2.readlines()
l = lis + lis2
print(lis)
print(lis2)
#print(len(lis)+len(lis2))
print()
kk=[]
bb=[]
for i in range(len(lis)+len(lis2)):
    kk.append(int(l[i].split()[2]))
    bb.append(" ".join(l[i].split()[3:]).strip(')'))
    print(l[i].split()[2])
    print((l[i].split()[3]))
print()
print(kk)
print(bb)
print("------------------")

d= dict()
for i, j in zip(kk,bb):
    d[i]=j
    #print(i," ",d[i])
#d = sorted(d)
for key in sorted(d.keys()):
     (key,d[key])
     #pd.DataFrame(d)
#print(d)
sorted_x = sorted(d.items(), key=operator.itemgetter(0))
sorted_dict = collections.OrderedDict(sorted_x)
#print(sorted_x[0])
x = (pd.DataFrame(list(sorted_x)).T)
x.to_csv('new_N1.csv', sep=',', index=False, header=False)
#x.to_csv('new_N1.csv', sep=',')
print((pd.DataFrame(list(sorted_x)).T))
#new_f.write((pd.DataFrame(list(sorted_x)).T))


