#!/usr/bin/env python
# coding: utf-8

# In[134]:


import re
import os
import sys

def name(csv1):
    import csv
    rows = []
    with open(csv1, 'rt')as f:
        data = csv.reader(f)
        for row in data:
            rows.append(row)
        # print(rows)
    # f=open("/home/user/anu_output/ai1E_tmp_11_nov/ai1E_tmp/2.26/sample",'w')
    hindi = []
    english = []
    ewords1 = []
    for row in rows[1]:
        # for column in row[1:]:
        # if row!=0:
        hindi.append(row)
    for erow in rows[0]:
        english.append(erow)
    english.remove("English_Word")
    for i in english:
        str1 = i.split('_')
        ewords1 += str1[1::2]
    return ewords1


def extract_dictionary_ordered_fact(csv, group_file):
    array = []
    list1 = []
    list2 = []
    list3 = []
    ewords = name(csv)
    # print(ewords)
    with open(group_file, "r") as f:
        data = f.read().split("\n")
        # print(array)
        for i in data:
            i = i.lstrip("(id-Apertium_output ")
            list1.append(i)

        # print(list1)
        for i in list1:
            i = i.split(" ", 1)
            # print(i)
            list2.append(i)
        list2 = list2[:-1]
        # print(list2)
        final = []
        for i in list2:
            eng = ""
            for j in range(len(i)):
                if "@PUNCT-OpenParen@PUNCT-OpenParen - )" in i[j] or "@PUNCT-OpenParen@PUNCT-OpenParen -- )" in i[j]:
                    c = i[0]
                    # print(c)
                    # print(ewords[5])
                    d = list2.index(i)
                    m = list2[d+1][0]
                    # print(list2[d+1][1])
                    hword = list2[d +
                                  1][1].strip(" @PUNCT-ClosedParen@PUNCT-ClosedParen )")
                    # print(hword)
                    hword = hword.strip(" ")
                    hword = hword.replace(" ", "_")
                    for k in range(int(c)-1, int(m)):
                        eng = eng+ewords[k]+"_"
                    eng = eng.strip("_")
                    final.append(eng+"\t"+hword)
        return(final)

        # print(final)
input_dict = sys.argv[1]
input_dict1 = sys.argv[2]
output_dict = sys.argv[3]
# converting_dictionaries_into_list()
output = extract_dictionary_ordered_fact(input_dict, input_dict1)
with open(output_dict, "w") as out:
    for i in output:
        out.write(i+"\n")

# extract_dictionary_ordered_fact()


# In[ ]:
