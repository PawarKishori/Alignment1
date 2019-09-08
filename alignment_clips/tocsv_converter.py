



#log: log_prashant_module
import os
import pandas as pd
import operator
import collections
path = "save_facts1"
pt = 'save_facts_unknown'
path2 = "save_facts2"
open_file = open(path,'r')
#print(open_file.readlines())
open_file1= open(pt,'r')
xxxx=open_file1.readlines()
#print(len(xxxx))
#print(xxxx)
ab1=[]
bc1=[]

for i in range(len(xxxx)):
     kk1=(xxxx[i].split(' '))
     ss1=kk1
     #print(ss1)
     ab1.append(int(kk1[2]))
     bc1.append((" ".join(ss1[3:]))[:-2])
     #print(bc1)
     #print(kk1[2]," ",(",".join(ss1[3:]))[:-2])

#print(ab1)
#print(bc1)

#new_f = open('new_csv.csv','w')
#open_file2=open(path2,'r')
lis = open_file.readlines()
#print(lis)
#lis2 = open_file2.readlines()
#l = lis + lis2
#print(lis2)
#print(len(lis)+len(lis2))
#print(len(lis))
print()
ab=[]
bc=[]
sb1=[]
for i in range(len(lis)):
     kk=(lis[i].split(' '))
     ab.append(int(kk[1]))
     ss=kk
     #print(ss[1]," ",ss[1:][:])
     sb1.append((" ".join(ss[2:])))
     sb1[i]=(sb1[i].replace(")","").replace("\n",""))
     #sb1.append(kk[2].split()[0].strip(")"))
     #print(sb1)
     #print(kk)
     #ab.append(int(kk[2]))
     #bc.append((",".join(ss[3:]))[:-2])
     #print(kk[2]," ",(",".join(ss[3:]))[:-2])
     #print(kk[2:])
#print(ab)
#print(ab+ab1)
#print(sb1+bc1)
#print(bc+bc1)
ab=ab+ab1
bc=sb1+bc1
#print(ab1)
#print(bc1)
'''
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
'''
d= dict()
for i, j in zip(ab,bc):
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
print((pd.DataFrame(list(sorted_x)).T))
#new_f.write((pd.DataFrame(list(sorted_x)).T))

