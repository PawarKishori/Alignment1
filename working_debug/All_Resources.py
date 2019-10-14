
# coding: utf-8

# In[345]:


import os, re, sys, csv, string
import anchor
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
# eng_file_name = 'ai1E'
# sent_no = '2.2' #2.29, 2.21, 2.61, 2.14, 2.64
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
path_tmp= tmp_path + eng_file_name + "_tmp"
sent_dir =  tmp_path + eng_file_name + "_tmp/" + sent_no
#------------------------------------------------------------------------------------
hfilename = sent_dir +  '/H_wordid-word_mapping.dat'
efilename = sent_dir + '/E_wordid-word_mapping.dat'
efilename_alternate = sent_dir + '/word.dat'
esent = sent_dir + '/E_sentence'
hsent = sent_dir + '/H_sentence'
hparserid_to_wid = sent_dir + '/H_parserid-wordid_mapping.dat'
nandani_file = sent_dir +  '/corpus_specific_dic_facts_for_one_sent.dat'
roja_transliterate_file = sent_dir +  '/Roja_chk_transliterated_words.dat'
# roja_transliterate_file = path_tmp +  '/results_of_transliteration.dat'
#html_file = path_tmp +'/'+ eng_file_name +'_table1.html'
log_file = sent_dir + '/log_htmltocsv'

k_layer_ids_file= sent_dir + '/H_alignment_parserid-new.csv'

############################################Counting no of Eng Words###############################################
eng=open(efilename,"r").read().strip("\n")
no_of_eng_words=len(eng.split("\n"))
##############################################CREATING LOG OBJECT##################################################
if os.path.exists(log_file):
    os.remove(log_file)
log = open(log_file,'a')


# In[346]:


def lower_e_sentence() :
    with open(esent,"r") as esen :
        edata=esen.read().strip("\n").lower()
        edata=edata.translate(edata.maketrans('', '', string.punctuation))
        return(edata)


# In[347]:


def h_sentence() :
    with open(hsent,"r") as hsen :
        hdata=hsen.read().strip("\n")
        hdata=hdata.translate(hdata.maketrans('', '', string.punctuation))
        return hdata


# In[348]:


########################################convert_words_to_ids_in_list###############################################
def convert_words_to_ids_in_list(listofwords,id_word_dict) :   
    for n, i in enumerate(listofwords):
        for key,values in id_word_dict.items() :
            #print(i,j)
            if "#" not in i :
                if i == values and i != 0:
#                 print(i,key)
                    listofwords[n]=str(key)
            else :
                wordlist=i.split("#")
                if values in wordlist :
                    if any(char.isdigit() for char in listofwords[n]) :
                        listofwords[n]=listofwords[n]+"/"+str(key)
                    else :
                        listofwords[n]=str(key)
    return listofwords


# In[349]:


##############################FUNCTION FOR RETURNING MULTIPLE KEYS FOR VALUES######################################
def return_key_from_value(dictionary, value):
    ids_to_return=[]
    for ids, words in dictionary.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
        if words == value:
            ids_to_return.append(ids)
        if len(ids_to_return) == 1 :
            id_to_return=ids_to_return[0]
            return id_to_return
        
    return ids_to_return


# In[350]:


#######################################ID-WORD PAIR DICTIONARY#####################################################
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


# In[351]:


def creating_h2w_dict():
    h2w=[]
    show_hindi ={}
    try:   
        h2w = create_dict(hfilename, '(H_wordid-word')
#         print(h2w)
        for k,v in h2w.items():
            show_hindi[k] = str(k)+"_"+v
#         print(show_hindi)
        
    except FileNotFoundError:
        print("FILE MISSING: " + hfilename )
        log.write("FILE MISSING: " + hfilename + "\n")
    return h2w,show_hindi
h2w,show_hindi=creating_h2w_dict()


# In[352]:


def creating_e2w_dict():
    e2w=[]
    show_eng ={}  
    try:   
        e2w = create_dict(efilename, '(E_wordid-word')
#         print(e2w)
           
        for k,v in e2w.items():
            show_eng[k] = str(k)+"_"+v
#         print(show_hindi)
        
    except FileNotFoundError:
        print("FILE MISSING: " + efilename )
        log.write("FILE MISSING: " + efilename + "\n")
    return e2w,show_eng
e2w,show_eng=creating_e2w_dict()


# In[353]:


#Extract nandani_mapping dictionary[eids to hids] from corpus_specific_dic_facts_for_one_sent.dat
def extract_dictionary_from_deftemplate(filename):
    with open(filename, "r") as f:
        data = f.read().split("\n")
#         print(data)
        while "" in data:
            data.remove("")
        nandini_dict={}
        for line in data:
#             print(line)
            key = line.split(")")[0].lstrip("Edict-Hdict (E_id ")
            val = line.split(")")[2].lstrip("(H_id ")
#             print(key, val)
            nandini_dict[key]=val
    return(nandini_dict)


# In[354]:


def get_E_H_Ids_mfs(filename):
    e_sent=lower_e_sentence()
    h_sent=h_sentence()
    e_pos=[]
    h_pos=[]
    tmp = {}
    with open(filename,'r') as f:
        entries=f.read().strip("\n").split("\n")
        entries = [item.rstrip(")") for item in entries]
#         print(entries)
        for entry in entries:
#             print(entry)
            new_entry = entry.split("\t")
#             print(new_entry)
            ewords = new_entry[1]
            hwords = new_entry[3]
#             print(ewords,hwords)
        if " " in ewords or " " in hwords :
            if ewords in e_sent and hwords in h_sent:
                esearch= e_sent.find(ewords)+1
                hsearch= h_sent.find(hwords)+1
                ewords=ewords.split(" ")
                hwords=hwords.split(" ")
                e_pos.append(esearch)
                h_pos.append(hsearch)
            for pos in range(1,len(ewords)):
                e_pos.append(e_pos[pos-1]+1)
            for pos in range(1,len(hwords)):
                h_pos.append(h_pos[pos-1]+1)
            
            head_in_english = e_pos[-1] 
            #This will change once we will get head id infrmation from english group.
            hindi_group = " ".join([str(i) for i in h_pos])+")"
            tuple_list=[]
            tmp[head_in_english] = hindi_group
            tmp[e_pos[0]] = "(~"
            for i in range(1,len(e_pos)) :
                if i != head_in_english and i != e_pos[0]:
                    tmp[i] = "~"   
        else:
#                 print("one-to-one entry")
#                 print(e2w)
#                 print(ewords)
                eid = return_key_from_value(e2w, ewords)
                hid = return_key_from_value(h2w, hwords)
#                 print(eid)
                final_eids = eid
                final_hids = hid           #IMP
                if final_eids not in tmp:
                    tmp[final_eids] = final_hids

            
           

        #print(tmp)
    return(tmp) 


# In[355]:


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
        #print(tmp)
    return(tmp) 


# In[356]:


##############################################ROW 1################################################################
def A_layer():
    a_layer_ids = anchor.load_row_from_csv(k_layer_ids_file,0)
    a_layer_ids = anchor.cleaning_list(a_layer_ids)  #Not needed but still added
    a_layer_ids[0] = "English_word_ids"
    return a_layer_ids
##############################################ROW 1################################################################
def K_exact_match_Roja():
    
    k_layer_ids= anchor.load_row_from_csv(k_layer_ids_file, 1)
    k_layer_ids = anchor.cleaning_list(k_layer_ids) #assigning Zero at - places
    k_layer_ids[0]= "K_exact_match(Roja)"
    return k_layer_ids


# In[357]:


##############################################ROW 2################################################################
###########################################K_partial_Content_word(Roja)############################################
def K_exact_without_vib_Roja():
    k_exact_wo_vib_ids= anchor.load_row_from_csv(k_layer_ids_file, 2)
    k_exact_wo_vib_ids = anchor.cleaning_list(k_exact_wo_vib_ids)
    k_exact_wo_vib_ids[0]="K_exact_without_vib"
    return k_exact_wo_vib_ids


# In[358]:


##############################################ROW 3################################################################
#################################################K_root_info(Roja)#################################################
def K_partial_Roja():
    k_layer_partial_ids= anchor.load_row_from_csv(k_layer_ids_file, 3)
    k_layer_partial_ids = anchor.cleaning_list(k_layer_partial_ids)
    k_layer_partial_ids[0]="K_partial"
    return k_layer_partial_ids


# In[359]:


##############################################ROW 4################################################################
###############################################K_(Roja)###################################################
def K_root_Roja():
    k_root_ids= anchor.load_row_from_csv(k_layer_ids_file, 4)
    k_root_ids = anchor.cleaning_list(k_root_ids)
    k_root_ids[0]="K_root"
    return(k_root_ids)


# In[360]:


##############################################ROW 5################################################################
###########################################K_(Roja)############################################
def K_dict_Roja():
    k_dict_ids= anchor.load_row_from_csv(k_layer_ids_file, 5)
    k_dit_ids = anchor.cleaning_list(k_dict_ids)
    k_dict_ids[0]="K_dict"
    return(k_dict_ids)


# In[361]:


############################################NANDINI's DICT ROW#####################################################
def Nandani_Dict():
    nandani_mapping_list=[]
    try:
    
#     print(nandani_file)
        data=""
        nandani_mapping = extract_dictionary_from_deftemplate(nandani_file)  
#     print(nandani_mapping)
    # print(nandani_mapping)
        
        for j in range(0,no_of_eng_words+1):
            if str(j) in nandani_mapping.keys():
    #         print(str(j), transliterate_mapping[str(j)])
                nandani_mapping_list.append(nandani_mapping[str(j)])
            else:
    #         print(str(j), '0')
                nandani_mapping_list.append('0')

       
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
        
    except :
        nandani_mapping_list=['0']* (no_of_eng_words+1)
        nandani_mapping_list[0] = 'Nandani dict'
        print("FILE MISSING: " + nandani_file ) 
        log.write("FILE MISSING: " + nandani_file  + "\n")
    return nandani_mapping_list


# In[362]:


def Bharatvani_Dict():
    tech_dict_list=[]
    try:
        tech_dict_filename = sent_dir + '/Tech_dict_lookup.dat'
        tech_dict_dict = get_E_H_Ids_mfs(tech_dict_filename)
#         print(tech_dict_dict)
        for j in range(0,no_of_eng_words+1):
            if j in tech_dict_dict.keys():
            #         print(str(j), transliterate_mapping[str(j)])
                tech_dict_list.append(tech_dict_dict[j])
            else:
                tech_dict_list.append('0')
        tech_dict_list[0] = 'Bharatwani Dict.' 

    except FileNotFoundError:
        tech_dict_list=['0']*(no_of_eng_words+1)
        tech_dict_list[0]='Bharatwani Dict.'
        print("Tech dict not created")
        
    return tech_dict_list


# In[363]:


########################################TRANSLITERATION DICT ROW###################################################
def Transliteration_Dict():
    roja_transliterate_list=[]
    try:
        tranliterate_dict={}
        transliterate_mapping = get_E_H_dict_Ids(roja_transliterate_file)  
    #     print(transliterate_mapping)
       
    
        for j in range(0,no_of_eng_words+1):
            if str(j) in transliterate_mapping.keys():
#             print(str(j), transliterate_mapping[str(j)])
                roja_transliterate_list.append(transliterate_mapping[str(j)])
            
            else:
                roja_transliterate_list.append('0')
        roja_transliterate_list[0] = 'Roja Transliterate'
        
    except :
        roja_transliterate_list=[0]* (no_of_eng_words+1)
        roja_transliterate_list[0] = 'Roja Transliterate'
        print("FILE MISSING: " + roja_transliterate_file )
        log.write("FILE MISSING: " + roja_transliterate_file + "\n")
    return roja_transliterate_list


# In[364]:


############################################KISHORI's DICT ROW#####################################################
def Kishori_exact_match_WSD_modulo():
    dict_new=[] 
    
    try:
        kishori_csv = sent_dir + '/Exact_match_dict.csv'
        dict_new= anchor.load_row_from_csv(kishori_csv, 2)
        dit_new=convert_words_to_ids_in_list(dict_new,h2w)
        dict_new.insert(0,"Kishori_exact_match_WSD_modulo")
#         print(dict_new)
        
    except FileNotFoundError:
        dict_new = ['0'] * (no_of_eng_words+1)
        dict_new[0] = "Kishori_exact_match_WSD_modulo"
        print(kishori_csv +" not found")
        log.write("FILE MISSING: " + kishori_csv  + "\n")
        
    return dict_new


# In[365]:


##########################################INTEGRATION##############################################################

def integrating_all_rows():
        row0=A_layer()
        row1=K_exact_match_Roja()
        row2=K_exact_without_vib_Roja()
        row3=K_partial_Roja()
        row4=K_root_Roja()
        row5=K_dict_Roja()
        row6=Nandani_Dict()
        row7=Bharatvani_Dict()
        row8=Transliteration_Dict()
        row9=Kishori_exact_match_WSD_modulo()
        print(h2w)
        print(e2w)
        print("0 :",row0)
        print("1 :",row1)#De
        print("2 :",row2)
        print("3 :",row3)
        print("4 :",row4)
        print("5 :",row5)
        print("6 :",row6)#
        print("7 :",row7)#
        print("8 :",row8)#
        print("9 :",row9)#
        with open(sent_dir+'/All_Resources.csv', 'w') as csvfile :
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(row0)
            csvwriter.writerow(row1)
            csvwriter.writerow(row2)
            csvwriter.writerow(row3)
            csvwriter.writerow(row4)
            csvwriter.writerow(row5)
            csvwriter.writerow(row6)
            csvwriter.writerow(row7)
            csvwriter.writerow(row8)
            csvwriter.writerow(row9)
integrating_all_rows()

