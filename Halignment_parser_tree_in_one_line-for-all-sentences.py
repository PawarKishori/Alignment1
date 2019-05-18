#!/usr/bin/env python
# coding: utf-8

# # Import

# In[3]:


from __future__ import print_function
from itertools import groupby
from operator import itemgetter
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
import sys,  writeFact, os, pandas as pd, numpy as np, itertools
import networkx as nx
import matplotlib.pyplot as plt
import AnuLibrary
import os,sys

# In[6]:


for i in range(1,101):
    
    alignment_path = '.'
    tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
    folder_name = tmp_path + sys.argv[1] + '_tmp'
    #folder_name ='/home/kishori/a/tmp_anu_dir/tmp/GeoE01_tmp'
    sent_number = str(i)
    rawFile =  folder_name +'/2.'+sent_number+'/H_sentence'
    which_lang= rawFile.split('/')[-1].split('_')[0]
    parse = folder_name +'/2.'+sent_number+'/hindi_dep_parser_original.dat'
#     parse = folder_name +'/2.'+sent_number+'/E_conll_parse'
    tmpSentPath = folder_name+ '/2.'+sent_number+'/' 
    print("============",sent_number)
#     x = AnuLibrary.create_hindi_facts(parse, rawFile, tmpSentPath, alignment_path)
    try:
        [relation_df, wid_word_list,punctlist,wid_word_dict, item2WriteInFacts, def_lwg_item, all_vib_ids,wid_pid,p_w, wid_pos_list, wid_rel_list,cid_hid, cid_hid_dict]= AnuLibrary.create_hindi_facts(parse, rawFile, tmpSentPath, alignment_path)
#         print(relation_df)
    except Exception:
        print("Old Error/Key error", sent_number)
        continue

# check_relation_df_correct_or_wrong_and_integrate_in_create_hindi_df
    #print(cid_hid_dict)
#     print(wid_word_dict)
    sub_tree = cid_hid_dict


    def find_single_line_tree(node, sub_tree, clause,already_done):
        if node in already_done:
            raise Exception
#         print(node + '(', end = '')
        clause.append(node)
#         clause.append('(')
        if node in sub_tree:
            for i in sub_tree[node]:
                find_single_line_tree(i, sub_tree, clause,already_done+[node])
#         print(')', end = '')
#         clause.append(' ')
#         print(clause)
        return(clause)
    
    
    filename = which_lang + '_clause_v1'
    filename_w = which_lang + '_clause_words_v1'
    filename_template = which_lang + '_clause_template'
    
    g = open(tmpSentPath + filename_template, 'w')
    w = open(tmpSentPath + filename_w, 'w')
    
    try:
        with open(tmpSentPath + filename , 'w') as f:
            clause = []
            for i in wid_word_list:
                clause_list=[];clause_list_word= []; clause_list_string=[]
                #print(str(i[0]), "=> ", end='')
                clause_list = find_single_line_tree(i[0], sub_tree, clause_list,[]) 
#                 clause_list.remove(str(i[0]))
                clause_list.sort()
                clause_list_string = [str(i) for i in clause_list]
                string = " ".join(clause_list_string)
                #print(string)
                f.write('(E_clause_hid-clause_elements\t'+ str(i[0]) + '\t' + string + ')\n')
              
                
                clause_list_word = [wid_word_dict[i] for i in clause_list]
                string_words = ' '.join(clause_list_word)
                #print(string_words)
                w.write('(E_clause_hword-clause_element_words\t'+ wid_word_dict[i[0]] + '\t' + string_words + ')\n')
                g.write('(clause (language hindi) (cl_head_id '+ str(i[0]) +') (cl_head_word '+  wid_word_dict[i[0]] +' ) (cl_element_ids '+ string +') (cl_element_words '+ string_words +'))\n')

    except Exception:
        print(string)
        print(relation_df)
        print(sub_tree)
        print("Error in Recursion in tree", sent_number, Exception)
        continue
    g.close()
    w.close()


# # for i in range(1,101):
# 	alignment_path = '.'
# 	folder_name ='cl_english_100_detok_tmp'
# 	sent_number = str(i)
# 	rawFile =  folder_name +'/2.'+sent_number+'/H_sentence'
# 	which_lang= rawFile.split('/')[-1].split('_')[0]
# 	parse = folder_name +'/2.'+sent_number+'/hindi_dep_parser_original.dat'
# 	tmpSentPath = folder_name+ '/2.'+sent_number+'/' 
# 
# 	x = AnuLibrary.create_hindi_facts(parse, rawFile, tmpSentPath, alignment_path)
# 	[relation_df, wid_word_list,punctlist,wid_word_dict, item2WriteInFacts, def_lwg_item, all_vib_ids,wid_pid,p_w, wid_pos_list, wid_rel_list,cid_hid, cid_hid_dict]= AnuLibrary.create_hindi_facts(parse, rawFile, tmpSentPath, alignment_path)
# 
# 	# check_relation_df_correct_or_wrong_and_integrate_in_create_hindi_df
# 
# 	sub_tree = cid_hid_dict
# 	sub_tree_words = {}
# 
# 	for key, val_list in sub_tree.items():
# 	    new_key = wid_word_dict[int(key)]
# 	    new_values_list = [wid_word_dict [int(i)] for i in val_list]
# 	    sub_tree_words[new_key] = new_values_list
# 
# 	# print(sub_tree)
# 	# sub_tree_words
# 
# 	def find_single_line_tree(node, sub_tree, clause):
# 		print(node + '(', end = '')
# 		clause.append(node)
# 		clause.append('(')
# 		if node in sub_tree:
# 		    for i in sub_tree[node]:
#                 find_single_line_tree(i, sub_tree, clause)
# 		print(')', end = '')
# 		clause.append(') ')
# 		return(clause)
# 	    
# 	    
# 	#change filename, 'root', sub_tree_words => for words and ids
# 
# 	rawFile =  folder_name +'/2.'+sent_number+'/H_sentence'
# 	which_lang= rawFile.split('/')[-1].split('_')[0]
# 	parse = folder_name +'/2.'+sent_number+'/hindi_dep_parser_original.dat'
# 	tmpSentPath = folder_name+ '/2.'+sent_number+'/' 
# 
# 
# 	filename = which_lang+ '_clause_single_line_ids'
# 
# 	with open(tmpSentPath + filename , 'w') as f:
# 	    clause = []
# 	    clause = find_single_line_tree('0', sub_tree, clause)
# 	    string = "".join(clause)
# 	    print(string)
# 	    f.write(string)

# In[ ]:




