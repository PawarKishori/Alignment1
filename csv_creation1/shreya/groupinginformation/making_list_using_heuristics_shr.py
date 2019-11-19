#!/usr/bin/env python
# coding: utf-8

# In[4]:

import sys
import string

def name(csv1):
    import csv
    rows=[]
    with open(csv1,'rt')as f:
        data = csv.reader(f)
        for row in data:
            rows.append(row)
        #print(rows)
    #f=open("/home/user/anu_output/ai1E_tmp_11_nov/ai1E_tmp/2.15/sample",'w')
    hindi=[]
    english=[]
    ewords1=[]
    for row in rows[1]:
        #for column in row[1:]:
        #if row!=0:
        hindi.append(row)
    for erow in rows[0]:
        english.append(erow)
    english.remove("English_Word") 
    for i in english:
        str1=i.split('_')
        ewords1+=str1[1::2]
     
    #print(english)
    hindi.remove("K_layer") 
    j=0
    hlist=[]
    x=""
    hlist=[]
    elist=[]
    dict1=[]
    for i in range(len(hindi)):
        c=0
        d=0
        eword=""
        hindi[i]=hindi[i].strip(' ')
        if hindi[i]!="0":
            hindi[i]=hindi[i].replace(' ','_')
            #print(hindi[i])
            #hlist.append(hindi[i])
            for j in hindi[i]:
                if j=='_':
                    c=c+1
            c=c+1
            
            d=hindi.index(hindi[i])
            for k in range(d-c+1,d+1):
                eword=eword+ewords1[k]+"_"
            eword=eword.strip('_')    
            dict1.append(eword+'\t'+hindi[i])  
            #f.write(eword+'\t'+hindi[i]+'\n')
            #print(eword)   
            #meaning_of_every_word_seperately(eword,hindi[i])    
            hlist.append(eword+'\t'+hindi[i]+'\n')
    #print(dict1) 
    #list=meaning_of_every_word_seperately("/home/user/anu_output/ai1E_tmp_11_nov/ai1E_tmp/2.25/sample","/home/user/anusaaraka/Anu_data/domain/tech_sample")  
    return hlist

input_csv = sys.argv[1]
output_dict = sys.argv[2]
# converting_dictionaries_into_list()
output = name(input_csv)
with open(output_dict, "w") as out:
    for i in output:
        out.write(i)
    

#name('/home/user/anu_output/ai1E_tmp_11_nov/ai1E_tmp/2.15/srun_All_Resources_id_word.csv')

