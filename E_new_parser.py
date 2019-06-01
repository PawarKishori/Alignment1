#!/usr/bin/env python
# coding: utf-8

# In[2]:


from __future__ import print_function
from itertools import groupby

import os, pandas as pd
import AnuLibrary, writeFact, tree
from operator import itemgetter
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
import sys,  writeFact, os

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


#     print("End nodes(",len(end_nodes),") :",end_nodes_list)    

for i in range(1,101):
    alignment_path = '.'
    tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
    folder_name = tmp_path + sys.argv[1] + '_tmp'
#    folder_name ='/home/kishori/a/tmp_anu_dir/tmp/'+sys.argv[1]+'_tmp'
#     folder_name ='/home/kishori/a/tmp_anu_dir/tmp/cl_english_100_detok_tmp'
    sent_number = str(i)
    rawFile =  folder_name +'/2.'+sent_number+'/E_sentence'  #change_in_eng
    which_lang= rawFile.split('/')[-1].split('_')[0]
    parse = folder_name +'/2.'+sent_number+'/E_conll_parse' #change_in_eng
    tmpSentPath = folder_name+ '/2.'+sent_number+'/'
    print("============",sent_number)
    
    #with open(alignment_path+"/vibhakti","r") as f:
    #    vibhaktis = f.read().splitlines()
       
    [wid_word_list,punctlist,wid_word_dict]=writeFact.createH_wid_word_and_PunctFact(rawFile) 
   # item2WriteInFacts, def_lwg_item, all_vib_ids = writeFact.lwg_of_postprocessors(wid_word_list,vibhaktis)  
    relation_df = AnuLibrary.create_hindi_dataframe(parse)  
   # print(relation_df) 
#     print(wid_word_list,relation_df['PID'].tolist(),relation_df['WORD'].tolist(),relation_df['POS'].tolist(), relation_df['RELATION'])
    [wid_pid,p_w, wid_pos_list, wid_rel_list]=writeFact.createWID_PID(wid_word_list,relation_df['PID'].tolist(),relation_df['WORD'].tolist(),relation_df['POS'].tolist(), relation_df['RELATION'].tolist())
    writeFact.add(wid_pid,"E_wid-pid",tmpSentPath+"/E_wid-pid")
    writeFact.addLists([relation_df['PID'].tolist(),relation_df['WORD'].tolist()],"E_pid-word",tmpSentPath+"/E_pid-wid.dat")
    writeFact.addLists([relation_df['POS'].tolist(),relation_df['RELATION'].tolist(),relation_df['PID'].tolist(),relation_df['WORD'].tolist(),relation_df['PIDWITH'].tolist()],"E_pos1-relation-pid1-word1-pid2",tmpSentPath+"/E_conll_facts.dat")
#     print(p_w)

    relation_df = writeFact.convertPIDsToWIDs(relation_df)
#     print(relation_df)

    writeFact.addLists([relation_df['POS'].tolist(),relation_df['RELATION'].tolist(),relation_df['PID'].tolist(),relation_df['WORD'].tolist(),relation_df['PIDWITH'].tolist()],"E_pos1-relation-cid-word1-hid",tmpSentPath+"/E_parse.dat")
        
    cid_hid = writeFact.extractUnlabelledDependency(relation_df)
#         tree(relation_df, wid_word_list, cid_hid, wid_pos_list, wid_rel_list, which_language, tmpSentPath, rawFile)
    PID = relation_df['PID'].tolist()
    POS = relation_df['POS'].tolist()
    WORD = relation_df['WORD'].tolist()
    PIDWITH = relation_df['PIDWITH'].tolist()
    RELATION = relation_df['RELATION'].tolist()
    
    filecontent = open(rawFile,"r").read()
    filename = rawFile.split('/')[-1]
    print (color.BOLD + folder_name+"/" + filename,": ", filecontent, end='' + color.END)

#     tree.show_parse_information(relation_df)

    hid_cid = tree.reverse_tuple_list(cid_hid)
    tree.draw_tree(relation_df, hid_cid, which_lang, tmpSentPath)


#     verb = extract_id_of_i_value_from_j_column_list("VERB",POS)
#     all_aux = find_single_AUX(PID,POS)
  


# In[ ]:




