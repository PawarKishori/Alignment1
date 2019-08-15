#!/usr/bin/env python
# coding: utf-8

# In[35]:

# In[36]:


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
#tmp_path='/home/kishori/a/tmp_anu_dir/tmp/BUgol_13_aug/'
# eng_file_name = 'cc_conjE'

#eng_file_name = 'BUgol2.1E'
#sent_no = '2.89' #2.29, 2.21, 2.61, 2.14, 2.64

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


es=open(path_tmp+ '/E_sentence').read()
hs=open(path_tmp + '/H_sentence').read()
hs = H_Modules.wx_utf_converter_sentence(hs)

print(hs)


himg = path_tmp+'/H_tree_final.png'
eimg = path_tmp+'/E_tree_final.png'

if os.path.exists(log_file):
    os.remove(log_file)
log = open(log_file,'a')
#------------------------------------------------------------------------------------


# In[37]:


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





# In[38]:


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

#created for extracting eid-hid pair corresponding to eword-hword pair of roja_chk_transliteration_out
def get_E_H_dict_Ids(filename):
    tmp={}
    with open(filename,'r') as f:
        
#         print(f.read().strip("\n").split("\n"))
        entries=f.read().strip("\n").split("\n")
#         print("=>",entries)
        entries = [item.rstrip(")") for item in entries]
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
    return(tmp)    

#------------------------------------------------------------------------------------


# In[39]:


#$$$ 4

#Functions for anchor calculations:


def union_of_columns_verically(dfs):
    final_row_in_csv=[]
    for j in range(0,no_of_eng_words):
        hindi_allocations_list=[]
        #for every row extracted all non zero entries and stored in hindi_allocations_list
        hindi_allocations_list = [str(i) for i in dfs.iloc[:,j].tolist() if i!='0' and i!=0]
    
        #For an empty hindi_allocations_list i.e verical column equivalent to 1 eng id appended '0' entry in it.
        if not hindi_allocations_list:
            hindi_allocations_list.append('0')
            
        #hindi_allocations string contains all entries in vertical column with "#" seperator.
        hindi_allocations = "#".join([str(i) for i in hindi_allocations_list])        
        final_row_in_csv.append(hindi_allocations)
    return(final_row_in_csv)

#taking union on repreated entries
def remove_duplicates_from_union(final_row_in_csv):
    anchor1=[]; anchor1_str_list=[]; count_dict_list=[]
    for j in range(0,no_of_eng_words):
        temp=[];temp1=[]; temp_count_dict={}
        temp = re.split('#|/',final_row_in_csv[j])
        temp1 = list(dict.fromkeys(re.split('#|/',final_row_in_csv[j])))
        count_info = [temp.count(x) for x in temp1]

        for i in range(len(temp1)):
            temp_count_dict[temp1[i]] = count_info[i]
    
        count_dict_list.append(temp_count_dict)
        anchor1.append(temp1)
        anchor1_str_list.append("#".join(temp1))  
    return(anchor1, anchor1_str_list, count_dict_list)


def remove_multi_entry_in_a_cell(anchor1):
    anchor2=[]; anchor2_str_list=[]
    for j in range(0,no_of_eng_words):
        if len(anchor1[j]) == 1:
            temp = anchor1[j]
        else:
            temp=['0']
        anchor2.append(temp)
        anchor2_str_list.append("".join(temp))
#         print(anchor1[j],"=>", anchor2[j])
    return(anchor2, anchor2_str_list)

def remove_single_hindi_id_in_more_than_one_column(anchor2_str_list):
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





# In[40]:


#$$$ 5

##CREATION OF PYTHON DICTS and LISTS FROM NECESSARY FILES, csv,sys,os
try:   
    h2w = create_dict(hfilename, '(H_wordid-word')
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
    print("FILE MISSING: " + nandani_mapping )
    log.write("FILE MISSING: " + nandani_mapping + "\n")

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
    #     print(e2w)
    show_eng ={}    
    for k,v in e2w.items():
        show_eng[k] = str(k)+"_"+v
    #     print(show_eng)
    eng = [show_eng[i] for i in sorted(show_eng.keys())]
#     print(show_eng.values(), type(show_eng.values()))
    title=["0"]+list(show_eng.values())#.insert(0,'0')

        
except:
    print("FILE MISSING: " + efilename )
    log.write("FILE MISSING: " + efilename+ "\n")
    command = "awk '{printf $3}' "+efilename_alternate
    print(command)
    x=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True).stdout.read()
#     x1 = x.decode(encoding="utf-8", errors="strict")
    x1=x.decode("utf-8") 
    x2 = x1.split(")")
    while "" in x2:
        x2.remove("")
    print(x2, len(x2), type(x2))
    title=["0"] + list(x2[:-1])
    print(type(title))
    print(title, len(title), no_of_eng_words)
    print(dfs.shape)
#     print("===>",x,"\n", str(x))    

try:
    tranliterate_dict={}
    transliterate_mapping = get_E_H_dict_Ids(roja_transliterate_file)  
except:
    print("FILE MISSING: " + roja_transliterate_file )
    log.write("FILE MISSING: " + roja_transliterate_file + "\n")

# display(dfs)
dictionary_wordnet = list(dfs.iloc[5])
hindi_wordnet = list(dfs.iloc[8])
partial_match = list(dfs.iloc[12])
print(dictionary_wordnet)
print(hindi_wordnet)
print(partial_match)
dfs.drop(9, inplace=True)
dfs.drop(6, inplace=True)
dfs.drop(13, inplace=True)
# print(hindi_wordnet)
# print(partial_match)
dfs



# In[41]:


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
                    print( title[i], "==>", id_to_IDSTR_on_string(x[i]))
                    f.write(" ".join([title[i], "==>", id_to_IDSTR_on_string(x[i]),"\n"]))
        f.write("===============\n")
        print("======")

create_debug_file_for_layer(dictionary_wordnet,"dictionary_match_debug.txt")
create_debug_file_for_layer(hindi_wordnet,"hindi_wordnet_debug.txt")
create_debug_file_for_layer(partial_match,"partial_match_debug.txt")


# In[42]:


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
print(k_layer_ids)
k_layer_partial_ids= load_row_from_csv(k_layer_ids_file, 2)
k_layer_partial_ids = cleaning_list(k_layer_partial_ids)
print(k_layer_partial_ids)

dfs.loc[24] = k_layer_ids
dfs.loc[25] = k_layer_partial_ids




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


# In[43]:


# #remove=========================
# #10 11 12 => [10, 11, 12]
# def create_list_from_space_seperated_string(string):
#     if " " not in string:
#         return([string])
#     return(string.split(" "))

# #[[10,11,12], [12]] => [12]
# def intersection_of_two_list(lst1, lst2): 
#     lst3 = [value for value in lst1 if value in lst2] 
#     return lst3 

# #[[1,2],[11,12],[1],[2]] => [[1],[2],[1,2],[11,12]]
# def sort_list_of_list_by_length(listlist):
    
    

# #10 11 12#12 => 10 11 12
# def merge_overlapping_entries(anchor1):
#     print("***")
#     print(len(anchor1))
#     for i in range(0, len(anchor1)):
#         if len(anchor1[i])>1:
#             print(anchor1[i])
#             all_list_in_cell=[]
#             for item in anchor1[i]:
#                 all_list_in_cell.append(create_list_from_space_seperated_string(item))
#             print(all_list_in_cell)
#     return(anchor1)
    
# print(show_hindi)
# #remove=========================


# In[44]:


#$$$ 7

# Calling function for Union of columns and removing duplicates:
print("====finalrow_in_csv")
final_row_in_csv = union_of_columns_verically(dfs)
final_row_in_csv[0]="Verical Union v1"
print(final_row_in_csv)

print("====anchor1")
anchor1, anchor1_str_list, count_dict_list = remove_duplicates_from_union(final_row_in_csv)
print(anchor1_str_list)
# anchor1_2 = merge_overlapping_entries(anchor1)

anchor1[0] = 'Potential anchors v1' 
anchor1_str_list[0] = 'Potential anchors v1' 

print("====anchor2")
anchor2, anchor2_str_list = remove_multi_entry_in_a_cell(anchor1)
print(anchor2_str_list)

print("====anchor3")
anchor3_str_list = remove_single_hindi_id_in_more_than_one_column(anchor2_str_list)
anchor3_str_list[0]="Starting anchor v1"
print(anchor3_str_list)
dfs.loc[26] = anchor1_str_list
dfs.loc[27] = anchor3_str_list
dfs


# In[45]:


#$$$ 8
#extracting Roja and Nandani Dictionary values and inserting in csv
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
    dfs.loc[28] = roja_transliterate_list
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
    dfs.loc[29] = nandani_mapping_list
except:
    print("FILE MISSING: " + nandani_file ) 
    log.write("FILE MISSING: " + nandani_file  + "\n")

dfs


# In[46]:


#$$$ 9
final_row_in_csv = union_of_columns_verically(dfs)
final_row_in_csv[0]="Verical Union v2"
print(final_row_in_csv)
anchor1, anchor1_str_list, count_dict_list = remove_duplicates_from_union(final_row_in_csv)
anchor1[0] = 'Potential anchors v2' 
anchor1_str_list[0] = 'Potential anchors v2' 
print(anchor1_str_list)
anchor2, anchor2_str_list = remove_multi_entry_in_a_cell(anchor1)
print(anchor2_str_list)
anchor3_str_list = remove_single_hindi_id_in_more_than_one_column(anchor2_str_list)
anchor3_str_list[0]="Starting anchor v2"
print(anchor3_str_list)
dfs.loc[30] = anchor1_str_list
dfs.loc[31] = anchor3_str_list


dfs.loc[32] = dictionary_wordnet
dfs.loc[33] = hindi_wordnet  
dfs.loc[34] = partial_match

dfs.to_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_2.csv", index=False)
dfs.to_html(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_2.html", index=False)
dfs


# In[47]:


#$$$ 10

pd.options.display.max_columns = None
pd.set_option('display.max_colwidth',-1)
potentialv1 = dfs.loc[26].to_list()
new_dfs = pd.DataFrame([potentialv1])

# try:
#     startingv1 = dfs.loc[27].to_list()
# #     print(startingv1)
#     startingv1_words = replace_id_by_id_word_pair_for_visualization(startingv1)
# #     print(unique_words)
#     new_dfs = new_dfs.append(pd.Series(startingv1_words, index=new_dfs.columns ), ignore_index=True)

# except:
#     print("Starting anchor v2 has no results")
#     log.write("Starting anchor v2 has no results to write in short"  + "\n")


# try:
#     roja = dfs.loc[28].to_list()
# #     print(roja)
#     roja_words = replace_id_by_id_word_pair_for_visualization(roja)
# #     print(roja_words)
#     new_dfs = new_dfs.append(pd.Series(roja_words, index=new_dfs.columns ), ignore_index=True)

# except:
#     print("Roja transliterate has no results")
#     log.write("Roja transliterate has no results to write in short"  + "\n")

# try:
#     nandani = dfs.loc[29].to_list()
# #     print(nandani)
#     nandani_words = replace_id_by_id_word_pair_for_visualization(nandani)
# #     print(nandani_words)
#     new_dfs = new_dfs.append(pd.Series(nandani_words, index=new_dfs.columns ), ignore_index=True)

# except:
#     print("Nandani transliterate has no results")
#     log.write("Roja transliterate has no results to write in short"  + "\n")
    
# potentialv2 = dfs.loc[30].to_list()
# new_dfs = new_dfs.append(pd.Series(potentialv2, index=new_dfs.columns ), ignore_index=True)


# try:
#     startingv2 = dfs.loc[31].to_list()
# #     print(startingv2)
#     startingv2_words = replace_id_by_id_word_pair_for_visualization(startingv2)
# #     print(startingv2_words)
#     new_dfs = new_dfs.append(pd.Series(startingv2_words, index=new_dfs.columns ), ignore_index=True)

# except:
#     print("Starting anchor v2 has no results")
#     log.write("Roja transliterate has no results to write in short" + "\n")
# print(title)
# new_dfs.columns =title
# hindi_row = "  ,  ".join(hindi_word) #+ ['.'] * (new_dfs.shape[1]-1)


# # new_dfs = new_dfs.append(pd.Series(hindi_row, index=new_dfs.columns ), ignore_index=True)

# new_dfs.to_csv(path_tmp +"/short.csv", index=False)
# new_dfs.to_html(path_tmp + '/short.html')

# new_dfs



# In[48]:


log.close()


# In[49]:



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
new.columns =title
new.index = np.arange(1,len(dfs)+1)
new = new.set_index('0')
new


# In[62]:




def write_to_html_file(df, filename=''):
    '''
    Write an entire dataframe to an HTML file with nice formatting.
    '''

    result = '''
<html>
<head>
<style>
h3{
text-align: center;
}
</style>
		<meta charset="UTF-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"> 
		<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
		<title>Anusaaraka Output</title>
		<link rel="stylesheet" type="text/css" href="../styles/css/normalize.css" />
		<link rel="stylesheet" type="text/css" href="../styles/css/demo.css" />
		<link rel="stylesheet" type="text/css" href="../styles/css/component.css" />
        
        		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
		<script src="http://cdnjs.cloudflare.com/ajax/libs/jquery-throttle-debounce/1.1/jquery.ba-throttle-debounce.min.js"></script>
		<script src="../styles/js/jquery.stickyheader.js"></script>

</head>
<body>
    '''
    result += '<h3> Sentence Number: %s </h3>\n<hr>' % sent_no
    result += '<h3> %s </h3>\n<hr>' % es
    result += '<h3> %s </h3>\n' % hs
    result += '<h3> %s </h3>\n' % hindi_row
    result += df.to_html(classes='wide', escape=False)
    result += '<center> <img src="{0}"> <hr> <img src="{1}"> <hr> </center>' .format(eimg,himg)
#     result += '<center><iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfoXq6rT-vfEl1eUU0-dVBbe5fajs5THxaatO2sxGg1YUx-vA/viewform?embedded=true" width="640" height="879" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe></center>'
    result += '''

</body>
</html>
'''
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(result)
        
write_to_html_file(new, path_tmp+'/final.html')
new.to_csv(path_tmp +'/final.csv')
# new.to_html(path_tmp +'/final.html')


# In[ ]:





# In[ ]:




