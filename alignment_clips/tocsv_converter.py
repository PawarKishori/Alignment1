import os
import pandas as pd
import operator
import collections

path = "save_facts1"
pt = 'save_facts_unknown'
path2 = "save_facts2"
open_file = open(path,'r')
open_file1= open(pt,'r')
xxxx=open_file1.readlines()

ab1=[]
bc1=[]

for i in range(len(xxxx)):
     kk1=(xxxx[i].split(' '))
     ss1=kk1
     #print(ss1)
     ab1.append(int(kk1[2]))
     bc1.append((" ".join(ss1[3:]))[:-2])

lis = open_file.readlines()

ab=[];bc=[];sb1=[]

for i in range(len(lis)):
     kk=(lis[i].split(' '))
     ab.append(int(kk[1]))
     ss=kk
     #print(ss[1]," ",ss[1:][:])
     sb1.append((" ".join(ss[2:])))
     sb1[i]=(sb1[i].replace(")","").replace("\n",""))

ab=ab+ab1
bc=sb1+bc1

d= dict()
for i, j in zip(ab,bc):
    d[i]=j


for key in sorted(d.keys()):
     (key,d[key])


sorted_x = sorted(d.items(), key=operator.itemgetter(0))
sorted_dict = collections.OrderedDict(sorted_x)

x = (pd.DataFrame(list(sorted_x)).T)
x.to_csv('new_N1.csv', sep=',', index=False, header=False)
print((pd.DataFrame(list(sorted_x)).T))


