#!/usr/bin/env python
# coding: utf-8

# In[37]:
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
    elist=[]
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
        final2=[]
        # print(list2)
        for i in list2:
            eng = ""
            for j in range(0, 1):
                if "@PUNCT-OpenParen@PUNCT-OpenParen - )" in i[1] or "@PUNCT-OpenParen@PUNCT-OpenParen -- )" in i[1]:
                    c = i[0]
                    # print(c)
                    l=len(" @PUNCT-ClosedParen@PUNCT-ClosedParen )")
                    d = list2.index(i)
                    m = list2[d+1][0]
                    # print(list2[d+1][1])
                    str1 = list2[d+1][1]
                    hword=str1[:-l]
                    # print(hword)
                    hword = hword.strip(" ")
                    hword = hword.replace(" ", "_")
                    for k in range(int(c)-1, int(m)):
                        eng = eng+ewords[k]+"_"
                        elist.append(k+1)
                    eng = eng.strip("_")
                    final2.append(eng+"\t"+hword)
                    x=k-(int(m)-int(c))+1    
                    eng=str(x)+"_"+eng
                    
                    final.append(eng+"\t"+hword)
                elif " @PUNCT-ClosedParen@PUNCT-ClosedParen )" not in i[1] and "@PUNCT-OpenParen@PUNCT-OpenParen - )" not in i[1] and "@PUNCT-OpenParen@PUNCT-OpenParen -- )" not in i[1]:
                    c = i[0]
                    # print(i)
                    d = list2.index(i)
                    # print(d)
                    g = int(list2[d][0])
                    # print(g)
                    # print(ewords(g))
                    elist.append(g)
                    hword = list2[d][1].strip(" )")
                    if hword is "":
                        hword="0"
                    final2.append(ewords[g-1]+"\t"+hword)
                    final.append(str(g)+"_"+ewords[g-1]+"\t"+hword)
        for i in range(1,len(ewords)+1):
            if i not in elist:
                final2.append(ewords[i-1]+"\t"+"0")
                final.append(str(i)+"_"+ewords[i-1]+"\t"+"0")      
        return final,final2


        # print(final)
input_dict = sys.argv[1]
input_dict1 = sys.argv[2]
output_dict = sys.argv[3]
output_dict1=sys.argv[4]
# converting_dictionaries_into_list()
output1,output2 = extract_groups(input_dict, input_dict1)
with open(output_dict, "w") as out:
    for i in output1:
        out.write(i+"\n")
with open(output_dict1,"w") as out1:
    for j in output2:
        out1.write(j+"\n")


# extract_dictionary_ordered_fact()
