



#log: log_prashant_module
import os
import pandas as pd
import operator
import collections
path = "save_facts1"
pt = 'save_facts_unknown'
open_file = open(path,'r')
open_file1= open(pt,'r')
unknown_facts=open_file1.readlines()


unknown_english_id=[]
unknown_hindi_id=[]
for i in range(len(unknown_facts)):
     split_=(unknown_facts[i].split(' '))
     unknown_english_id.append(int(split_[2]))                           #english id
     unknown_hindi_id.append((",".join(split_[3:]))[:-2])              #hindi id

final_facts = open_file.readlines()

print()
print(len(final_facts)+len(unknown_facts))
#print()
final_english_id=[]
final_hindi_id=[]
for i in range(len(final_facts)):
     kk=(final_facts[i].split(' '))
     final_english_id.append(int(kk[2]))                             #final english id
     final_hindi_id.append((",".join(kk[3:]))[:-2])                #final hindi id

#print()

ab=unknown_english_id+final_english_id
bc=unknown_hindi_id+final_hindi_id

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
x.to_csv('new_N1.csv', index=False, header=False)
print((pd.DataFrame(list(sorted_x)).T))
#new_f.write((pd.DataFrame(list(sorted_x)).T))

