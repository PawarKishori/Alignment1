#!/usr/bin/env python
# coding: utf-8

# In[1]:



# In[2]:


##CREATION OF PYTHON DICTS and LISTS FROM NECESSARY FILES
import sys, os, pandas as pd, numpy as np, itertools, re
pd.options.display.max_columns = None

#Specify path of sentence:
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
#eng_file_name = 'cc_conjE'
eng_file_name = sys.argv[1]

sent_no = sys.argv[2]
#sent_no = '2.1' #2.29, 2.21, 2.61, 2.14, 2.64
path_tmp= tmp_path + eng_file_name + "_tmp/" + sent_no
filename =path_tmp +  '/H_wordid-word_mapping.dat'
efilename = path_tmp + '/E_wordid-word_mapping.dat'


roja_transliterate_file = path_tmp +  '/results_of_transliteration.dat'
nandani_file = path_tmp +  '/corpus_specific_dic_facts_for_one_sent.dat'

data=""; tranliterate_dict={}
def extract_dictionary_from_deftemplate(filename):
    with open(filename, "r") as f:
        data = f.read().split("\n")
#         print(data)
        while "" in data:
            data.remove("")
            
        tranliterate_dict={}

        for line in data:
#             print(line)
            key = line.split(")")[0].lstrip("Edict-Hdict (E_id ")
            val = line.split(")")[2].lstrip("(H_id ")
#             print(key, val)
            tranliterate_dict[key]=val
    return(tranliterate_dict)

try:
    transliterate_mapping = extract_dictionary_from_deftemplate(roja_transliterate_file)  
    print(transliterate_mapping)

except:
    print("FILE MISSING: " + roja_transliterate_file )
nandani_mapping = extract_dictionary_from_deftemplate(nandani_file)  
print(nandani_mapping)
# print(data)


#Function to extract dictionary from H_wordid-word_mapping.dat
def parser2wordid1(filename):
    with open(filename,"r") as f1: 
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        p2w = {}
        for line in text:
            t = line.lstrip('(H_wordid-word').strip(')').split("\t")
            p2w[int(t[1].lstrip("P"))] = t[2]
    return(p2w)

#Function to extract dictionary from E_wordid-word_mapping.dat
def parser2wordid(filename):
    with open(filename,"r") as f1: 
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        p2w = {}
        for line in text:
            t = line.lstrip('(E_wordid-word').strip(')').split("\t")
            p2w[int(t[1].lstrip("P"))] = t[2]
    return(p2w)
    
p2w = parser2wordid1(filename)
e2w = parser2wordid(efilename)
# print(p2w)
# print(e2w)


# extracting df from BUgol2.1E_2.21_1.csv which contains  old dictionary facts with hindi word is and not parser id   
dfs = pd.read_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_1.csv")

#row index started from 1 instead of 0, which was earlier.
dfs.index = np.arange(1,len(dfs)+1)

# print(dfs.shape)
# r = len(p2w)
# c = dfs.shape[1] - 1
# print(r, c)
# r_list = range(1,r+1)
# c_list =range(1,c+1)
# print(r_list, c_list)

# df = pd.Dataframe(rows=r_list, columns = c_list)
# df = pd.DataFrame(index=r_list, columns = c_list)
# print(df)

#Creation of resources list from 1st column of dataframe
resources = [i.lstrip().rstrip() for i in dfs.iloc[:, 0].tolist()]

#Creation of resources_dict which mapping of alphabets to big names from 1st column of dataframe

letters = [chr(i) for i in range(65, 88)]
resource_dict={}

for k,v in zip(letters,resources):
    resource_dict[k]=v

show_hindi ={}    
for k,v in p2w.items():
    show_hindi[k] = str(k)+"_"+v
    
show_eng ={}    
for k,v in e2w.items():
    show_eng[k] = str(k)+"_"+v
    
# print(show_eng)
# print(show_hindi)

eng = [show_eng[i] for i in sorted(show_eng.keys())]
hin = [show_hindi[i] for i in sorted(show_hindi.keys())]

show_eng[0]='0'
title=show_eng.values()  #.insert(0,'0')


eng, hin
df = pd.DataFrame(index=hin, columns = eng)
df
p2w
e2w
resources
resource_dict
# resource_dict_invert= {v: k for k, v in resource_dict.items()}
# print()
dfs


# In[3]:


import sys, os, pandas as pd, numpy as np
no_of_eng_words = dfs.shape[1]
final_row_in_csv =[]; final_row_in_csv1=[]; allocations=[]
# display(dfs)
for j in range(0,no_of_eng_words):
    hindi_allocations_list=[]
    #for every row extracted all non zero entries and stored in hindi_allocations_list
    hindi_allocations_list = [str(i) for i in dfs.iloc[:,j].tolist() if i!='0' and i!=0]
    #print(j, hindi_allocations_list)
    
    #For an empty hindi_allocations_list i.e verical column equivalent to 1 eng id appended '0' entry in it.
    if not hindi_allocations_list:
        hindi_allocations_list.append('0')
    #print(j, hindi_allocations_list)
    
    #hindi_allocations string contains all entries in vertical column with "#" seperator.
    hindi_allocations = "#".join([str(i) for i in hindi_allocations_list])
        
