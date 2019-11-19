#!/usr/bin/env python
# coding: utf-8

# In[28]:


import re
import string
import sys


def make_lists_from_single_word_dictionary(dict):
    with open(dict, "r+") as ins:
        array = []
        lines = ins.readlines()
    desired_lines = lines[0:]
    for line in desired_lines:
        if line[0] != '#':
            array.append(line)
    # print(array)
    ewords1 = []
    hwords1 = []
    ewords = []
    hwords = []
    hwords2 = []
    for i in array:
        str1 = i.split('\t')
        ewords1 += str1[::2]  # list slicing
        hwords1 += str1[1::2]  # list slicing
        #ewords = [x.lower() for x in ewords]
    # print(ewords1)
    for m in hwords1:
        m = m.strip('\n')
        hwords2.append(m)
    for n in ewords1:
        n = n.strip('_noun')
        ewords.append(n)
    list1 = []
    for k in hwords2:
        list1 = k.split('/')
        hwords.append(list1)
    # print(hwords)
    return ewords, hwords


def make_lists_from_multi_word_dictionary(dict):
    with open(dict, "r+") as ins:
        array = []
        lines = ins.readlines()
    desired_lines = lines[0:]
    for line in desired_lines:
        if line[0] != '#':
            array.append(line)
    # print(array)
    ewords1 = []
    hwords1 = []
    ewords = []
    hwords = []
    hwords2 = []
    d = ""
    for i in array:
        str1 = i.split('\t')
        ewords1 += str1[::2]  # list slicing
        hwords1 += str1[1::2]  # list slicing
        ewords = [x.lower() for x in ewords1]
    # print(ewords)
    for j in hwords1:
        d = ""
        for k in j:
            if k != '#':
                d = d+k
            elif k == '#':
                break
        hwords.append(d)
    # print(ewords1)
    list1 = []
    list2 = []
    for n in ewords1:
        list1 = n.split('_')
        list2.append(list1)
    # print(list2)
    # hwords2=[]
    # for i in hwords:
        #str=i.replace('_',' ')
        # hwords2.append(str)
    # print(hwords)
    for m in hwords:
        m = m.strip('\n')
        hwords2.append(m)
    return list2, hwords2


def meaning_of_every_word_seperately(dict1, dict2):
    elist, hlist = make_lists_from_multi_word_dictionary(dict1)
    elist1, hlist1 = make_lists_from_single_word_dictionary(dict2)
    # print(hlist)
    list2 = []
    list3 = []
    haligned = []
    ealigned = []
    g = []
    y = 0
    # print(elist)
    z = 0
    for i in elist:
        # print(i)
        list1 = []
        str1 = ""
        v = 0
        y = 0
        for j in i:
            # print(j)
            c = 0
            for m in elist1:
                if j == m:
                    v += 1
                    # print(m)
                    # print("true")
                    x = elist1.index(m)
                    y = elist.index(i)
                    for k in hlist1[x]:
                        # print(k)
                        if k in hlist[y]:
                            list1.append(m+":"+k+" ")
                            #str1=str1.join(m+" <> "+k+" ")
                            c += 1
                            hlist[y] = hlist[y].strip(k)
                            # print(str1)
                        # else:
                            #list1.append(j+" <> "+"-")
            if c == 0:
                ealigned.append(j)
                #list1.append(j+" <> "+"?")
                #str1=str1.join(j+" <> "+"?"+" ")
        # print(y)
        if v != 0:
            # print(hlist[y])
            g = hlist[y].split('_')
            g = list(filter(None, g))
            if len(ealigned) <= len(g):
                for l in range(len(ealigned)):
                    # print(l)
                    list1.append(ealigned[l]+":"+g[l]+"?"+" ")
            elif len(ealigned) >= len(g):
                for l in range(len(g)):
                    # print(l)
                    list1.append(ealigned[l]+":"+g[l]+"?"+" ")
        elif v == 0:
            haligned = hlist[z].split('_')
            # print(hlist[z])
            if len(ealigned) <= len(haligned):
                for l in range(len(ealigned)):
                    # print(l)
                    list1.append(ealigned[l]+":"+haligned[l]+"?"+" ")
            elif len(ealigned) > len(haligned):
                for l in range(len(haligned)):
                    # print(l)
                    list1.append(ealigned[l]+":"+haligned[l]+"?"+" ")
        eng = '_'.join(i)
        haligned = []
        ealigned = []
        g = []
        z += 1
        list2.append(eng+"\t"+''.join(list1))
        # list2.append(str1)
    return(list2)
    # for i in list2:
    #str1 = "".join(i)
    # print(str1)
    # list3.append(str1)
    # print(list3)
    # return list3


input_dict = sys.argv[1]
input_dict1 = sys.argv[2]
output_dict = sys.argv[3]
# converting_dictionaries_into_list()
output = meaning_of_every_word_seperately(input_dict, input_dict1)
with open(output_dict, "w") as out:
    for i in output:
        out.write(i+"\n")
# meaning_of_every_word_seperately("/home/user/anusaaraka/Anu_data/domain/multi_word_dic/tech_sample2","/home/user/anusaaraka/Anu_data/domain/tech_sample")


# In[ ]:
