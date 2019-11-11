#!/usr/bin/env python
# coding: utf-8

# In[62]:





# In[107]:


import os,csv,sys
multi_align_dict=os.getenv("HOME_alignment")+"/dictionary/Multi_word.txt"
single_align_dict=os.getenv("HOME_alignment")+"/dictionary/Single_word.txt"
#e_corpus = "ai1E"
#sent_no = "2.8"
e_corpus=sys.argv[1]
sent_no=sys.argv[2]
temp_path = os.getenv("HOME_anu_tmp")+"/tmp/"+e_corpus+"_tmp"
sent_dir = temp_path+"/"+sent_no
e_wordid_file = sent_dir+"/E_wordid-word_mapping.dat"
h_wordid_file = sent_dir+"/H_wordid-word_mapping.dat"
csv_file = sent_dir+"/Domain_Specific_Align_Dict.csv"
log_file = temp_path+"/Domain_Specific_Align_Dict.log"
if os.path.exists(log_file):
    os.remove(log_file)
log = open(log_file,'a+')

def Eng_word_id_hash():
    eng_hash={}
    try :
        eng_file_data=open(e_wordid_file,"r").read().strip().split("\n")
        for i in eng_file_data:
            i=i.split("\t")
#             print(i)
            eng_hash[i[1]]=i[2].strip(")")
        return eng_hash
        
    except :
        print(sent_dir+"/H_wordid-word_mapping.dat is missing.")
        log.write(sent_dir+"/H_wordid-word_mapping.dat is missing.")
        sys.exit()
def Hin_word_id_hash():
    hin_hash={}
    try :
        hin_file_data=open(h_wordid_file,"r").read().strip().split("\n")
#         print(hin_file_data)
        for i in hin_file_data:
            i=i.split("\t")
#             print(i)
            hin_hash[i[1]]=i[2].strip(")")
        return hin_hash
    except :
        print(sent_dir+"/H_wordid-word_mapping.dat is missing.")
        log.write(sent_dir+"/H_wordid-word_mapping.dat is missing.")
        sys.exit()
# Hin_word_id_hash()   
def Reading_Alignment_Dictionary():
    single_dic=open(single_align_dict,"r")
    multi_dic=open(multi_align_dict,"r")
    single_dic_data=single_dic.read()
    multi_dic_data=multi_dic.read()
    single_dic_data=single_dic_data.strip().split("\n")
    multi_dic_data=multi_dic_data.strip().split("\n")
    single_e_words = []
    single_h_words = []
    multi_h_words = []
    multi_e_words = []
    for i in single_dic_data : #dic_data
        str1=i.split(' <> ')
        single_e_words+=str1[::2]  #list slicing
        single_h_words+=str1[1::2] #list slicing
    for i in multi_dic_data : #dic_data
        str1=i.split(' <> ')
        multi_e_words+=str1[::2]  #list slicing
        multi_h_words+=str1[1::2]
    return single_e_words,single_h_words,multi_e_words,multi_h_words
single_e_words,single_h_words,multi_e_words,multi_h_words=Reading_Alignment_Dictionary()
eng_hash=Eng_word_id_hash()
hin_hash=Hin_word_id_hash()


def Processing_Single_Words(single_e_words,single_h_words) :
    found_hash= {}
    final_list=[0 for x in range(len(list(eng_hash.values())))]
#     print(final_list)
    for eid, eng in eng_hash.items():
        for edict,hdict in zip(single_e_words,single_h_words):
            if eng.lower() == edict.lower() :
#                 print(eid)
                if final_list[int(eid)-1]== 0 :
                    if hdict in hin_hash.values() :
                        final_list[int(eid)-1]=hdict
    return final_list


def CSV_GENEREATION() :
    row0=list(eng_hash.keys())
    row1=list(eng_hash.values())
    row2=Processing_Single_Words(single_e_words,single_h_words)
    print(row1)
    print(row2)
    with open(csv_file, 'w') as csvfile :
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row0)
        csvwriter.writerow(row1)
        csvwriter.writerow(row2)
CSV_GENEREATION()


# In[ ]:




