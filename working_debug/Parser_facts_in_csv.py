#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %%HTML
# <style type="text/css">
# table.dataframe td, table.dataframe th {
#     border: 1px  black solid !important;
#   color: black !important;
# }
# </style>


# In[2]:


#$$$ 1 Input file names and imports
import subprocess
from bs4 import BeautifulSoup,sys,os, re
import pandas as pd
import numpy as np
pd.options.display.max_columns = None
import csv
import H_Modules


#Specify path of sentence:
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
# tmp_path='/home/kishori/a/tmp_anu_dir/tmp/BUgol_27_aug/'
# eng_file_name = 'cc_conjE'

# eng_file_name = 'E'
# sent_no = '2.14' #2.29, 2.21, 2.61, 2.14, 2.64

eng_file_name = sys.argv[1]
sent_no = sys.argv[2]

path_tmp= tmp_path + eng_file_name + "_tmp/" + sent_no
sent_dir =  tmp_path + eng_file_name + "_tmp/"
#------------------------------------------------------------------------------------
hfilename = path_tmp +  '/H_wordid-word_mapping.dat'
efilename = path_tmp + '/E_wordid-word_mapping.dat'
efilename_alternate = path_tmp + '/word.dat'

hparserid_to_wid = path_tmp + '/H_parserid-wordid_mapping.dat'
nandani_file = path_tmp +  '/corpus_specific_dic_facts_for_one_sent.dat'
roja_transliterate_file = path_tmp +  '/Roja_chk_transliterated_words.dat'
# roja_transliterate_file = path_tmp +  '/results_of_transliteration.dat'
html_file = path_tmp +'/'+ eng_file_name +'_table1.html'
log_file = path_tmp + '/log_htmltocsv'

e_group_html = path_tmp + '/E_group_HTML.txt'
h_group_html = path_tmp + '/H_group_HTML.txt'



es=open(path_tmp+ '/E_sentence').read()
hs=open(path_tmp + '/H_sentence').read()
hs = H_Modules.wx_utf_converter_sentence(hs)

print(hs)

print(path_tmp)
# himg = path_tmp+'/H_tree_final.png'
himg = 'H_tree_final.png'
eimg = 'E_tree_final.png'

himg1 = 'H_tree_initial.png'
eimg1 = 'E_tree_initial.png'

himg2 = 'H_tree_corrected.png'
eimg2 = 'E_tree_corrected.png'


if os.path.exists(log_file):
    os.remove(log_file)
log = open(log_file,'a')

#------------------------------------------------------------------------------------


# In[3]:


#$$$ 2 func is to replace manju mam id's to word ids of hindi assigned words below every eng wordid
def func(x):
    col = x.tolist()
    new_col=[];all_series=[];final_cell_value=""
    #if(str('   anu_exact_match  ', 'utf-8')) in col:
    #if unicode('   anu_exact_match  ') in col:
    if '   anu_exact_match  ' in col:
        new_col =[str(i) for i in col]
    else:
        for count, i in enumerate(col,0):
            if(i!= ' .'):
                change = i.lstrip().rstrip()
                if '/' in change:
                    possibilities = [str(i.lstrip().rstrip()) for i in change.split("/")]
                    new2=[]
                    for poss in possibilities:
                        if '+' in poss:
                            g = poss.split('+')
                            new1=[]
                            for one in g:
#                                 print("((one))",one, type(one))
                                new1.append(p2w[int(one)])
                            final_cell_value1 = " ".join(new1)
                            new2.append(final_cell_value1)
                        else:
#                             print("***poss", poss, type(poss))
                            final_cell_value2 = p2w[int(poss)]
                            new2.append(final_cell_value2)
                    final_cell_value = "/".join(new2)
                    new_col.append(final_cell_value)
                    
                elif '+' in change:
                    grouping = [str(i.lstrip().rstrip()) for i in change.split("+")]
                    new=[]
#                     print(p2w)
                    for g in grouping:
#                         print(g)
                        new.append(p2w[int(g)])
                    final_cell_value = " ".join(new)
                    new_col.append(final_cell_value)
                else:
                    final_cell_value = p2w[int(change)]
                    new_col.append(final_cell_value)
            else:
                final_cell_value = '0'
                new_col.append(final_cell_value)
    new_col.append(final_cell_value)
    new_col = new_col[:-1]
    new_x = pd.Series(new_col)
#     print(new_x)
    return(new_x)


# In[ ]:





# In[4]:


#$$$ 3
#Function to extract dictionary from H_wordid-word_mapping.dat
def create_dict(filename,string):
    with open(filename,"r") as f1: 
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        p2w = {}
        for line in text:
            t = line.lstrip(string).strip(')').split("\t")
            p2w[int(t[1].lstrip("P"))] = t[2]
    return(p2w)


#Extract nandani_mapping dictionary[eids to hids] from corpus_specific_dic_facts_for_one_sent.dat
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

#given a value returns corresponding key from a dictionary
def return_key_from_value(dictionary, value):
    key =[ k for k,v in dictionary.items() if v == value]
    return (key[0])


# In[5]:


#$$$ 4

#Functions for anchor calculations:

#Function used in visualization
def replace_id_by_id_word_pair_for_visualization(unique):
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
    return(unique_words) 


# In[6]:


#$$$ 5

##CREATION OF PYTHON DICTS and LISTS FROM NECESSARY FILES, csv,sys,os
try:   
    h2w = create_dict(hfilename, '(H_wordid-word')
    hdf=pd.DataFrame(list(h2w.values()), index=h2w.keys())

#     print(h2w)
    show_hindi ={}    
    for k,v in h2w.items():
        show_hindi[k] = str(k)+"_"+v
#     print(show_hindi)
    hin = [show_hindi[i] for i in sorted(show_hindi.keys())]
    hindi_word = list(show_hindi.values())
    hindi_row = "  ,  ".join(hindi_word)

except:
    print("FILE MISSING: " + hfilename )
    log.write("FILE MISSING: " + hfilename + "\n")
    
#-----------------------------------------------------------------------------------------
try:
    p2w = create_dict(hparserid_to_wid, '(H_parserid-wordid')
except:
    print("*FILE MISSING: " + hparserid_to_wid)
    log.write("FILE MISSING: " + hparserid_to_wid+ "\n")
try:
    html = open(html_file).read()
    soup = BeautifulSoup(html, "lxml")
    table = soup.find('table')
    table_rows = table.find_all('tr')
    l=[]
#     print(table_rows)
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td] 
        l.append(row)
    df = pd.DataFrame(l)
    final = df[9:-1].drop(df.columns[[-1]], axis=1)
    final=final[0:23]
    final.to_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + ".csv", index=False)
    
except:
    print("FILE MISSING: " + html_file)
    log.write("FILE MISSING: " + html_file+ "\n")
    
#     
try:
    new = final.apply(func)
#     print(new)
#     if new==0:
#         break
#     print("************",new)
    new.to_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_1.csv", index=False)
except :
    print("Discrepance in hindi manju id, parser id and word id")
    log.write("Discrepance in hindi manju id, parser id and word id" + "\n")
    log.close()
    sys.exit()
    
    
# if new=='exit':
#     sys.exit()
# else:
    
#------------------------------------------------------------------------------------
try:
#     print(nandani_file)
    data="";
    nandani_mapping = extract_dictionary_from_deftemplate(nandani_file)  
#     print(nandani_mapping)
except:
    print("FILE MISSING: " + nandani_file )
    log.write("FILE MISSING: " + nandani_file + "\n")

#------------------------------------------------------------------------------------

try:
    # extracting df from BUgol2.1E_2.21_1.csv which contains  old dictionary facts with hindi word is and not parser id   
    dfs = pd.read_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_1.csv")
    #row index started from 1 instead of 0, which was earlier.
    dfs.index = np.arange(1,len(dfs)+1)
    # print(dfs.shape)
    # r = len(h2w)
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
    # display(dfs)
    # resource_dict_invert= {v: k for k, v in resource_dict.items()}
    no_of_eng_words = dfs.shape[1]

except:
    print("FILE MISSING: " + path_tmp +'/'+ eng_file_name + "_"+sent_no + "_1.csv" )
    log.write("FILE MISSING: " + path_tmp +'/'+ eng_file_name + "_"+sent_no + "_1.csv" + "\n")

#------------------------------------------------------------------------------------
try:
    e2w = create_dict(efilename, '(E_wordid-word')
    edf=pd.DataFrame(list(e2w.values()), index=e2w.keys())

    #     print(e2w)
    show_eng ={}    
    for k,v in e2w.items():
        show_eng[k] = str(k)+"_"+v
    #     print(show_eng)
    eng = [show_eng[i] for i in sorted(show_eng.keys())]
#     print(show_eng.values(), type(show_eng.values()))
    title=["Resources"]+list(show_eng.values())#.insert(0,'0')

        
except:
    print("FILE MISSING: " + efilename )
    log.write("FILE MISSING: " + efilename+ "\n")
    command = "awk '{printf $3}' "+ efilename_alternate
    print(command)
    x=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True).stdout.read()
#     x1 = x.decode(encoding="utf-8", errors="strict")
    x1=x.decode("utf-8") 
    x2 = x1.split(")")
    while "" in x2:
        x2.remove("")
    print(x2, len(x2), type(x2))
    title=["Resources"] + list(x2[:-1])
    print(type(title))
    print(title, len(title), no_of_eng_words)
    print(dfs.shape)
#     print("===>",x,"\n", str(x))    

#created for extracting eid-hid pair corresponding to eword-hword pair of roja_chk_transliteration_out
def get_E_H_dict_Ids(filename):
    tmp={}
    with open(filename,'r') as f:
#         print(f.read())
#         print("====")
#         print(f.read().strip("\n").split("\n"))
        entries=f.read().strip("\n").split("\n")
        entries = [item.rstrip(")") for item in entries]
#         print("=>",entries)

#         print(h2w)
        for entry in entries:
#             print(entry)
            eword = entry.split("\t")[1]
            hword = entry.split("\t")[2]
#             print(eword, hword)
            eid = return_key_from_value(e2w, eword)
            hid = return_key_from_value(h2w, hword)
#             print(eid, hid)
            tmp[str(eid)] = str(hid)
        print(tmp)
    return(tmp)    

#------------------------------------------------------------------------------------



# try:
#     tranliterate_dict={}
#     transliterate_mapping = get_E_H_dict_Ids(roja_transliterate_file)  
# except:
#     print("FILE MISSING: " + roja_transliterate_file )
#     log.write("FILE MISSING: " + roja_transliterate_file + "\n")

# display(dfs)

# dictionary_wordnet = list(dfs.iloc[5])
hindi_wordnet = list(dfs.iloc[8])
partial_match = list(dfs.iloc[12])

# dfs.drop(6, inplace=True)
dfs.drop(9, inplace=True)
dfs.drop(13, inplace=True)

# print(hindi_wordnet)
# print(partial_match)

# print(dictionary_wordnet)
# print(hindi_wordnet)
# print(partial_match)

org_col = list(dfs.columns)
new_col = org_col
new_col[0]="Resources"
dfs.columns=new_col

# print(h2w)
# print(e2w)


# print(show_eng)
# print(show_hindi)
dfs
#CHANGE
# display(edf.T)
# display(hdf.T)


# In[7]:


#Code to create Debug files for various layers:

def id_to_IDSTR_on_string(i):
    if(i!= '0' and i!=0):  #code for those cell values which are neither '0' nor 0.
        i=str(i)           #changed all int to string
        change = i.lstrip().rstrip()
#                 print("===>", change) 
        pchange1 = change.replace('#', ' # ')
    
        pchange = pchange1.replace('/', ' / ')
#                 print(pchange)
        pchange_list = pchange.split()
#                 print(pchange_list)
        change1=[]
        for item in pchange_list:
            if item=='#' :  #dont replace # and / with any word.
                change1.append('#')
            elif item =='/':
                change1.append('/')
            else:
                if int(item) in show_hindi.keys():  # dict keys are int so typecasting item to int
                    change1.append(show_hindi[int(item)])  #here too typecasting needed
                         
#                 print(change1)
        final_cell_value=" ".join(change1)
#         new_col.append(final_cell_value)
                
    else:
        final_cell_value = '0'           #converted all int 0 to '0'
#         new_col.append(final_cell_value)
    return(final_cell_value)
    
def create_debug_file_for_layer(x, filename):
    with open(sent_dir + "/"+filename, "a") as f:
        print(sent_no)
        f.write(" ".join([sent_no,":\n"]))
        for i in range(0, no_of_eng_words):
            if i!=0:
                if x[i]!='0' and x[i]!=0:
#                     print( title[i], "==>", id_to_IDSTR_on_string(x[i]))
                    f.write(" ".join([title[i], "==>", id_to_IDSTR_on_string(x[i]),"\n"]))
        f.write("===============\n")
#         print("======")

# create_debug_file_for_layer(dictionary_wordnet,"dictionary_match_debug.txt")
# create_debug_file_for_layer(hindi_wordnet,"hindi_wordnet_debug.txt")
# create_debug_file_for_layer(partial_match,"partial_match_debug.txt")


# In[8]:


#$$$ 6
#Roja K layer partial match

def cleaning_list(k_layer_ids):
    for n, i in enumerate(k_layer_ids):
        if i == '-':
            k_layer_ids[n] = 0
#     for n, i in enumerate(k_layer_ids):
#         if i == '_':
#             k_layer_ids[n] = 0
    return(k_layer_ids)

def load_row_from_csv(filename, row_number):
    try:
        with open(filename, newline='') as iris:
            # returning from 2nd row
            return list(csv.reader(iris, delimiter=','))[row_number]
    except FileNotFoundError as e:
        raise e


k_layer_ids_file= path_tmp + '/H_alignment_parserid.csv'

k_layer_ids= load_row_from_csv(k_layer_ids_file, 1)
k_layer_ids = cleaning_list(k_layer_ids)
k_layer_ids[0]= "K_exact_match(Roja)"
print(k_layer_ids)

k_layer_partial_ids= load_row_from_csv(k_layer_ids_file, 2)
k_layer_partial_ids = cleaning_list(k_layer_partial_ids)
k_layer_partial_ids[0]="K_partial_Content_word(Roja)"
print(k_layer_partial_ids)

k_layer_root_ids= load_row_from_csv(k_layer_ids_file, 3)
k_layer_root_ids = cleaning_list(k_layer_root_ids)
k_layer_root_ids[0]="K_root_info(Roja)"
print(k_layer_root_ids)

# dfs.loc[24] = k_layer_ids
dfs.loc[dfs.index[-1]+1] = k_layer_ids
# dfs.loc[25] = k_layer_partial_ids
dfs.loc[dfs.index[-1]+1] =k_layer_partial_ids
dfs.loc[dfs.index[-1]+1] =k_layer_root_ids

# try:
    
# k_layer_ids_file= path_tmp + '/H_alignment_parserid.csv'
# with open(k_layer_ids_file, 'r') as f:
#     print("ppp")
#     print(f.read().split("\n")[2].strip("\r").split(","))
#     k_layer_ids = f.read().split("\n")[2].strip("\r").split(",")
    
#     k_layer_partial_ids = f.read().split("\n")[2].strip("\r").split(",")
#     print(k_layer_ids)

#     k_layer_ids = cleaning_list(k_layer_ids)
# #     k_layer_partial_ids = cleaning_list(k_layer_partial_ids)

#     print(k_layer_ids, len(k_layer_ids), no_of_eng_words)

# dfs.loc[24] = k_layer_ids

# dfs
# except:
#     print("FILE MISSING: " + k_layer_ids_file )
#     log.write("FILE MISSING: " + k_layer_ids_file + "\n")
# print(show_hindi)
# print(show_engg)

dfs


# In[9]:


# #remove=========================
# #10 11 12 => [10, 11, 12]
def create_list_from_space_seperated_string(string):
    if " " not in string:
        return([string])
    return(string.split(" "))

# # returns a non-empty list when there is some intersection between 2 elements 
# #[[10,11,12], [12]] => [12]
def intersection_of_two_list(lst1, lst2): 
    common_element = [value for value in lst1 if value in lst2] 
    return common_element 

# #[[1,2],[11,12],[1],[2]] => [[1],[2],[1,2],[11,12]]
def sort_list_of_list_by_length(listlist):
    tuple_list=[]
    for item in listlist:
        tuple_list.append((len(item),item))
    x = sorted(tuple_list, key=lambda x: x[0])
    final = [i[1] for i in x ]
    return(final)
    
# print(intersection_of_two_list([10,11,12], [12]))
# print(create_list_from_space_seperated_string('10 11 12'))
# #10 11 12#12 => 10 11 12
def merge_overlapping_entries(anchor1):
    print("***")
    print(len(anchor1))
#     print(anchor1)
    for i in range(1, len(anchor1)): #excluding 0th index of anchor1 which is label of row [row index]
        if len(anchor1[i])>1:
#             print(anchor1[i])
            all_list_in_cell=[]
            for item in anchor1[i]:
                all_list_in_cell.append(create_list_from_space_seperated_string(item))
            ordered_listOflist = sort_list_of_list_by_length(all_list_in_cell)
            print("=>", ordered_listOflist)
    
    
            
#     return(anchor1)
    
# print(show_hindi)
# # #remove=========================
# merge_overlapping_entries(anchor1)


def remove_single_hindi_id_in_more_than_one_column(anchor2_str_list):
    print("$$$",anchor2_str_list)
    anchor3_str_list=anchor2_str_list
    
    repetated_entries=[]
    for i in range(0, len(anchor2_str_list)):
    
#     print(anchor2_str_list[i], anchor2_str_list.count(anchor2_str_list[i]))
        if anchor2_str_list.count(anchor2_str_list[i]) > 1:
            repetated_entries.append(anchor2_str_list[i])
            anchor3_str_list[i] = '0'
#     print(anchor2_str_list)
#     print(anchor3_str_list)
#     print(repetated_entries)
    for j in range(0, len(anchor3_str_list)):
        for i in range(0,len(repetated_entries)):
#         print(repetated_entries[i])
            if repetated_entries != '0':
                if repetated_entries[i] == anchor3_str_list[j]:
                    anchor3_str_list[j] = '0'
    return(anchor3_str_list)


def remove_multi_entry_in_a_cell(anchor1):
    print("))))", anchor1)
    anchor2=[]; anchor2_str_list=[]
    print(no_of_eng_words)
    dict1 = {} 
  
    for i in anchor1[1:]:
        for j in i:
            if j not in dict1.keys():
                dict1[j]=1
            else:
                dict1[j]+=1  
#     print(dict1)
    
    
    for j in range(0,no_of_eng_words):
        if len(anchor1[j]) == 1 and dict1[anchor1[j][0]]==1:
            temp = anchor1[j]
        elif  len(anchor1[j]) == 1 and anchor1[j][0]=='0':
            temp = anchor1[j]
        else:
            temp=['0']
        anchor2.append(temp)
        anchor2_str_list.append("".join(temp))
#         print(anchor1[j],"=>", anchor2[j])
#     print(anchor1, len(anchor1))
#     print(anchor2, len(anchor2))
    return(anchor2, anchor2_str_list)

# resource_list = list(dfs['Resources'])
# eng_id_list = list(dfs['13'])
# print(len(resource_list), len(eng_id_list))
# for i,item in enumerate([resource_list,eng_id_list],1):
#     print(eng_id_list[i])
# dfs


# In[10]:


#$$$ 8
#extracting Roja and Nandani Dictionary values and inserting in csv
try:
    tranliterate_dict={}
    transliterate_mapping = get_E_H_dict_Ids(roja_transliterate_file)  
    print(transliterate_mapping)
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
#     dfs.loc[28] = roja_transliterate_list
    dfs.loc[dfs.index[-1]+1] = roja_transliterate_list
except:
    print("FILE MISSING: " + roja_transliterate_file )
    log.write("FILE MISSING: " + roja_transliterate_file  + "\n")


try:
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
#     dfs.loc[29] = nandani_mapping_list
    dfs.loc[dfs.index[-1]+1]=nandani_mapping_list
except:
    print("FILE MISSING: " + nandani_file ) 
    log.write("FILE MISSING: " + nandani_file  + "\n")
dfs


# In[11]:


#Integrating technical dictionary

#Correctness of range
def check_multi_or_single_word_equivalence(l):
    if len(l) == len(set(l)):
        return(l)
    else:
        return(l[0])

#created for extracting eid-hid pair corresponding to eword-hword pair of roja_chk_transliteration_out
def get_E_H_dict_Ids_mfs(filename):
    tmp={}
    with open(filename,'r') as f:
        entries=f.read().strip("\n").split("\n")
        entries = [item.rstrip(")") for item in entries]
        for entry in entries:
            print(entry)
            entry  = entry.lstrip("(E_word-mfs-H_word	")
            new_entry = entry.split("\tmfs\t")
#             print(new_entry)
            ewords = new_entry[0]
            hwords = new_entry[1]
            if " " in ewords or " " in hwords:
                print("multi-equivalence")
                if " " in ewords:
                    x=ewords.split(" ")[0]
                    eng_multiword_len = len(ewords.split(" "))
                else:
                    x=ewords
                    eng_multiword_len = 0
                if " " in hwords: 
                    y=hwords.split(" ")[0]
                    hin_multiword_len = len(hwords.split(" "))
                else:
                    y=hwords
                    hin_multiword_len = 0
#                 print(x,y)
                eid = return_key_from_value(e2w, x)
                hid = return_key_from_value(h2w, y)
                final_eids = check_multi_or_single_word_equivalence([eid, eid+eng_multiword_len-1])
                final_hids = check_multi_or_single_word_equivalence([hid, hid+hin_multiword_len-1])
#                 print([eid, eid + eng_multiword_len], [hid, hid + eng_multiword_len])
                print(final_eids,final_hids)
#                 print(check_multi_or_single_word_equivalence([2,4]))
#                 print(type(check_multi_or_single_word_equivalence([2,4])))

                     
                # Tilda logic
#                 if type(final_hids)==list:
#                     print("list it is!")
#                     final_hids_str = " ".join([str(i) for i in final_hids])
#                 else:
#                     final_hids_str = str(y)
#                 tmp[final_eids[-1]] = final_hids_str
#                 for i in final_eids[:-1]:
#                     tmp[i]='~'
# #                     print(i)

                head_in_english = final_eids[-1]  #This will change once we will get head id infrmation from english group.
                hindi_group = " ".join([str(i) for i in final_hids])
                tuple_list=[]
#                 for i in final_eids:
#                     if i==0:
#                         tuple_list
                        
#                 eids= [6,7,8]
#                 hindi_group = '3 4'
#                 tmp[final_eids[0]] = '('
#                 tmp[final_eids[-1]] =')'
                tmp[head_in_english] = hindi_group
#                 print(tmp.keys())
#                 print(tmp)
                if head_in_english in tmp:
#                     print("====>",head_in_english
                    tmp[head_in_english] = hindi_group
                    
                else:
                    tmp[head_in_english]=hindi_group

            else:
                print("one-to-one entry")
                eid = return_key_from_value(e2w, ewords)
                hid = return_key_from_value(h2w, hwords)
                print(eid, hid)
                final_eids = eid; final_hids = hid           #IMP
                if final_eids not in tmp:
                    tmp[final_eids] = final_hids
#             tmp[str(eid)] = str(hid)
        print(tmp)
    return(tmp)    

try:
    tech_dict_filename = path_tmp + '/Tech_dict_lookup.dat'
    tech_dict_dict = get_E_H_dict_Ids_mfs(tech_dict_filename)
    tech_dict_list=[]
    for j in range(0,no_of_eng_words):
        if j in tech_dict_dict.keys():
            #         print(str(j), transliterate_mapping[str(j)])
            tech_dict_list.append(tech_dict_dict[j])
        else:
            #         print(str(j), '0')
            tech_dict_list.append('0')
    tech_dict_list[0] = 'Bharatwani Dict.'
    # print(roja_transliterate_list)   
    #     dfs.loc[28] = roja_transliterate_list
    dfs.loc[dfs.index[-1]+1] = tech_dict_list
    dfs
except:
    print("Tech dict not created")

dfs


# In[12]:


#$$$ 7
# display(dfs)
#taking union on repreated entries
resource_list = list(dfs['Resources'])
resource_dict={}
for i, item in enumerate(resource_list):
    resource_dict[i]=item
    
exact_match = ['   anu_exact_match  ', 'K_exact_match(Roja)','Nandani dict', 'Roja Transliterate', 'Bharatwani Dict.','   M_layer_match  ', '   L_layer_match  ']
partial_match_labels = ['   anu_exact_match_without_vib  ', '   anu_root_match_without_vib  ', '   dictionary_match_without_vib  ', '   multi_dictionary_match  ', '   dictionary_match  ', '   multi_hindi_wordnet_match  ', '   anu_root_match  ', '   kriyA_mUla_partial_match  ', '   hnd_and_std_rel_match  ', '   hindi_tam_match  ', '   hindi_tam_dic_match  ', '   english_word_match  ', '   transliteration_match  ', '   scope  ', '   manual_scope  ', 
'   M_layer_partial_match  ', '   L_layer_partial_match  ', 'K_partial_Content_word(Roja)', 'K_root_info(Roja)']
guess_match = ['   single_verb_match  ']

# print(resource_dict)
def union_of_columns_verically(dfs):
    final_row_in_csv=[];final_row_in_csv1=[] ;final_row_in_csv2=[]
    for j in range(0,no_of_eng_words):
        hindi_allocations_list=[];hindi_allocations_list1=[];hindi_allocations_list2=[]
        #for every row extracted all non zero entries and stored in hindi_allocations_list
#         hindi_allocations_list = [str(i) for i in dfs.iloc[:,j].tolist() if i!='0' and i!=0]
#         for i in dfs.iloc[:,j].tolist(): #j is column index, we are applying function on every column
#             if i!='0' and i!=0:
#                 print(i)
#                 hindi_allocations_list.append(str(i))
#         print("hindi id suggestions for eng id",j,dfs.iloc[:,j].tolist())
        for index, item in enumerate(dfs.iloc[:,j].tolist()):
#             print(index,item, type(item))
            if item!='0' and item!=0:
#                 print(index, item)
# #                hindi_allocations_list.append((str(item), resource_dict[index]))

                if resource_dict[index] in exact_match:
#                     print(j, index, item)
                    hindi_allocations_list.append(str(item))
#                 else:
#                     hindi_allocations_list.append('0')
#     #                     hindi_allocations_list.append((str(item), resource_dict[index]))
                if resource_dict[index] in partial_match_labels:
#                     print(j, index, item)
                    hindi_allocations_list1.append(str(item))
#                 else:
#                     hindi_allocations_list1.append('0')
                if resource_dict[index] in guess_match:
#                     print(j, index, item)
                    hindi_allocations_list2.append(str(item))
#                 else:
#                     hindi_allocations_list2.append('0')
            else:
                hindi_allocations_list.append('0')
                hindi_allocations_list1.append('0')
                hindi_allocations_list2.append('0')
        hindi_allocations = "#".join([str(i) for i in hindi_allocations_list])
        hindi_allocations1 = "#".join([str(i) for i in hindi_allocations_list1])
        hindi_allocations2 = "#".join([str(i) for i in hindi_allocations_list2])

        final_row_in_csv.append(hindi_allocations)
        final_row_in_csv1.append(hindi_allocations1)
        final_row_in_csv2.append(hindi_allocations2)

#         print(final_row_in_csv)
#         print(final_row_in_csv1)
#         print(final_row_in_csv2)
        
#         #For an empty hindi_allocations_list i.e verical column equivalent to 1 eng id appended '0' entry in it.
#         if not hindi_allocations_list:
#             hindi_allocations_list.append('0')
#         if not hindi_allocations_list1:
#             hindi_allocations_list.append('0')
#         if not hindi_allocations_list2:
#             hindi_allocations_list.append('0')
            
#         #hindi_allocations string contains all entries in vertical column with "#" seperator.
#         hindi_allocations = "#".join([str(i) for i in hindi_allocations_list])
#         hindi_allocations1 = "#".join([str(i) for i in hindi_allocations_list1])
#         hindi_allocations2 = "#".join([str(i) for i in hindi_allocations_list2])
        
#         final_row_in_csv.append(hindi_allocations)
#         final_row_in_csv1.append(hindi_allocations1)
#         final_row_in_csv2.append(hindi_allocations2)

#     #     print(final_row_in_csv[1:])
    return([final_row_in_csv,final_row_in_csv1 ,final_row_in_csv2])



# Calling function for Union of columns and removing duplicates:
# print("====finalrow_in_csv")
final_row_in_csv,final_row_in_csv1 ,final_row_in_csv2 = union_of_columns_verically(dfs)
# union_of_columns_verically(dfs)
# final_row_in_csv[0]="Verical Union exact"
# final_row_in_csv1[0]="Verical Union partial"
# final_row_in_csv2[0]="Verical Union guess"

print(final_row_in_csv)
print(len(final_row_in_csv))
print(final_row_in_csv1)
print(len(final_row_in_csv1))

print(final_row_in_csv2)
print(len(final_row_in_csv2))


# In[14]:


def remove_duplicates_from_union(final_row_in_csv):
#     print(final_row_in_csv)
    anchor1=[]; anchor1_str_list=[]; count_dict_list=[]
    for j in range(0,no_of_eng_words):
        temp=[];temp1=[]; temp_count_dict={}
        temp = re.split('#|/',final_row_in_csv[j])
        temp1 = list(dict.fromkeys(re.split('#|/',final_row_in_csv[j])))
#         print(j,temp1)
        count_info = [temp.count(x) for x in temp1]
        for i in range(len(temp1)):
            temp_count_dict[temp1[i]] = count_info[i]
    
        count_dict_list.append(temp_count_dict)
        if len(temp1) > 1:
            while '0' in temp1:
                temp1.remove('0')
        anchor1.append(temp1)
        anchor1_str_list.append("#".join(temp1)) 
#     print(anchor1)
    return(anchor1, anchor1_str_list, count_dict_list)


print("====anchor1")
anchor1, anchor1_str_list, count_dict_list = remove_duplicates_from_union(final_row_in_csv)
anchor1[0] = 'Potential anchors (exact)' 
anchor1_str_list[0] = 'Potential anchors (exact)' 
print(anchor1_str_list)

anchor2, anchor2_str_list = remove_multi_entry_in_a_cell(anchor1)
anchor2_str_list[0]="Starting anchor"
anchor3_str_list = remove_single_hindi_id_in_more_than_one_column(anchor2_str_list)
anchor3_str_list[0]="Starting anchor"
print(anchor3_str_list)


anchor1_partial, anchor1_str_list_partial, count_dict_list_partial = remove_duplicates_from_union(final_row_in_csv1)
anchor1_partial[0] = 'Potential anchors (partial)' 
anchor1_str_list_partial[0] = 'Potential anchors (partial)' 
print(anchor1_str_list_partial)


anchor1_guess, anchor1_str_list_guess, count_dict_list_guess = remove_duplicates_from_union(final_row_in_csv2)
anchor1_guess[0] = 'Potential anchors (guess)' 
anchor1_str_list_guess[0] = 'Potential anchors (guess)' 
print(anchor1_str_list_guess)

dfs.loc[dfs.index[-1]+1]=anchor1_str_list
dfs.loc[dfs.index[-1]+1]=anchor3_str_list
dfs.loc[dfs.index[-1]+1]=anchor1_str_list_partial
dfs.loc[dfs.index[-1]+1]=anchor1_str_list_guess

# #Extra layers which are not considered in csv now, but might be considered in future

dfs.loc[dfs.index[-1]+1] = hindi_wordnet
dfs.loc[dfs.index[-1]+1] = partial_match

dfs


# In[14]:


# #$$$ 9

# #Creation of anchor version 2 from anchor version1 + Roja n Nandani dictionary module
# # This contains:
# #     union_of_columns_verically(dataframe)
# #     remove_duplicates_from_union(final_row_in_dataframe)
# #     remove_multi_entry_in_a_cell(changed_final_row_in_dataframe)

# final_row_in_csv = union_of_columns_verically(dfs)
# final_row_in_csv[0]="Verical Union v2"
# print(final_row_in_csv)
# anchor1, anchor1_str_list, count_dict_list = remove_duplicates_from_union(final_row_in_csv)
# anchor1[0] = 'Potential anchors v2' 
# anchor1_str_list[0] = 'Potential anchors v2' 
# print(anchor1_str_list)
# anchor2, anchor2_str_list = remove_multi_entry_in_a_cell(anchor1)
# print(anchor2_str_list)
# anchor3_str_list = remove_single_hindi_id_in_more_than_one_column(anchor2_str_list)
# anchor3_str_list[0]="Starting anchor v2"
# print(anchor3_str_list)
# # print(dfs.index[-1]+1)

# # dfs.loc[30] = anchor1_str_list
# dfs.loc[dfs.index[-1]+1] = anchor1_str_list
# # dfs.loc[31] = anchor3_str_list
# dfs.loc[dfs.index[-1]+1] =anchor3_str_list


# In[15]:


# #Prashant's and Apratim's module
# try:
#     prashant_csv = path_tmp + '/new_N1.csv'
#     # print(open(prashant_csv,'r').read())
#     N1_layer= load_row_from_csv(prashant_csv, 1)
#     print(N1_layer)
#     N1_layer.insert(0,"N1_layer")
#     # print(N1_layer)
#     print(N1_layer)
#     dfs.loc[dfs.index[-1]+1] = N1_layer
#     dfs
# except:
#     print("new_N1.csv not found")
#     log.write("FILE MISSING: " + prashant_csv  + "\n")
#     log.close()


# In[14]:




dfs.to_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_2.csv", index=False)
dfs.to_html(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_2.html", index=False)

#Extract row of dataframe based on cell value in a column
def extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,col_name, cell_vale):
    x = dfs.loc[dfs[col_name] == cell_vale]
    y=x.values.tolist()[0]
    return(y)

potential_anchor = extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,'Resources','Potential anchors (exact)')
starting_anchor = extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,'Resources','Starting anchor')
potential_anchor_partial = extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,'Resources','Potential anchors (partial)')
potential_anchor_guess = extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,'Resources','Potential anchors (guess)')


print(starting_anchor)
print(potential_anchor)
print(potential_anchor_partial)
print(potential_anchor_guess)

start_dict ={}
for i,val in enumerate(title,0):
    start_dict[i] = starting_anchor[i]
# print(start_v2_dict)
# #display(dfs)
# new


# In[17]:


#Changes every cell value[hindi ids] from id to is_word pair
def id_to_word(x):
    show_hindi[0]='0'
#     print(show_hindi)
    col = x.tolist()
    new_col=[];all_series=[];final_cell_value=""

    if '   anu_exact_match  ' in col:
        new_col =[str(i) for i in col]
    else:
        for count, i in enumerate(col,0):
#             print(i, type(i))
            if i == '~':
                final_cell_value = '~'           #converted all int 0 to '0'
                new_col.append(final_cell_value)
                
            elif(i!= '0' and i!=0 ):  #code for those cell values which are neither '0' nor 0.
                i=str(i)           #changed all int to string
                change = i.lstrip().rstrip()
#                 print("===>", change) 
                pchange1 = change.replace('#', ' # ')
                pchange = pchange1.replace('/', ' / ')
#                 print(pchange)
                pchange_list = pchange.split()
#                 print(pchange_list)
                change1=[]
                for item in pchange_list:
                    if item=='#' :  #dont replace # and / with any word.
                        change1.append('#')
                    elif item =='/':
                        change1.append('/')
                    else:
                        if int(item) in show_hindi.keys():  # dict keys are int so typecasting item to int
                            change1.append(show_hindi[int(item)])  #here too typecasting needed
                    
#                 print(change1)
                final_cell_value=" ".join(change1)
                new_col.append(final_cell_value)
            
            
                
            else:
                final_cell_value = '0'           #converted all int 0 to '0'
                new_col.append(final_cell_value)
#         print("=======")        
            
    new_col.append(final_cell_value)
    new_col = new_col[:-1]
    new_x = pd.Series(new_col)
    return(new_x)


# print(dfs)

new = dfs.apply(id_to_word)
print(title)
new.columns = title
new.index = np.arange(1,len(dfs)+1)
new=new.set_index('Resources')
# new.index.name="R"
new.index.name = None

# with open(sent_dir+ '/Potential_debug.txt','a') as f:
#     multi = [x for x in list(new.iloc[23]) if '#' in x]
#     print( sent_no + " => " + " ".join(multi)+ "\n" )
#     f.write(sent_no + " => " + " ".join(multi)+ "\n")
# display(new)
#display(dfs)
dfs.to_csv(path_tmp +'/final_id.csv')
dfs


# In[18]:


# import re
# #=====================================================

# # Extracting and printing grouping information in [..][..] format
# hindi_row_tooltip = "".join(load_row_from_csv(h_group_html, 0))
# # print(hindi_row_tooltip)
# hindi_row = "".join(load_row_from_csv(h_group_html, 1))
# eng_row_tooltip = "".join(load_row_from_csv(e_group_html, 0))
# eng_row = "".join(load_row_from_csv(e_group_html, 1))

# #=====================================================
# #Prashant's and Saumya's grouping information
# def extract_from_grouping_ordered_facts(filename):
#     with open(filename, "r") as f:
#         data = f.read().split("\n")
#         while "" in data:
#             data.remove("")
#         egroups=[]
#         for x in data:
#             tmp_str = x.split(')')[1].split('ids ')[-1]
#             tmp_list = create_list_from_space_seperated_string(tmp_str)
#             tmp_list = [int(x) for x in tmp_list]
#             egroups.append(tmp_list)
#     return(egroups)

# #Prashant's and Saumya's grouping information
# egroup_file = path_tmp + '/E_Word_Group.txt'
# hgroup_file = path_tmp + '/H_Word_Group.txt'

# egroups = extract_from_grouping_ordered_facts(egroup_file)
# hgroups = extract_from_grouping_ordered_facts(hgroup_file)

# print(egroups)
# print(hgroups)

# #==================================
# def grouping_with_border_color_in_dataframe(egroups, lang_dataframe, color):
    
#     tmp=[]
#     for i in range(0,len(egroups)):
#         for j in range(0, len(egroups[i])):
#             tmp.append(".{} tbody tr >td:nth-child({}){{\nborder: 10px solid {};\n}}\n".format(lang_dataframe,egroups[i][j],color[i]))
#             ecode="".join(tmp)
#     return(ecode)
# # ecolor = ["MEDIUMBLUE","SKYBLUE","DARKGREEN","HOTPINK","SIENNA","SPRINGGREEN","REBECCAPURPLE","MOCCASIN","TEAL", "ORANGE","GREENYELLOW",
# # "KHAKI","AQUA","DARKGRAY","NAVY","ROSYBROWN","DARKSALMON","PAPAYAWHIP" ,"TAN", "THISTLE", "PALEVIOLETRED","LIGHTSALMON","LIGHTSTEELBLUE", "SANDYBROWN","ORCHID"]

# # hcolor =["CRIMSON", "OLIVE", "BLACK", "MEDIUMSPRINGGREEN","SALMON","PINK","SILVER", "CADETBLUE", "DARKKHAKI", "ROYALBLUE", "PERU ,"TOMATO", "LAVENDER", "SEAGREEN","NAVAJOWHITE","PALEVIOLETRED","CORAL","CORNFLOWERBLUE","MAROON","SLATEGRAY","DODGERBLUE","PLUM","MEDIUMVIOLETRED","DARKSLATEGRAY", "MISTYROSE"]
# # ecolor = ["MEDIUMBLUE","SKYBLUE","DARKGREEN","HOTPINK","SIENNA","SPRINGGREEN","REBECCAPURPLE","MOCCASIN","TEAL", "ORANGE","GREENYELLOW","KHAKI","AQUA","DARKGRAY","NAVY","ROSYBROWN","DARKSALMON","PAPAYAWHIP" ,"TAN", "THISTLE", "PALEVIOLETRED","LIGHTSALMON","LIGHTSTEELBLUE", "SANDYBROWN","ORCHID","CRIMSON", "OLIVE", "BLACK", "MEDIUMSPRINGGREEN","SALMON","PINK","SILVER", "CADETBLUE", "DARKKHAKI", "ROYALBLUE", "PERU ,"TOMATO", "LAVENDER", "SEAGREEN","NAVAJOWHITE","PALEVIOLETRED","CORAL","CORNFLOWERBLUE","MAROON","SLATEGRAY","DODGERBLUE","PLUM","MEDIUMVIOLETRED","DARKSLATEGRAY", "MISTYROSE"]
# ecolor = ["MEDIUMBLUE","SKYBLUE","DARKGREEN","HOTPINK","SIENNA","SPRINGGREEN","REBECCAPURPLE","MOCCASIN","TEAL", "ORANGE","GREENYELLOW","KHAKI","AQUA","DARKGRAY","NAVY","ROSYBROWN","DARKSALMON","PAPAYAWHIP" ,"TAN", "THISTLE", "PALEVIOLETRED","LIGHTSALMON","LIGHTSTEELBLUE", "SANDYBROWN","ORCHID","CRIMSON", "OLIVE", "BLACK", "MEDIUMSPRINGGREEN","SALMON","PINK","SILVER", "CADETBLUE", "DARKKHAKI", "ROYALBLUE", "PERU" ,"TOMATO", "LAVENDER", "SEAGREEN","NAVAJOWHITE","PALEVIOLETRED","CORAL","CORNFLOWERBLUE","MAROON","SLATEGRAY","DODGERBLUE","PLUM","MEDIUMVIOLETRED","DARKSLATEGRAY", "MISTYROSE"]

# hcolor =["CRIMSON", "OLIVE", "BLACK", "MEDIUMSPRINGGREEN","SALMON","PINK","SILVER", "CADETBLUE", "DARKKHAKI", "ROYALBLUE", "PERU" ,"TOMATO", "LAVENDER", "SEAGREEN","NAVAJOWHITE","PALEVIOLETRED","CORAL","CORNFLOWERBLUE","MAROON","SLATEGRAY","DODGERBLUE","PLUM","MEDIUMVIOLETRED","DARKSLATEGRAY", "MISTYROSE","DARKMAGENTA","PURPLE","INDIGO","SLATEBLUE","LAWNGREEN","LIME","LIMEGREEN","PALEGREEN","LIGHTGREEN","MEDIUMSPRINGGREEN","FORESTGREEN","GREEN","OLIVEDRAB","DARKOLIVEGREEN","MEDIUMAQUAMARINE","DARKCYAN","CYAN","LIGHTCYAN","PALETURQUOISE","AQUAMARINE","DIMGRAY","LINEN","SNOW","HONEYDEW","SADDLEBROWN"]

# print(len(ecolor))
# print(len(hcolor))

# ecode = grouping_with_border_color_in_dataframe(egroups,"english", ecolor)
# hcode = grouping_with_border_color_in_dataframe(hgroups, "hindi",hcolor)
# # print(hcode)
# # print(ecode)
# #======================================================
# #Bringing anchor information in english dataframe
# eng_hin_anchors=[]
# for item in range(1,no_of_eng_words):
# #     print(item, start_v2_dict[item])
# #     print(str(item) + " ("+ start_v2_dict[item]+")")
#     if start_dict[item]=='0':
#         tmp=str(item) 
#     else:
#         tmp = str(item) + " ("+ start_dict[item]+")"
#     eng_hin_anchors.append(tmp)
# print(eng_hin_anchors)
# # display(edf)

# try:
#     edf_trans=edf
#     edf_trans.insert(1,"new", eng_hin_anchors)
#     edf_trans=edf_trans.set_index('new')
#     edf_trans.index.name = None
#     edf_trans.T
# except:
#     print("new exists hence wont insert again")



# #======================================================


# In[19]:



# # hindi_row="[1_This 2_range]    [3_consists]    [4_of 5_the 6_famous 7_valley]    [8_of 9_Kashmir]    [10_the 11_Kangra]    [12_and]    [13_Kullu 14_Valley]    [15_in 16_Himachal 17_Pradesh]    "
# # hindi_row_tooltip="This range _ consists _ of the famous valley _ of Kashmir _ the Kangra _ and _ Kullu Valley _ in Himachal Pradesh"

# def write_to_html_file(df, filename=''):
#     '''
#     Write an entire dataframe to an HTML file with nice formatting.
#     '''

#     result = '''
# <html>
# <head>
# <style>
# h3{
# text-align: center;
# }
# h4{
# text-align: center;
# }




# /* Style the tab */
# .tab {
#   overflow: hidden;
#   border: 1px solid #ccc;
#   background-color: #f1f1f1;
# }

# /* Style the buttons inside the tab */
# .tab button {
#   background-color: inherit;
#   float: left;
#   border: none;
#   outline: none;
#   cursor: pointer;
#   padding: 14px 16px;
#   transition: 0.3s;
#   font-size: 17px;
# }

# /* Change background color of buttons on hover */
# .tab button:hover {
#   background-color: #ddd;
# }

# /* Create an active/current tablink class */
# .tab button.active {
#   background-color: #ccc;
# }

# /* Style the tab content */
# .tabcontent {
#   display: none;
#   padding: 6px 12px;
#   border: 1px solid #ccc;
#   border-top: none;
# }

# /* Style the tab content */
# .hcontent {
#   display: none;
#   padding: 6px 12px;
#   border: 1px solid #ccc;
#   border-top: none;
# }


# /* -------- Tooltip ---------- */

# .tooltip {
#   position: relative;
#   border-bottom: 1px dotted black;
  
# }

# .tooltip .tooltiptext {
#   visibility: hidden;
#   width: 1000px;
#   background-color: black;
#   color: #fff;
  
#   border-radius: 6px;
#   padding: 5px 0;
  
#   /* Position the tooltip */
#   position: absolute;
#   z-index: 1;
#   top: 100%;
#   left: 50%;
#   margin-left: -500px;
# }

# .tooltip:hover .tooltiptext {
#   visibility: visible;
# }

# /* -------- /Tooltip ---------- */




# .corner {
#   width: 0;
#   height: 0;
#   border-top: 90px solid #ffcc00;
#   border-bottom: 10px solid transparent;
#   border-left: 90px solid transparent;
#   position:fixed;
#   right:0;
#   margin:0px;
#   z-index: 2;
# }

# .corner span {
#   position:absolute;
#   top: -80px;
#   width: 100px;
#   left: -106px;
#   text-align: right;
#   font-size: 20px;
#   font-family: arial;
#   font-weight: bold;
#   display:block;
# }




# #gotoTop {
#   display: none;
#   position: fixed;
#   bottom: 20px;
#   right: 20px;
#   z-index: 99;
#   font-size: 18px;
#   border: none;
#   outline: none;
#   background-color: #a5a5a5;
#   color: white;
#   cursor: pointer;
#   padding: 12px;
#   border-radius: 10px;
# }

# #gotoTop:hover {
#   background-color: #555;
# }




# nav.float-action-button {
#   position: fixed;
#   bottom: 0;
#   right: 0;
#   margin: 90px 10px;
# }

# a.buttons {
#   box-shadow: 0 5px 11px -2px rgba(0, 0, 0, 0.18), 0 4px 12px -7px rgba(0, 0, 0, 0.15);
#   border-radius: 50%;
#   width: 56px;
#   height: 56px;
#   color: #000;
#   font-size: 18px;
#   padding: 15px 0 0 0;
#   text-align: center;
#   display: block;
#   margin: 20px auto 0;
#   position: relative;
#   -webkit-transition: all .1s ease-out;
#   transition: all .1s ease-out;
# }

# a.buttons:active,
# a.buttons:focus,
# a.buttons:hover {
#   box-shadow: 0 0 4px rgba(0, 0, 0, .14), 0 4px 8px rgba(0, 0, 0, .28);
#   text-decoration: none;
# }

# a.buttons:not(:last-child) {
#   width: 56px;
#   height: 56px;
#   margin: 20px auto 0;
#   opacity: 0;
#   font-size: 18px;
#   padding-top: 15px;
#   -webkit-transform: translateY(50px);
#   -ms-transform: translateY(50px);
#   transform: translateY(50px);
# }

# nav.float-action-button:hover a.buttons:not(:last-child) {
#   opacity: 1;
#   -webkit-transform: none;
#   -ms-transform: none;
#   transform: none;
#   margin: 20px auto 0;
# }

# a.buttons:nth-last-child(1) {
#   -webkit-transition-delay: 25ms;
#   transition-delay: 25ms;
#   background-color: #ffcc00;
#   /* Button color */
# }

# a.buttons:nth-last-child(1) i.fa {
#   transform: rotate3d(0, 0, 1, 0);
#   transition: content 0.4s, transform 0.4s, opacity 0.4s;
# }

# a.buttons:nth-last-child(1):hover i.fa {
#   transform: rotate3d(0, 0, 1, -180deg);
# }

# a.buttons:nth-last-child(1) i.fa:nth-last-child(1) {
#   position: absolute;
#   margin: 10px 0 0 -32px;
# }

# a.buttons:nth-last-child(1) i.fa:nth-last-child(2) {
#   opacity: 0;
# }

# a.buttons:nth-last-child(1):hover i.fa:nth-last-child(1) {
#   opacity: 0;
# }

# a.buttons:nth-last-child(1):hover i.fa:nth-last-child(2) {
#   opacity: 1;
# }

# a.buttons:not(:last-child):nth-last-child(2) {
#   -webkit-transition-delay: 50ms;
#   transition-delay: 20ms;
#   background-color: #ffcc00;
#   /* Facebook color */
# }

# a.buttons:not(:last-child):nth-last-child(3) {
#   -webkit-transition-delay: 75ms;
#   transition-delay: 40ms;
#   background-color: #ffcc00;
#   /* Twitter color */
# }

# a.buttons:not(:last-child):nth-last-child(4) {
#   -webkit-transition-delay: 100ms;
#   transition-delay: 60ms;
#   background-color: #ffcc00;
#   /* Google plus color */
# }

# .tooltip.left {
#   margin-left: -10px;
# }



# /* The Modal (background) */
# .modal {
#   display: none; /* Hidden by default */
#   position: fixed; /* Stay in place */
#   z-index: 1; /* Sit on top */
#   padding-top: 100px; /* Location of the box */
#   left: 0;
#   top: 0;
#   width: 100%; /* Full width */
#   height: 100%; /* Full height */
#   overflow: auto; /* Enable scroll if needed */
#   background-color: rgb(0,0,0); /* Fallback color */
#   background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
# }

# /* Modal Content */
# .modal-content {
#   position: relative;
#   background-color: #fefefe;
#   margin: auto;
#   padding: 0;
#   border: 1px solid #888;
#   width: 80%;
#   box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
#   -webkit-animation-name: animatetop;
#   -webkit-animation-duration: 0.4s;
#   animation-name: animatetop;
#   animation-duration: 0.4s
# }

# /* Add Animation */
# @-webkit-keyframes animatetop {
#   from {top:-300px; opacity:0} 
#   to {top:0; opacity:1}
# }

# @keyframes animatetop {
#   from {top:-300px; opacity:0}
#   to {top:0; opacity:1}
# }

# /* The Close Button */
# .close {
#     color: white;
#     float: right;
#     font-size: 35px;
#     font-weight: bold;
# 	padding:15px;
# }

# .close:hover,
# .close:focus {
#     color: #000;
#     text-decoration: none;
#     cursor: pointer;
# }

# .modal-header {
#   padding: 2px 16px;
#   background-color: #5cb85c;
#   color: white;
# }

# .modal-body {padding: 10px 16px;}

# .modal-footer {
#   padding: 2px 16px;
#   background-color: #5cb85c;
#   color: white;
# }

# /* English and Hindi DF's */

# '''
#     result += '{}' .format(ecode)
#     result += '{}' .format(hcode)
   
#     result += '''
    
# </style>
# 		<meta charset="UTF-8" />
# 		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
# 		<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
# 		<title>Anusaaraka Output</title>
# 		<link rel="stylesheet" type="text/css" href="../styles/css/normalize.css" />
# 		<link rel="stylesheet" type="text/css" href="../styles/css/demo.css" />
# 		<link rel="stylesheet" type="text/css" href="../styles/css/component.css" />
# 		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
# 		<script src="http://cdnjs.cloudflare.com/ajax/libs/jquery-throttle-debounce/1.1/jquery.ba-throttle-debounce.min.js"></script>
# 		<script src="../styles/js/jquery.stickyheader.js">
#         <link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
# </script>
        
# <script>
# var sUsrAg = navigator.userAgent,
#   usingChrome = sUsrAg.indexOf("Chrome") > -1;

# if (!usingChrome) {
#   alert("Please use Google chrome to access this page. Some features do not work in browsers other than Chrome.");
# }
# </script>       

# </head>
# <body>
#     '''
#     result += '<p class="corner"><span>%s</span></p>' % sent_no
#     result += '<button onclick="topFunction()" id="gotoTop" title="Go to top">&#8679;</button>'
#     result += '<br><h3> Sentence Number: %s &nbsp &nbsp &nbsp|&nbsp &nbsp &nbsp Reference English Text: <a href="iess102.pdf" target="_blank">English Chapter 2</a> &nbsp &nbsp &nbsp|&nbsp &nbsp &nbsp  Reference Hindi Text: <a href="ihss102.pdf" target="_blank">Hindi Chapter 2</a></h3><hr>' % sent_no
#     result += '<h3> %s </h3>\n<hr>' % es
# #     result += '<h3> %s </h3><button onclick="myFunction()">i</button>\n<hr>' % es
# #     result += '<h4 class="tooltip"> {0} <span class="tooltiptext"> {1} </span></h4>\n' .format(eng_row,eng_row_tooltip)

#     result += '<h3> %s </h3>\n' % hs
# #     result += '<h4 class="tooltip"> {0} <span class="tooltiptext"> {1} </span></h4>\n' .format(hindi_row,hindi_row_tooltip)
# #     result += '<span class="tooltiptext"> %s </span>\n' % hindi_row_tooltip
#     result += df.to_html(classes='wide overflow-y', escape=False)
#     #result += '<center> <img src="{0}"> <hr> <img src="{1}"> <hr> </center>' .format(eimg,himg)
# #     result += '<center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="640" height="879" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center>'

#     result += '<h4 class="tooltip"> English Grouping: {0} <span class="tooltiptext"> {1} </span></h4>\n <hr>' .format(eng_row,eng_row_tooltip)

#     result += '<h4 class="tooltip"> Hindi Grouping: {0} <span class="tooltiptext"> {1} </span></h4>\n' .format(hindi_row,hindi_row_tooltip)

#     result += '''
    
   
    
#  <center><h2>English Dependency Parse Trees</h2></center>

# <div class="tab">
#   <button class="tablinks" onclick="openCity(event, 'E1')">English Final</button>
#   <button class="tablinks" onclick="openCity(event, 'E2')">English Corrected</button>
#   <button class="tablinks" onclick="openCity(event, 'E3')">English Initial</button>
# </div>

# <div id="E1" class="tabcontent">
#   <h3>Transfored  Tree version2<br><br>Tree after local word grouping of intrachunk relations.</h3>
#   '''
#     result += '<center> <img src="{}"></center>' .format(eimg)
   
#     result += '''
    
    
# </div>

# <div id="E2" class="tabcontent">
#   <h3>Transfored  Tree version1<br><br>Changed obl tags and transformed cc-conj structure.</h3>
#   '''
#     result += '<center> <img src="{}"></center>' .format(eimg2)
    
#     result += '''
    
# </div>

# <div id="E3" class="tabcontent">
#   <h3>Original parse by parser<br><br>Stanford's 3.9 Dependency parse.</h3>
#   '''
#     result += '<center> <img src="{}"></center>' .format(eimg1)
    
#     result += '''
# </div>




#  <center><h2>Hindi Dependency Parse Trees</h2></center>

# <div class="tab">
#   <button class="hlinks" onclick="hCity(event, 'H1')">Hindi Final</button>
#   <button class="hlinks" onclick="hCity(event, 'H2')">Hindi Corrected</button>
#   <button class="hlinks" onclick="hCity(event, 'H3')">Hindi Initial</button>
# </div>

# <div id="H1" class="hcontent">
#   <h3>Transfored  Tree version2<br>Tree after local word grouping of intrachunk relations.</h3>
#   '''
#     result += '<center> <img src="{}"></center>' .format(himg)
   
#     result += '''
    
# </div>

# <div id="H2" class="hcontent">
#   <h3>Transfored  Tree version1<br><br>Changed obl tags and transformed cc-conj structure.</h3>

#   '''
#     result += '<center> <img src="{}"></center>' .format(himg2)
    
#     result += '''
    
# </div>

# <div id="H3" class="hcontent">
#   <h3>Orginal Parse<br><br>Irshad's Hindi Neural parse trained on UD annotated hindi treebank [IIIT].</h3>
  
#     '''
#     result += '<center> <img src="{}"></center>' .format(himg1)
    
#     result += '''
# </div>

#     '''
# #     result += '<center>{}></center>' .format(edf)
#     try:
#         result += edf_trans.T.to_html(classes="english", escape=False, index=False)
#         result += hdf.T.to_html(classes="hindi", escape=False, index=False)
#     except:
#         print("edf try catch")
    
#     '''
    
#     '''
# #     result += '<center style="padding-top:25px"><h4> Sentence Number: %s </h4></center>\n' % sent_no
# #     result += '<center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="800" height="700" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center>'

#     result += '''
#     <br>
# <!-- dictionary links -->
# <nav class="float-action-button"> 
#         <a href="https://https://www.collinsdictionary.com/dictionary/english-hindi" target="_blank" class="buttons" title="Collins Dictionary" data-toggle="tooltip" data-placement="left">
#           <i>Collin</i>
#         </a>
#        <a href="https://archive.org/details/in.ernet.dli.2015.464149" target="_blank" class="buttons" title="Collins Dictionary" data-toggle="tooltip" data-placement="left">
#           <i>Kosh</i>
#         </a>
# 		<a href="#" id="myBtn2" class="buttons" title="Sentence Observations" data-toggle="tooltip" data-placement="left">
#           <i>Form</i>
#         </a>
#         <a href="#" class="buttons" title="Links" data-toggle="tooltip" data-placement="left">
#           <i>Links</i>
   
#         </a>
# </nav>


# <!-- The Modal -->
# <div id="myModal2" class="modal">
# <!-- Modal content -->
#   <div class="modal-content">
#       <span class="close second">&times;</span>
#     <div class="modal-header">
#       <h2>Form</h2>
#     </div>
#     <div class="modal-body">
#       <p><center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="640" height="879" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center> </p>

#     </div>
#     <div class="modal-footer">
#       <h3>Modal Footer</h3>
#     </div>
#   </div>
#   </div>
# </div>

# <script>

# // When the user scrolls down 20px from the top of the document, show the button
# window.onscroll = function() {scrollFunction()};

# function scrollFunction() {
#     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
#         document.getElementById("gotoTop").style.display = "block";
#     } else {
#         document.getElementById("gotoTop").style.display = "none";
#     }
   
# }

# // When the user clicks on the button, scroll to the top of the document
# function topFunction() {
 
#      $('html, body').animate({scrollTop:0}, 'slow');
# }

# </script>

# <script>
# // Get the modal
# var modal1 = document.getElementById("myModal1");
# var modal2 = document.getElementById("myModal2");

# // Get the button that opens the modal
# var btn1 = document.getElementById("myBtn1");
# var btn2 = document.getElementById("myBtn2");


# // Get the <span> element that closes the modal
# var span1 = document.getElementsByClassName("close")[0];
# var span2 = document.getElementsByClassName("close second")[0];


# // When the user clicks the button, open the modal
# btn1.onclick = function() {
#     modal1.style.display = "block";
# }
# btn2.onclick = function() {
#     modal2.style.display = "block";
# }

# // When the user clicks on <span> (x), close the modal
# span1.onclick = function() {
#     modal1.style.display = "none";
# }

# span2.onclick = function() {
#     modal2.style.display = "none";
# }

# window.onclick = function(event) {
#     if (event.target == modal1) {
#         modal1.style.display = "none";
#     }
#     if (event.target == modal2) {
#         modal2.style.display = "none";
#     }
# }
# </script>

# <script>
# function openCity(evt, cityName) {
#   var i, tabcontent, tablinks;
#   tabcontent = document.getElementsByClassName("tabcontent");
#   for (i = 0; i < tabcontent.length; i++) {
#     tabcontent[i].style.display = "none";
#   }
#   tablinks = document.getElementsByClassName("tablinks");
#   for (i = 0; i < tablinks.length; i++) {
#     tablinks[i].className = tablinks[i].className.replace(" active", "");
#   }
#   document.getElementById(cityName).style.display = "block";
#   evt.currentTarget.className += " active";
# }
# </script>

# <script>

# function hCity(hevt, hName) {
#   var j, hcontent, hlinks;
#   hcontent = document.getElementsByClassName("hcontent");
#   for (j = 0; j < hcontent.length; j++) {
#     hcontent[j].style.display = "none";
#   }
#   hlinks = document.getElementsByClassName("hlinks");
#   for (j = 0; j < hlinks.length; j++) {
#     hlinks[j].className = hlinks[j].className.replace(" active", "");
#   }
#   document.getElementById(hName).style.display = "block";
#   hevt.currentTarget.className += " active";
# }
# </script>

# <script>
# function myFunction() {
#   var x = document.getElementById("myDIV");
#   if (x.style.display === "none") {
#     x.style.display = "block";
#   } else {
#     x.style.display = "none";
#   }
# }
# </script>
# </body>
# </html>
# '''
#     with open(filename, 'w', encoding="utf-8") as f:
#         f.write(result)
        
# write_to_html_file(new, path_tmp+'/final.html')
# new.to_csv(path_tmp +'/final.csv')
# # new.to_html(path_tmp +'/final.html')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# # hindi_row="[1_This 2_range]    [3_consists]    [4_of 5_the 6_famous 7_valley]    [8_of 9_Kashmir]    [10_the 11_Kangra]    [12_and]    [13_Kullu 14_Valley]    [15_in 16_Himachal 17_Pradesh]    "

# # hindi_row_tooltip="This range _ consists _ of the famous valley _ of Kashmir _ the Kangra _ and _ Kullu Valley _ in Himachal Pradesh"

# def write_to_html_file(df, filename=''):
#     '''
#     Write an entire dataframe to an HTML file with nice formatting.
#     '''

#     result = '''
# <html>
# <head>
# <style>
# h3{
# text-align: center;
# }
# h4{
# text-align: center;
# }




# /* Style the tab */
# .tab {
#   overflow: hidden;
#   border: 1px solid #ccc;
#   background-color: #f1f1f1;
# }

# /* Style the buttons inside the tab */
# .tab button {
#   background-color: inherit;
#   float: left;
#   border: none;
#   outline: none;
#   cursor: pointer;
#   padding: 14px 16px;
#   transition: 0.3s;
#   font-size: 17px;
# }

# /* Change background color of buttons on hover */
# .tab button:hover {
#   background-color: #ddd;
# }

# /* Create an active/current tablink class */
# .tab button.active {
#   background-color: #ccc;
# }

# /* Style the tab content */
# .tabcontent {
#   display: none;
#   padding: 6px 12px;
#   border: 1px solid #ccc;
#   border-top: none;
# }

# /* Style the tab content */
# .hcontent {
#   display: none;
#   padding: 6px 12px;
#   border: 1px solid #ccc;
#   border-top: none;
# }


# /* -------- Tooltip ---------- */

# .tooltip {
#   position: relative;
#   border-bottom: 1px dotted black;
  
# }

# .tooltip .tooltiptext {
#   visibility: hidden;
#   width: 1000px;
#   background-color: black;
#   color: #fff;
  
#   border-radius: 6px;
#   padding: 5px 0;
  
#   /* Position the tooltip */
#   position: absolute;
#   z-index: 1;
#   top: 100%;
#   left: 50%;
#   margin-left: -500px;
# }

# .tooltip:hover .tooltiptext {
#   visibility: visible;
# }

# /* -------- /Tooltip ---------- */




# .corner {
#   width: 0;
#   height: 0;
#   border-top: 90px solid #ffcc00;
#   border-bottom: 10px solid transparent;
#   border-left: 90px solid transparent;
#   position:fixed;
#   right:0;
#   margin:0px;
#   z-index: 2;
# }

# .corner span {
#   position:absolute;
#   top: -80px;
#   width: 100px;
#   left: -106px;
#   text-align: right;
#   font-size: 20px;
#   font-family: arial;
#   font-weight: bold;
#   display:block;
# }




# #gotoTop {
#   display: none;
#   position: fixed;
#   bottom: 20px;
#   right: 20px;
#   z-index: 99;
#   font-size: 18px;
#   border: none;
#   outline: none;
#   background-color: #a5a5a5;
#   color: white;
#   cursor: pointer;
#   padding: 12px;
#   border-radius: 10px;
# }

# #gotoTop:hover {
#   background-color: #555;
# }




# nav.float-action-button {
#   position: fixed;
#   bottom: 0;
#   right: 0;
#   margin: 90px 10px;
# }

# a.buttons {
#   box-shadow: 0 5px 11px -2px rgba(0, 0, 0, 0.18), 0 4px 12px -7px rgba(0, 0, 0, 0.15);
#   border-radius: 50%;
#   width: 56px;
#   height: 56px;
#   color: #000;
#   font-size: 18px;
#   padding: 15px 0 0 0;
#   text-align: center;
#   display: block;
#   margin: 20px auto 0;
#   position: relative;
#   -webkit-transition: all .1s ease-out;
#   transition: all .1s ease-out;
# }

# a.buttons:active,
# a.buttons:focus,
# a.buttons:hover {
#   box-shadow: 0 0 4px rgba(0, 0, 0, .14), 0 4px 8px rgba(0, 0, 0, .28);
#   text-decoration: none;
# }

# a.buttons:not(:last-child) {
#   width: 56px;
#   height: 56px;
#   margin: 20px auto 0;
#   opacity: 0;
#   font-size: 18px;
#   padding-top: 15px;
#   -webkit-transform: translateY(50px);
#   -ms-transform: translateY(50px);
#   transform: translateY(50px);
# }

# nav.float-action-button:hover a.buttons:not(:last-child) {
#   opacity: 1;
#   -webkit-transform: none;
#   -ms-transform: none;
#   transform: none;
#   margin: 20px auto 0;
# }

# a.buttons:nth-last-child(1) {
#   -webkit-transition-delay: 25ms;
#   transition-delay: 25ms;
#   background-color: #ffcc00;
#   /* Button color */
# }

# a.buttons:nth-last-child(1) i.fa {
#   transform: rotate3d(0, 0, 1, 0);
#   transition: content 0.4s, transform 0.4s, opacity 0.4s;
# }

# a.buttons:nth-last-child(1):hover i.fa {
#   transform: rotate3d(0, 0, 1, -180deg);
# }

# a.buttons:nth-last-child(1) i.fa:nth-last-child(1) {
#   position: absolute;
#   margin: 10px 0 0 -32px;
# }

# a.buttons:nth-last-child(1) i.fa:nth-last-child(2) {
#   opacity: 0;
# }

# a.buttons:nth-last-child(1):hover i.fa:nth-last-child(1) {
#   opacity: 0;
# }

# a.buttons:nth-last-child(1):hover i.fa:nth-last-child(2) {
#   opacity: 1;
# }

# a.buttons:not(:last-child):nth-last-child(2) {
#   -webkit-transition-delay: 50ms;
#   transition-delay: 20ms;
#   background-color: #ffcc00;
#   /* Facebook color */
# }

# a.buttons:not(:last-child):nth-last-child(3) {
#   -webkit-transition-delay: 75ms;
#   transition-delay: 40ms;
#   background-color: #ffcc00;
#   /* Twitter color */
# }

# a.buttons:not(:last-child):nth-last-child(4) {
#   -webkit-transition-delay: 100ms;
#   transition-delay: 60ms;
#   background-color: #ffcc00;
#   /* Google plus color */
# }

# .tooltip.left {
#   margin-left: -10px;
# }



# /* The Modal (background) */
# .modal {
#   display: none; /* Hidden by default */
#   position: fixed; /* Stay in place */
#   z-index: 1; /* Sit on top */
#   padding-top: 100px; /* Location of the box */
#   left: 0;
#   top: 0;
#   width: 100%; /* Full width */
#   height: 100%; /* Full height */
#   overflow: auto; /* Enable scroll if needed */
#   background-color: rgb(0,0,0); /* Fallback color */
#   background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
# }

# /* Modal Content */
# .modal-content {
#   position: relative;
#   background-color: #fefefe;
#   margin: auto;
#   padding: 0;
#   border: 1px solid #888;
#   width: 80%;
#   box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2),0 6px 20px 0 rgba(0,0,0,0.19);
#   -webkit-animation-name: animatetop;
#   -webkit-animation-duration: 0.4s;
#   animation-name: animatetop;
#   animation-duration: 0.4s
# }

# /* Add Animation */
# @-webkit-keyframes animatetop {
#   from {top:-300px; opacity:0} 
#   to {top:0; opacity:1}
# }

# @keyframes animatetop {
#   from {top:-300px; opacity:0}
#   to {top:0; opacity:1}
# }

# /* The Close Button */
# .close {
#     color: white;
#     float: right;
#     font-size: 35px;
#     font-weight: bold;
# 	padding:15px;
# }

# .close:hover,
# .close:focus {
#     color: #000;
#     text-decoration: none;
#     cursor: pointer;
# }

# .modal-header {
#   padding: 2px 16px;
#   background-color: #5cb85c;
#   color: white;
# }

# .modal-body {padding: 10px 16px;}

# .modal-footer {
#   padding: 2px 16px;
#   background-color: #5cb85c;
#   color: white;
# }




# </style>
# 		<meta charset="UTF-8" />
# 		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
# 		<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
# 		<title>Anusaaraka Output</title>
# 		<link rel="stylesheet" type="text/css" href="../styles/css/normalize.css" />
# 		<link rel="stylesheet" type="text/css" href="../styles/css/demo.css" />
# 		<link rel="stylesheet" type="text/css" href="../styles/css/component.css" />
# 		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
# 		<script src="http://cdnjs.cloudflare.com/ajax/libs/jquery-throttle-debounce/1.1/jquery.ba-throttle-debounce.min.js"></script>
# 		<script src="../styles/js/jquery.stickyheader.js">
#         <link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
# </script>
        
# <script>
# var sUsrAg = navigator.userAgent,
#   usingChrome = sUsrAg.indexOf("Chrome") > -1;

# if (!usingChrome) {
#   alert("Please use Google chrome to access this page. Some features do not work in browsers other than Chrome.");
# }
# </script>       

# </head>
# <body>
#     '''
#     result += '<button onclick="topFunction()" id="gotoTop" title="Go to top">&#8679;</button>'
#     result += '<h3> <a href="https://docs.google.com/document/d/1YAXKVYBlt_MGWgoyHbULq4YsWHLwrmkr0EGPTit5zfs/edit?usp=sharing" target="_blank">Alignment Guidelines</a> </h3>\n<hr>' 
# #      result += '<p class="corner"><span>%s</span></p>' % sent_no
    
#     result += '<h3> Sentence Number: %s &nbsp &nbsp &nbsp|&nbsp &nbsp &nbsp Reference English Text: <a href="../iess102.pdf" target="_blank">English Chapter 2</a> &nbsp &nbsp &nbsp|&nbsp &nbsp &nbsp  Reference Hindi Text: <a href="../ihss102.pdf" target="_blank">Hindi Chapter 2</a></h3><hr>' % sent_no
#     result += '<h3> %s </h3>\n<hr>' % es
# #     result += '<h3> %s </h3><button onclick="myFunction()">i</button>\n<hr>' % es
# #     result += '<h4 class="tooltip"> {0} <span class="tooltiptext"> {1} </span></h4>\n' .format(eng_row,eng_row_tooltip)

#     result += '<h3> %s </h3>\n' % hs
# #     result += '<h4 class="tooltip"> {0} <span class="tooltiptext"> {1} </span></h4>\n' .format(hindi_row,hindi_row_tooltip)
# #     result += '<span class="tooltiptext"> %s </span>\n' % hindi_row_tooltip
#     result += df.to_html(classes='wide overflow-y', escape=False)
#     #result += '<center> <img src="{0}"> <hr> <img src="{1}"> <hr> </center>' .format(eimg,himg)
# #     result += '<center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="640" height="879" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center>'

#     result += '<h4 class="tooltip"> English Grouping: {0} <span class="tooltiptext"> {1} </span></h4>\n <hr>' .format(eng_row,eng_row_tooltip)

#     result += '<h4 class="tooltip"> Hindi Grouping: {0} <span class="tooltiptext"> {1} </span></h4>\n' .format(hindi_row,hindi_row_tooltip)

#     result += '''
    
   
    
#  <center><h2>English Dependency Parse Trees</h2></center>

# <div class="tab">
#   <button class="tablinks" onclick="openCity(event, 'E1')">English Final</button>
#   <button class="tablinks" onclick="openCity(event, 'E2')">English Corrected</button>
#   <button class="tablinks" onclick="openCity(event, 'E3')">English Initial</button>
# </div>

# <div id="E1" class="tabcontent">
#   <h3>Transfored  Tree version2<br><br>Tree after local word grouping of intrachunk relations.</h3>
#   '''
#     result += '<center> <img src="{}"></center>' .format(eimg)
   
#     result += '''
    
    
# </div>

# <div id="E2" class="tabcontent">
#   <h3>Transfored  Tree version1<br><br>Changed obl tags and transformed cc-conj structure.</h3>
#   '''
#     result += '<center> <img src="{}"></center>' .format(eimg2)
    
#     result += '''
    
# </div>

# <div id="E3" class="tabcontent">
#   <h3>Original parse by parser<br><br>Stanford's 3.9 Dependency parse.</h3>
#   '''
#     result += '<center> <img src="{}"></center>' .format(eimg1)
    
#     result += '''
# </div>




#  <center><h2>Hindi Dependency Parse Trees</h2></center>

# <div class="tab">
#   <button class="hlinks" onclick="hCity(event, 'H1')">Hindi Final</button>
#   <button class="hlinks" onclick="hCity(event, 'H2')">Hindi Corrected</button>
#   <button class="hlinks" onclick="hCity(event, 'H3')">Hindi Initial</button>
# </div>

# <div id="H1" class="hcontent">
#   <h3>Transfored  Tree version2<br>Tree after local word grouping of intrachunk relations.</h3>
#   '''
#     result += '<center> <img src="{}"></center>' .format(himg)
   
#     result += '''
    
    
# </div>

# <div id="H2" class="hcontent">
#   <h3>Transfored  Tree version1<br><br>Changed obl tags and transformed cc-conj structure.</h3>

#   '''
#     result += '<center> <img src="{}"></center>' .format(himg2)
    
#     result += '''
    
# </div>

# <div id="H3" class="hcontent">
#   <h3>Orginal Parse<br><br>Irshad's Hindi Neural parse trained on UD annotated hindi treebank [IIIT].</h3>
  
#   '''
#     result += '<center> <img src="{}"></center>' .format(himg1)
    
#     result += '''
# </div>



#     '''
    
# #     result += '<center style="padding-top:25px"><h4> Sentence Number: %s </h4></center>\n' % sent_no
# #     result += '<center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="800" height="700" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center>'

#     result += '''
#     <br>
# <!-- dictionary links -->
# <nav class="float-action-button"> 
#         <a href="https://www.collinsdictionary.com/dictionary/english-hindi" target="_blank" class="buttons" title="Collins Dictionary" data-toggle="tooltip" data-placement="left">
#           <i>Collin</i>
#         </a>
#        <a href="https://www.oxfordlearnersdictionaries.com/" target="_blank" class="buttons" title="Oxford Dictionary" data-toggle="tooltip" data-placement="left">
#           <i>Oxford</i>
#         </a>
#         <a href="http://www.cfilt.iitb.ac.in/wordnet/webhwn/wn.php" target="_blank" class="buttons" title="Hindi Wordnet" data-toggle="tooltip" data-placement="left">
#           <i>Wordnet</i>
#         </a>
        
#         <!--
# 		<a href="#" id="myBtn2" class="buttons" title="Sentence Observations" data-toggle="tooltip" data-placement="left"> 
#           <i>Form</i>
#         </a>
#         -->
#         <a href="#" class="buttons" title="Links" data-toggle="tooltip" data-placement="left">
#           <i>Links</i>
   
#         </a>
# </nav>


# <!-- The Modal -->
# <div id="myModal2" class="modal">
# <!-- Modal content -->
#   <div class="modal-content">
#       <span class="close second">&times;</span>
#     <div class="modal-header">
#       <h2>Form</h2>
#     </div>
#     <div class="modal-body">
#       <p><center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="640" height="879" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center> </p>

#     </div>
#     <div class="modal-footer">
#       <h3>Modal Footer</h3>
#     </div>
#   </div>
#   </div>
# </div>

# <script>

# // When the user scrolls down 20px from the top of the document, show the button
# window.onscroll = function() {scrollFunction()};

# function scrollFunction() {
#     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
#         document.getElementById("gotoTop").style.display = "block";
#     } else {
#         document.getElementById("gotoTop").style.display = "none";
#     }
   
# }

# // When the user clicks on the button, scroll to the top of the document
# function topFunction() {
 
#      $('html, body').animate({scrollTop:0}, 'slow');
# }

# </script>

# <script>
# // Get the modal
# var modal1 = document.getElementById("myModal1");
# var modal2 = document.getElementById("myModal2");

# // Get the button that opens the modal
# var btn1 = document.getElementById("myBtn1");
# var btn2 = document.getElementById("myBtn2");


# // Get the <span> element that closes the modal
# var span1 = document.getElementsByClassName("close")[0];
# var span2 = document.getElementsByClassName("close second")[0];


# // When the user clicks the button, open the modal
# btn1.onclick = function() {
#     modal1.style.display = "block";
# }
# btn2.onclick = function() {
#     modal2.style.display = "block";
# }

# // When the user clicks on <span> (x), close the modal
# span1.onclick = function() {
#     modal1.style.display = "none";
# }

# span2.onclick = function() {
#     modal2.style.display = "none";
# }

# window.onclick = function(event) {
#     if (event.target == modal1) {
#         modal1.style.display = "none";
#     }
#     if (event.target == modal2) {
#         modal2.style.display = "none";
#     }
# }
# </script>

# <script>
# function openCity(evt, cityName) {
#   var i, tabcontent, tablinks;
#   tabcontent = document.getElementsByClassName("tabcontent");
#   for (i = 0; i < tabcontent.length; i++) {
#     tabcontent[i].style.display = "none";
#   }
#   tablinks = document.getElementsByClassName("tablinks");
#   for (i = 0; i < tablinks.length; i++) {
#     tablinks[i].className = tablinks[i].className.replace(" active", "");
#   }
#   document.getElementById(cityName).style.display = "block";
#   evt.currentTarget.className += " active";
# }
# </script>

# <script>

# function hCity(hevt, hName) {
#   var j, hcontent, hlinks;
#   hcontent = document.getElementsByClassName("hcontent");
#   for (j = 0; j < hcontent.length; j++) {
#     hcontent[j].style.display = "none";
#   }
#   hlinks = document.getElementsByClassName("hlinks");
#   for (j = 0; j < hlinks.length; j++) {
#     hlinks[j].className = hlinks[j].className.replace(" active", "");
#   }
#   document.getElementById(hName).style.display = "block";
#   hevt.currentTarget.className += " active";
# }
# </script>

# <script>
# function myFunction() {
#   var x = document.getElementById("myDIV");
#   if (x.style.display === "none") {
#     x.style.display = "block";
#   } else {
#     x.style.display = "none";
#   }
# }
# </script>
# </body>
# </html>
# '''
#     with open(filename, 'w', encoding="utf-8") as f:
#         f.write(result)
        
# write_to_html_file(new, path_tmp+'/final.html')
# new.to_csv(path_tmp +'/final.csv')
# # new.to_html(path_tmp +'/final.html')


# In[ ]:


# #Integrating technical dictionary

# #Correctness of range
# def check_multi_or_single_word_equivalence(l):
#     if len(l) == len(set(l)):
#         return(l)
#     else:
#         return(l[0])

# #created for extracting eid-hid pair corresponding to eword-hword pair of roja_chk_transliteration_out
# def get_E_H_dict_Ids_mfs(filename):
#     tmp={}
#     with open(filename,'r') as f:
#         entries=f.read().strip("\n").split("\n")
#         entries = [item.rstrip(")") for item in entries]
#         for entry in entries:
#             print(entry)
#             entry  = entry.lstrip("(E_word-mfs-H_word	")
#             new_entry = entry.split("\tmfs\t")
# #             print(new_entry)
#             ewords = new_entry[0]
#             hwords = new_entry[1]
#             if " " in ewords or " " in hwords:
#                 print("multi-equivalence")
#                 if " " in ewords:
#                     x=ewords.split(" ")[0]
#                     eng_multiword_len = len(ewords.split(" "))
#                 else:
#                     x=ewords
#                     eng_multiword_len = 0
#                 if " " in hwords: 
#                     y=hwords.split(" ")[0]
#                     hin_multiword_len = len(hwords.split(" "))
#                 else:
#                     y=hwords
#                     hin_multiword_len = 0
# #                 print(x,y)
#                 eid = return_key_from_value(e2w, x)
#                 hid = return_key_from_value(h2w, y)
#                 final_eids = check_multi_or_single_word_equivalence([eid, eid+eng_multiword_len-1])
#                 final_hids = check_multi_or_single_word_equivalence([hid, hid+hin_multiword_len-1])
# #                 print([eid, eid + eng_multiword_len], [hid, hid + eng_multiword_len])
#                 print(final_eids,final_hids)
# #                 print(check_multi_or_single_word_equivalence([2,4]))
# #                 print(type(check_multi_or_single_word_equivalence([2,4])))
# #                     
# #                     
#                 if type(final_hids)==list:
#                     print("list it is")
#                     final_hids_str = " ".join([str(i) for i in final_hids])
#                 else:
#                     final_hids_str = str(y)
#                 tmp[final_eids[-1]] = final_hids_str
#                 for i in final_eids[:-1]:
#                     tmp[i]='~'
# #                     print(i)
                

#             else:
#                 print("one-to-one entry")
#                 eid = return_key_from_value(e2w, ewords)
#                 hid = return_key_from_value(h2w, hwords)
#                 print(eid, hid)
#                 final_eids =eid; final_hids=hid           #IMP
#                 if final_eids not in tmp:
#                     tmp[final_eids] = final_hids
            
            
            
# #             tmp[str(eid)] = str(hid)
#         print(tmp)
#     return(tmp)    

# tech_dict_filename = path_tmp + '/Tech_dict_lookup.dat'
# tech_dict_dict = get_E_H_dict_Ids_mfs(tech_dict_filename)
# tech_dict_list=[]
# for j in range(0,no_of_eng_words):
#     if j in tech_dict_dict.keys():
#         #         print(str(j), transliterate_mapping[str(j)])
#         tech_dict_list.append(tech_dict_dict[j])
#     else:
#         #         print(str(j), '0')
#         tech_dict_list.append('0')
# tech_dict_list[0] = 'Bharatwani Dict.'
#     # print(roja_transliterate_list)   
# #     dfs.loc[28] = roja_transliterate_list
# dfs.loc[dfs.index[-1]+1] = tech_dict_list

# dfs


# In[ ]:





# In[ ]:





# In[ ]:




