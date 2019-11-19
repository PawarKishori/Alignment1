#!/usr/bin/env python
# coding: utf-8

# In[1]:

import sys
import string

def word(word_id_file):
    with open(word_id_file, "r") as ins:
        lines = ins.readlines()
    array = []
    ewords1 = []
    eword = []
    for line in lines:
        line.strip("(id-word ")
        line.strip('\n')
        array.append(line)
    for i in array:
        str1 = i.split("  ")
      # list slicing
        ewords1 += str1[1::2]
    for i in ewords1:
        i = i.strip(")\n")
        eword.append(i)
    # print(eword)
    return eword


def extract_groups(word_file, id_apertium):
        # hindi_dict_id_root={}
    array = []
    list1 = []
    list2 = []
    list3 = []
    ewords = word(word_file)
    # print(ewords)
    with open(id_apertium, "r") as f:
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
output = extract_groups(input_dict, input_dict1)
with open(output_dict, "w") as out:
    for i in output:
        out.write(i+"\n")
# extract_dictionary_ordered_fact()


# In[ ]:
