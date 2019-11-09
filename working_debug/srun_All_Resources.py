import os, re, sys, csv, string
import anchor
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
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
roja_transliterate_file = sent_dir +  '/Tranliterated_words_2nd_run.dat'
log_file = sent_dir + '/srun_All_Resources.log'

##############################################CREATING LOG OBJECT##################################################
if os.path.exists(log_file):
    os.remove(log_file)
log = open(log_file,'a')

############################################Counting no of Eng Words###############################################
try :
    eng=open(efilename,"r").read().strip("\n")
    no_of_eng_words=len(eng.split("\n"))
except :
    eng=open(esent,"r").read().strip("\n")
#     print(eng)
    no_of_eng_words=len(eng.split(" "))

# In[346]:


def lower_e_sentence() :
    with open(esent,"r") as esen :
        edata=esen.read().strip("\n")
        edata=edata.translate(edata.maketrans('', '', string.punctuation))
        return(edata)


# In[347]:


def h_sentence() :
    with open(hsent,"r") as hsen :
        hdata=hsen.read().strip("\n")
        hdata=hdata.translate(hdata.maketrans('', '', string.punctuation))
        return hdata




######################################## convert_words_to_ids_in_list ###############################################
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
    for ids, words in dictionary.items(): 
#         print(words,value)# for name, age in dictionary.iteritems():  (for Python 2.x)
        if str(words) == str(value):
#             print("###",ids)
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
        
    except FileNotFoundError:
        print("FILE MISSING: " + hfilename )
        log.write("FILE MISSING: " + hfilename + "\n")
        hin=open(hsent,"r").read().strip("\n")
        hin=hin.translate(hin.maketrans('', '', string.punctuation))
        hin=hin.split(" ")
        h2w = {i+1: hin[i] for i in range(0, len(hin))} 
    return h2w




h2w=creating_h2w_dict()



def creating_e2w_dict():
    e2w=[]
    show_eng ={}  
    try:   
        e2w = create_dict(efilename, '(E_wordid-word')
        e2w=dict((k, v) for k,v in e2w.items())
#         print(e2w)
           
#         for k,v in e2w.items():
#             show_eng[k] = str(k)+"_"+v
#         print(show_hindi)
        
    except FileNotFoundError:
        print("FILE MISSING: " + efilename )
        log.write("FILE MISSING: " + efilename + "\n")
        eng=open(esent,"r").read().strip("\n")
        eng=eng.translate(eng.maketrans('', '', string.punctuation))
        eng=eng.split(" ")
        e2w = {i+1: eng[i] for i in range(0, len(eng))} 
    
#     print(e2w)
    return e2w





e2w=creating_e2w_dict()



def get_E_H_Ids_mfs(filename):
    e_sent=lower_e_sentence()
    h_sent=h_sentence()
    e_pos=[]
    h_pos=[]
    tmp = {}
    with open(filename,'r') as f:
        entries=f.read().strip("\n").split("\n")
        entries = [item.rstrip(")") for item in entries]
        print(entries)
        for entry in entries:
#             print(entry)
            new_entry = entry.split("\t")
#             print(new_entry)
            ewords = new_entry[1]
            hwords = new_entry[3]
#             print(ewords,hwords)
        if " " in ewords or " " in hwords :
            ewords=ewords.split()
            e_len=len(ewords)
            e_sent=e_sent.split()
            for i,sublist in enumerate((e_sent[i:i+e_len] for i in range(len(e_sent)))):
                if ewords==sublist:
                    esearch=i+1
                    e_pos.append(esearch)
            hwords=hwords.split()
            h_len = len(hwords)
            h_sent=h_sent.split()
            for i,sublist in enumerate((h_sent[i:i+h_len] for i in range(len(h_sent)))):
                if hwords==sublist:
                    hsearch=i+1
                    h_pos.append(hsearch)
            #e_pos.append(esearch)
            #h_pos.append(hsearch)
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
            for i in e_pos :
                if i != head_in_english and i != e_pos[0]:
                    tmp[i] = "~"   
        else:
#                 
                eid = return_key_from_value(e2w, ewords)
#                 print(e2w)
#                 print(eid)
                hid = return_key_from_value(h2w, hwords)
#                 print(eid)
                final_eids = eid
                final_hids = hid           #IMP
#                 print(final_hids)
                if final_eids not in tmp:
                    tmp[final_eids] = final_hids
        #print(tmp)
    return(tmp) 


# In[355]:


#created for extracting eid-hid pair corresponding to eword-hword pair of roja_chk_transliteration_out
def get_E_H_dict_Ids(filename):
    tmp={}
    with open(filename,'r') as f:
        #print(f.read())
#         print("====")
#         print(f.read().strip("\n").split("\n"))
        entries=f.read().strip("\n").split("\n")
        entries = [item.rstrip(")") for item in entries]
        #print("=>",entries)

#         print(h2w)
        for entry in entries:
            #print(entry)
            eword = entry.split("\t")[1]
            hword = entry.split("\t")[2]
            #print(eword)
            #print(hword)
            #print(e2w)
            #print(h2w)
            eid = return_key_from_value(e2w, eword)
            print(eid) 
            hid = return_key_from_value(h2w, hword)
#             print(eid, hid)
            tmp[str(eid)] = str(hid)
        #print(tmp)
    return(tmp) 


# In[356]:


##############################################ROW 1################################################################
def A_layer():
    a_layer_ids = anchor.load_row_from_csv(k_layer_ids_file,0)
    a_layer_ids = anchor.cleaning_list(a_layer_ids)  #cleaning Not needed but still added
    a_layer_ids[0] = "English_word_ids"
    return a_layer_ids

########################################TRANSLITERATION DICT ROW###################################################

def Transliteration_Dict_old():
    roja_transliterate_list=[]
    try:
        tranliterate_dict={}
        transliterate_mapping = get_E_H_dict_Ids(roja_transliterate_file)  
        print("==>",transliterate_mapping)
       
    
        for j in range(0,no_of_eng_words+1):
            if str(j) in transliterate_mapping.keys():
#             print(str(j), transliterate_mapping[str(j)])
                roja_transliterate_list.append(transliterate_mapping[str(j)])
            
            else:
                roja_transliterate_list.append('0')
        roja_transliterate_list[0] = 'Transliterate'
        
    except :
        roja_transliterate_list=[0]* (no_of_eng_words+1)
        roja_transliterate_list[0] = 'Transliterate'
        print("FILE MISSING: " + roja_transliterate_file )
        log.write("FILE MISSING: " + roja_transliterate_file + "\n")
    return roja_transliterate_list


##########################################INTEGRATION##############################################################

def integrating_all_rows():

    row = Transliteration_Dict_old()


    with open(sent_dir+'/sun_All_Resources.csv', 'w') as csvfile :
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row0)
        csvwriter.writerow(row)


#def integrate_N2_to_all_rows():
    

with open(sent_dir + '/All_Resources.csv', 'r') as f:
    f = csv.reader(f)
    all_rows = list(f)
    N1_layer = all_rows[-1]


print(all_rows)
print(N1_layer)
integrating_all_rows(all_rows)



