#!/usr/bin/env python
# coding: utf-8

# In[101]:


import string
import sys


def csv_conversion(csv):
    with open(csv, "r") as ins:
        lines = ins.readlines()
    array = []
    for line in lines:
        array.append(line)
    # print(array)
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    for i in array:
        str1 = i.split("\t")
        list1 += str1[::2]
        list2 += str1[1::2]
    for i in list1:
        j = i.split("_", 1)
        list3.append(j)
    # print(list2)
    # print(list3)
    list7 = []
    for i in list3:
        list5.append(i[0])
        i.remove(i[0])
        list6.append((i))
    # print(list5)
    # print(list3)
    c = 0
    x = 0
    list8 = []
    # print(list5)
    y = 0
    for i in list6:
        eng = []
        z = int(list5[y])
        for j in i:
            if "_"in j:
                eng = j.split("_")
        if len(eng) != 0:
            eng[0] = "(("+eng[0]
            eng[len(eng)-1] = eng[len(eng)-1]+"))"
            for k in range(len(eng)):
                list7.insert(x, eng[k])
                x += 1
                list8.append(z)
                z = z+1
            y = y+1

        else:
            list7.insert(x, i[0])
            x += 1
            list8.append(z)
            y = y+1
    # print(list7)
    # print(list8)
    dict1 = {}
    dict2 = {}
    dict2 = dict(zip(list8, list7))

    # print(list2)
    # print(dict2)
    # return dict1
    hindi = []
    hindi1 = []
    for i in list2:
        c = 0
        for j in i:
            if j == ":":
                c = c+1
        if c > 1:
            hindi1 = i.split(" ")
            # print(hindi1)
            for k in hindi1:
                hindi.append(k)
        else:
            hindi.append(i)
    # print(hindi)
    hwords = []
    hwords1 = []
    ewords = []
    for i in hindi:
        str1 = i.split(":")
        ewords += str1[::2]
        hwords1 += str1[1::2]
    for i in hwords1:
        i = i.strip("\n")
        hwords.append(i)
    dict1 = dict(zip(list8, hwords))
    # print(dict1)
    # print(dict2)
    str1=str(dict1)
    str2=str(dict2)
    print(dict1)
    print(dict2)
    ll=[]; kk=[]
    for k,v in sorted(dict2.items()):
        ll.append(v)
    final={}
    print('+++++++++++++++++++++++++++++++++++++')
    for i,j in zip(sorted(dict1.items()),ll):
        #tmp = i[1].strip("\n").strip('?')
        tmp = i[1].strip("\n").strip(' ').strip('?')
        #print(tmp)
        neq = tmp
        if '((' in j:
            #print(")))",j)
            neq='(('+tmp
            #print(neq)
        if '))' in j:
            neq=tmp+'))'
        #print(i[0],neq)
        final[i[0]]=neq
        kk.append(neq)
    kk.insert(0,"K_enhanced")
    csv_final= ",".join(kk) 
    return csv_final


input_dict = sys.argv[1]
output_csv = sys.argv[2]
csv_final = csv_conversion(input_dict)
print("==>",csv_final)

with open(output_csv, "w") as out:
    out.write(csv_final)
        
'''with open(output_dict1, "w") as out1:
    out1.write(output2)'''
        
# csv_conversion()