#     if j==0:
#         hindi_allocations = "all"
    final_row_in_csv.append(hindi_allocations)

final_row_in_csv[0]="Sum of all Resource Suggestions with duplicates"

anchor1=[]; anchor1_str_list=[]; count_dict_list=[]
for j in range(0,no_of_eng_words):
    temp=[];temp1=[]; temp_count_dict={}

#     print(final_row_in_csv[j])
#     print(re.split('#|/',final_row_in_csv[j]))

    temp = re.split('#|/',final_row_in_csv[j])
#     print(temp)
    temp1 = list(dict.fromkeys(re.split('#|/',final_row_in_csv[j])))
#     print(temp1)
#     print([temp.count(x) for x in temp1])
    count_info = [temp.count(x) for x in temp1]

    for i in range(len(temp1)):
        temp_count_dict[temp1[i]] = count_info[i]
    
    count_dict_list.append(temp_count_dict)
#     print(temp_count_dict)
    anchor1.append(temp1)
    anchor1_str_list.append("#".join(temp1))
    
    
anchor1[0] = 'Sum of all Resource Suggestions without duplicates' 
anchor1_str_list[0] = 'Sum of all Resource Suggestions without duplicates' 
# print(anchor1)
    
dfs.loc[-1] = final_row_in_csv 
dfs.loc[-2] = anchor1_str_list
final_row_in_csv1= anchor1_str_list


# In[4]:



anchor2=[]; anchor2_str_list=[]
for j in range(0,no_of_eng_words):
    if len(anchor1[j]) == 1:
        temp = anchor1[j]
    else:
        temp=['0']
    anchor2.append(temp)
    anchor2_str_list.append("".join(temp))
#     print(anchor1[j],"=>", anchor2[j])

anchor2[0] = 'Hindi sugg. without conflict (cross alignment possibilities)' 
anchor2_str_list[0] = 'Hindi. sug. without conflict entry (cross alig)' 


dfs.loc[-3] = anchor2_str_list
# dfs.loc[-1:]

anchor3_str_list=anchor2_str_list
anchor3_str_list[0]="Unique Hindi sugg. entries"
repetated_entries=[]
for i in range(0, len(anchor2_str_list)):
    
#     print(anchor2_str_list[i], anchor2_str_list.count(anchor2_str_list[i]))
    if anchor2_str_list.count(anchor2_str_list[i]) > 1:
        repetated_entries.append(anchor2_str_list[i])
        anchor3_str_list[i] = '0'
        
#     print(anchor2_str_list[i] , anchor3_str_list)
#     while anchor2_str_list[i] in anchor3_str_list:
#             anchor3_str_list.remove(anchor2_str_list[i])
        

# print(anchor2_str_list)
# print(anchor3_str_list)
# print(repetated_entries)
for j in range(0, len(anchor3_str_list)):
    for i in range(0,len(repetated_entries)):
#         print(repetated_entries[i])
        if repetated_entries != '0':
            if repetated_entries[i] == anchor3_str_list[j]:
                anchor3_str_list[j] = '0'
          

# print(anchor3_str_list)
dfs.loc[-4] = anchor3_str_list
# dfs


# In[5]:


# print(nandani_mapping)
nandani_mapping_list=[]; 
for j in range(0,no_of_eng_words):
    if str(j) in nandani_mapping.keys():
#         print(str(j), transliterate_mapping[str(j)])
        nandani_mapping_list.append(nandani_mapping[str(j)])
    else:
#         print(str(j), '0')
        nandani_mapping_list.append('0')
    
    #This is temp module which has nandani's eng_multi to hindi_multi mapping
    #Eg. {'10 11': '3 4'} for group of 10 and 11 hindi has 3 and 4.
    #TODO FUTYRE: We need to add one more layer showing grouping information 
    for every_entry in nandani_mapping.keys():
        if " " in every_entry:
            eng_group_list = every_entry.split(" ")
            hindi_group_list = nandani_mapping[every_entry].split(" ")
#             print(eng_group_list, hindi_group_list)
            
            #Till now nandani's entries are of same length
            for i in range(0, len(eng_group_list)):
                nandani_mapping[eng_group_list[i]]= hindi_group_list[i]
#             print("Multiword entry in nandani dictionary")

# print(nandani_mapping)

nandani_mapping_list[0] = 'Nandani dict'
dfs.loc[-5] = nandani_mapping_list


try:
    
    ## print(transliterate_mapping)
    roja_transliterate_list=[]; 
    for j in range(0,no_of_eng_words):
        if str(j) in transliterate_mapping.keys():
    #         print(str(j), transliterate_mapping[str(j)])
            roja_transliterate_list.append(transliterate_mapping[str(j)])
        else:
    #         print(str(j), '0')
            roja_transliterate_list.append('0')
    roja_transliterate_list[0] = 'Roja Transliterate'
    # print(roja_transliterate_list)   
    dfs.loc[-6] = roja_transliterate_list
except:
    print("FILE MISSING: " + roja_transliterate_file )

# try:
all_entries=[]; anchor=roja_transliterate_list
# print("------", anchor)

# for i in range(0, no_of_eng_words):
# #     all_entries.append([roja_transliterate_list[i], nandani_mapping_list[i],anchor3_str_list[i]])
#     all_entries.append([roja_transliterate_list[i], anchor3_str_list[i]])

# #     print(all_entries[i])
#     count_zeroes = all_entries[i].count('0')
#     if count_zeroes == 3:
#         anchor[i]='0'
#     elif count_zeroes == 0:
#         anchor[i] == 'final anchor'

#     elif count_zeroes == 2:
# #         if all_entries[0]!= '0' or all_entries[0]!=0:
# #             new_entry = all_entries[0]
        
#         new_entry = [z for z in all_entries[i] if z!='0' ]
# #         for item in all_entries[i]:
# #             if item !='0' or item!=0:
# #                 new=item
# #                 break
# #             print(all_entries[i] ,"=>", new)
#         anchor[i]= new_entry[0]
        
#     elif count_zeroes ==1:
# #         print("two non zero")
#         print(all_entries[i])

        
# #         if all_entries[i][0]!= 'Roja Transliterate' and all_entries[i][1]!= 'Nandani dict' and all_entries[i][2]!= 'Unique Hindi sugg. entries':
            
#         if (all_entries[i][0]!='0' or 0) and (all_entries[i][1]!='0' or 0) and (all_entries[i][2]=='0' or 0) :
#             print("1st to roja")
#             anchor[i] = all_entries[i][0]

#         elif all_entries[i][0]!='0' or 0 and all_entries[i][1]=='0' or 0 and all_entries[i][2]!='0' or 0:
#             print("1st to roja")
#             anchor[i] = all_entries[i][0]

#         elif all_entries[i][0]=='0' and all_entries[i][1]!='0'and all_entries[i][2]!='0' or 0:
#             print("nandani")
#             anchor[i]= all_entries[i][1]
#     print(all_entries[i], anchor[i])   
        
# #     print(count_zeroes)
# #     print(anchor[i])
# anchor[0]='final anchor'
# print("PPPPP",anchor)
# dfs.loc[-7] = anchor
# dfs


# In[34]:


dfs1 = pd.DataFrame(dfs.iloc[-7:,:])
# print(dfs1.columns.tolist())
# print(title)
dfs1.columns = title
# print(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_2.csv")
dfs.to_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_2.csv", index=False)
# display(dfs1)
# show_hindi

# display(dfs)

new_dfs = dfs.iloc[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,-1,-2,-3]]
# new_dfs.columns = title
unique = new_dfs.iloc[-1].to_list()
nandani = new_dfs.iloc[-2].to_list()
roja = new_dfs.iloc[-3].to_list()


show_hindi[0]='0'

unique_words = []
for i in range(0,len(unique)):
    temp=[]
    if i== 0:
        unique_words.append(unique[i])
    if i > 0:
        check_multiple = unique[i].split(" ")
        if len(check_multiple) == 1:
            temp.append(show_hindi[int(unique[i])])
        else:
#         if len(check_multiple) > 1:
            for item in check_multiple:
                temp.append(show_hindi[int(item)])
#         print(temp)
        unique_words.append(" ".join(temp))
print(unique_words) 

# print(nandani)
nandani_words = []
for i in range(0,len(nandani)):
    temp=[]
    if i== 0:
        nandani_words.append(nandani[i])
    if i > 0:
        check_multiple = nandani[i].split(" ")
        if len(check_multiple) == 1:
            temp.append(show_hindi[int(nandani[i])])
        else:
#         if len(check_multiple) > 1:
            for item in check_multiple:
                temp.append(show_hindi[int(item)])
#         print(temp)
        nandani_words.append(" ".join(temp))
print(nandani_words) 
            
roja_words = []
for i in range(0,len(roja)):
    temp=[]
    if i== 0:
        roja_words.append(roja[i])
    if i > 0:
        check_multiple = roja[i].split(" ")
        if len(check_multiple) == 1:
            temp.append(show_hindi[int(roja[i])])
        else:
#         if len(check_multiple) > 1:
            for item in check_multiple:
                temp.append(show_hindi[int(item)])
#         print(temp)
        roja_words.append(" ".join(temp))
print(roja_words)


new_dfs_word = new_dfs[0:23]
new_dfs_word.columns = title
# print(len(unique_words))

new_dfs_word.loc[-1] = roja_words
new_dfs_word.loc[-2] = nandani_words
new_dfs_word.loc[-3] = unique_words
new_dfs_word

new_dfs_word.to_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_3.csv", index=False)
new_dfs_word.to_html(path_tmp + '/' + eng_file_name + "_" + sent_no + "_3.html")

short_new_dfs_word = new_dfs_word[-3:]
short_new_dfs_word.to_html(path_tmp + '/' + eng_file_name + "_" + sent_no + "_short.html")
print(path_tmp + '/' + eng_file_name + "_" + sent_no + "_short.html  created")
