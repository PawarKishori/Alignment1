#!/usr/bin/env python
# coding: utf-8

# In[41]:


# tmp_path = sys.argv[1] + '/'
# file_name = sys.argv[2]

import sys
tmp_path = '/home/kishori/a/tmp_anu_dir/tmp/'
file_name = 'Geo_chap2_E1_detok'


for i in range(1,101):
    sent_id = '2.'+ str(i)
    wid_word = tmp_path + file_name +'_tmp/'+ sent_id +'/E_wid-word.dat'
    grouping_ids = tmp_path + file_name +'_tmp/'+ sent_id +'/E_chunk_ids.dat'
    f = open(wid_word,"r")
    g = open(grouping_ids,"r")
    wid_word_dict = {}
    for line in f.read().splitlines():
        wid = int(line.split("\t")[1])
        word = line.split("\t")[2].split(')')[0]
        wid_word_dict[wid] = word

    with open(tmp_path + file_name + '_tmp/'+ sent_id +"/E_chunk_words.dat", "w") as x:
        try:
            for line in g.read().splitlines():
                new_str = "(chunk_type-name-headword-words"
                unchanged = " ".join(line.strip(")").split(" ")[1:3])
                ids = [int(i) for i in line.strip(")").strip("(").split(" ")[3:]]
                words = [wid_word_dict[i] for i in ids]
                words = " ".join(words)
#                 print( new_str+" "  + unchanged+ " " +words+ ")")
                x.write( new_str+" "  + unchanged+ " " +words+ ")\n")
        except Exception:
                print(sent_id,"===============")
                print(wid_word_dict)
                print("Error in wid-word_dict")
        


# In[ ]:




