import os, re, sys, csv, string
import anchor

#############################################Counting_no_of_Eng_Words#################################################

def lower_e_sentence() :
    with open(esent,"r") as esen :
        edata=esen.read().strip("\n")
        edata=edata.translate(edata.maketrans('', '', string.punctuation))

        return(edata)

def h_sentence() :
    with open(hsent,"r") as hsen :
        hdata=hsen.read().strip("\n")
        hdata=hdata.translate(hdata.maketrans('', '', string.punctuation))

        return hdata

#########################################convert_words_to_ids_in_list#################################################

def convert_words_to_ids_in_list(listofwords,id_word_dict) :   
    for n, i in enumerate(listofwords):
        for key,values in id_word_dict.items() :
            if "#" not in i :
                if i == values and i != 0:
                    listofwords[n]=str(key)
            else :
                wordlist=i.split("#")
                if values in wordlist :
                    if any(char.isdigit() for char in listofwords[n]) :
                        listofwords[n]=listofwords[n]+"/"+str(key)
                    else :
                        listofwords[n]=str(key)

    return listofwords

###############################################ID-WORD_PAIR_DICTIONARY################################################

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

def creating_h2w_dict():
    h2w=[]
    show_hindi ={}

    try:   
        h2w = create_dict(hfilename, '(H_wordid-word')
        
    except FileNotFoundError:
        #print("FILE MISSING: " + hfilename )
        log.write("FILE MISSING: " + hfilename + "\n")
        hin=open(hsent,"r").read().strip("\n")
        hin=hin.translate(hin.maketrans('', '', string.punctuation))
        hin=hin.split(" ")
        h2w = {i+1: hin[i] for i in range(0, len(hin))} 

    return h2w

def creating_e2w_dict():
    e2w=[]
    show_eng ={}  
    try:   
        e2w = create_dict(efilename, '(E_wordid-word')
        e2w=dict((k, v) for k,v in e2w.items())
        
    except FileNotFoundError:
        #print("FILE MISSING: " + efilename )
        log.write("FILE MISSING: " + efilename + "\n")
        eng=open(esent,"r").read().strip("\n")
        eng=eng.translate(eng.maketrans('', '', string.punctuation))
        eng=eng.split(" ")
        e2w = {i+1: eng[i] for i in range(0, len(eng))} 
    
    return e2w

def extract_dictionary_from_deftemplate(filename):
    with open(filename, "r") as f:
        data = f.read().split("\n")
        while "" in data:
            data.remove("")
        nandini_dict={}
        for line in data:
            key = line.split(")")[0].lstrip("Edict-Hdict (E_id ")
            val = line.split(")")[2].lstrip("(H_id ")
            nandini_dict[key]=val

    return(nandini_dict)

def get_E_H_Ids_mfs(filename):
    e_sent=lower_e_sentence()
    h_sent=h_sentence()
    e_pos=[]
    h_pos=[]
    tmp = {}
    with open(filename,'r') as f:
        entries=f.read().strip("\n").split("\n")
        entries = [item.rstrip(")") for item in entries]
        #print(entries)
        for entry in entries:
            new_entry = entry.split("\t")
            ewords = new_entry[1]
            hwords = new_entry[3]
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
            for pos in range(1,len(ewords)):
                e_pos.append(e_pos[pos-1]+1)
            for pos in range(1,len(hwords)):
                h_pos.append(h_pos[pos-1]+1) 
            
            head_in_english = e_pos[-1] 
            hindi_group = " ".join([str(i) for i in h_pos])+")"
            
            tuple_list=[]
            tmp[head_in_english] = hindi_group
            tmp[e_pos[0]] = "(~"
            for i in e_pos :
                if i != head_in_english and i != e_pos[0]:
                    tmp[i] = "~"   
        else:    
                eid =anchor.return_key_from_value(e2w, ewords)
                hid =anchor.return_key_from_value(h2w, hwords)
                final_eids = eid
                final_hids = hid           
                if final_eids not in tmp:
                    tmp[final_eids] = final_hids

    return(tmp) 

def get_E_H_dict_Ids(filename):
    tmp={}
    with open(filename,'r') as f:
        entries=f.read().strip("\n").split("\n")
        entries = [item.rstrip(")") for item in entries]
        for entry in entries:
            eword = entry.split("\t")[1]
            hword = entry.split("\t")[2]
            eid =anchor.return_key_from_value(e2w, eword)
            hid =anchor.return_key_from_value(h2w, hword)
            tmp[str(eid)] = str(hid)

    return(tmp) 


##################################################English_Words_Ids###################################################

def A_layer():
    a_layer_ids = anchor.load_row_from_csv(k_layer_ids_file,0)
    a_layer_ids = anchor.cleaning_list(a_layer_ids)  #Not needed but still added
    a_layer_ids[0] = "English_word_ids"

    return a_layer_ids

##################################################K_Exact_word(Roja)##################################################

def K_exact_match_Roja():
    
    k_layer_ids= anchor.load_row_from_csv(k_layer_ids_file, 1)
    k_layer_ids = anchor.cleaning_list(k_layer_ids) #assigning Zero at - places
    k_layer_ids[0]= "K_exact_match"

    return k_layer_ids

############################################K_partial_Content_word(Roja)##############################################

def K_exact_without_vib_Roja():
    k_exact_wo_vib_ids= anchor.load_row_from_csv(k_layer_ids_file, 2)
    k_exact_wo_vib_ids = anchor.cleaning_list(k_exact_wo_vib_ids)
    k_exact_wo_vib_ids[0]="K_exact_without_vib"

    return k_exact_wo_vib_ids

##################################################K_root_info(Roja)###################################################

def K_partial_Roja():
    k_layer_partial_ids= anchor.load_row_from_csv(k_layer_ids_file, 3)
    k_layer_partial_ids = anchor.cleaning_list(k_layer_partial_ids)
    k_layer_partial_ids[0]="K_partial"

    return k_layer_partial_ids

##################################################K_Tam_Info(Roja)####################################################

def K_TAM_Roja():
    with open(k_tam_file,'r') as csvfile:
        csvfile = csv.reader(csvfile)
        all_rows = list(csvfile)
        k_tam_layer = all_rows[-1]
        for i in range(len(k_tam_layer)):
            if k_tam_layer[i] == '-':
                k_tam_layer[i] = '0'
    return (k_tam_layer[:-1])

#####################################################K_Root(Roja)#####################################################

def K_root_Roja():
    k_root_ids= anchor.load_row_from_csv(k_layer_ids_file, 4)
    k_root_ids = anchor.cleaning_list(k_root_ids)
    k_root_ids[0]="K_root"

    return(k_root_ids)

#####################################################K_Dict(Roja)#####################################################

def K_dict_Roja():
    k_dict_ids= anchor.load_row_from_csv(k_layer_ids_file, 5)
    k_dit_ids = anchor.cleaning_list(k_dict_ids)
    k_dict_ids[0]="K_dict"

    return(k_dict_ids)

############################################DOMAIN_SPECIFIC_ALIGN_DICT_ROW############################################

def Domain_Specific_Alignment_Dict():
    dict_new=[] 
    
    try:
        nupur_csv = sent_dir + '/Domain_Specific_Align_Dict.csv'
        dict_new= anchor.load_row_from_csv(nupur_csv, 2)
        dict_new=convert_words_to_ids_in_list(dict_new,h2w)
        dict_new.insert(0,"Preprocessing")
        
    except FileNotFoundError:
        dict_new = ['0'] * (no_of_eng_words+1)
        dict_new[0] = "Preprocessing"
        log.write("FILE MISSING: " + nupur_csv  + "\n")
        
    return dict_new

###################################################BHARATVANI_DICT####################################################

def Bharatvani_Dict():
    tech_dict_list=[]
    try:
        tech_dict_filename = sent_dir + '/Tech_dict_lookup.dat'
        for j in range(0,no_of_eng_words+1):
            if j in tech_dict_dict.keys():
                tech_dict_list.append(tech_dict_dict[j])
            else:
                tech_dict_list.append('0')
        tech_dict_list[0] = 'Tech Dict' 

    except:
        tech_dict_list=['0']*(no_of_eng_words+1)
        tech_dict_list[0]='Tech Dict'
        
    return tech_dict_list

###############################################TRANSLITERATION_DICT_ROW###############################################

def Transliteration_Dict_old():
    roja_transliterate_list=[]
    try:
        tranliterate_dict={}
        transliterate_mapping = get_E_H_dict_Ids(roja_transliterate_file)  
        for j in range(0,no_of_eng_words+1):
            if str(j) in transliterate_mapping.keys():
                roja_transliterate_list.append(transliterate_mapping[str(j)])
            
            else:
                roja_transliterate_list.append('0')
        roja_transliterate_list[0] = 'Transliterate'
        
    except :
        roja_transliterate_list=[0]* (no_of_eng_words+1)
        roja_transliterate_list[0] = 'Transliterate'
        log.write("FILE MISSING: " + roja_transliterate_file + "\n")

    return roja_transliterate_list


##############################################K_exact_mwe_word_align_csv##############################################

def K_exact_mwe_word_align_csv():
    k_mwe =[]
    try:
        k_mwe_csv_file = sent_dir + '/K_exact_mwe_word_align.csv'
        k_mwe = anchor.load_row_from_csv(k_mwe_csv_file, 0)
        k_mwe = anchor.cleaning_list(k_mwe)                         #
        k_mwe = convert_words_to_ids_in_list(k_mwe, h2w)

    except FileNotFoundError:
        k_mwe = ['0'] * (no_of_eng_words + 1)
        k_mwe[0] = 'K_exact_mwe_word_align.csv'
        log.write("FILE MISSING: " + k_mwe_csv_file + "\n")

    k_mwe[0] = 'K_exact_mwe'

    return k_mwe

##############################################K_1st_letter_capital_word###############################################

def K_1st_letter_capital_word():
    k_prop_list=[]

    try:
        k_prop_csv_file = sent_dir + '/K_1st_letter_capital_word.csv'
        k_prop = anchor.load_row_from_csv(k_prop_csv_file, 0)
        k_prop = anchor.cleaning_list(k_prop)
        k_prop = convert_words_to_ids_in_list(k_prop, h2w)

    except FileNotFoundError:
        k_prop = ['0'] * (no_of_eng_words + 1)
        k_prop[0] = 'K_1st_letter_capital_word'
        log.write("FILE MISSING: " + k_prop_csv_file + "\n")

    return k_prop

##########################################TRANSLITERATION_DICT_ROW####################################################

def Transliteration_Dict():
    roja_transliterate_list=[]

    try:
        transl_csv = sent_dir + '/Transliterate1.csv'
        dict_new= anchor.load_row_from_csv(transl_csv, 2)       
        dict_new=convert_words_to_ids_in_list(dict_new,h2w)
        dict_new.insert(0,"Transliteration")

    except FileNotFoundError:
        dict_new = ['0'] * (no_of_eng_words+1)
        dict_new[0] = "Transliteration"
        log.write("FILE MISSING: " + transl_csv  + "\n")      

    return dict_new

###################################################KISHORI_DICT_ROW###################################################

def Kishori_exact_match_WSD_modulo():
    dict_new=[] 
    
    try:
        kishori_csv = sent_dir + '/Exact_match_dict.csv'
        dict_new= anchor.load_row_from_csv(kishori_csv, 2)
        dict_new= convert_words_to_ids_in_list(dict_new,h2w)
        dict_new.insert(0,"WSD_modulo")
        
    except FileNotFoundError:
        dict_new = ['0'] * (no_of_eng_words+1)
        dict_new[0] = "WSD_modulo"
        log.write("FILE MISSING: " + kishori_csv  + "\n")
        
    return dict_new

######################################################MWE_PP_ROW######################################################

def add_MW_PP_layer():
    if os.path.exists(MW_PP_file):
        with open(MW_PP_file, 'r') as file :
            data = file.readlines()
            print(e2w)
            for i in data:
                ewords = i.split(" <> ")[0].split(" ")
                hwords = i.split(" <> ")[1].strip("\n").split(" ")
                print(ewords)
                print(hwords)
                for i in ewords:
                    eid = anchor.return_key_from_value_without_case(e2w,i)
                    print(eid,i)
                for i in hwords:
                    hid =anchor.return_key_from_value(h2w,i)
                    print(hid,i)

######################################################INTEGRATION#####################################################

def integrating_all_rows():
    try :
        row0 = A_layer()
        row1 = K_exact_match_Roja()
        row2 = K_exact_mwe_word_align_csv() 
        row8 = K_partial_Roja()
        row10 = K_dict_Roja()
        row11 = K_root_Roja()

    except :
        log.write("FILE MISSING: " + k_layer_ids_file + "\n")
        row0=[0]* (no_of_eng_words+1)
        row0[0] = 'English_word_ids'
        row1=[0]* (no_of_eng_words+1)
        row1[0] = 'K_exact_match'
        row2=[0]* (no_of_eng_words+1)
        row2[0] = 'K_exact_without_vib'
        row9=[0]* (no_of_eng_words+1)
        row9[0] = 'K_root'
        row8=[0]* (no_of_eng_words+1)
        row8[0] = 'K_partial'
        row10=[0]* (no_of_eng_words+1)
        row10[0] = 'K_dict'
        row11=[0]* (no_of_eng_words+1)
        row11[0] = 'K_root'

    row1_2 = K_TAM_Roja()
    row3 = K_1st_letter_capital_word()
    row4 = K_exact_without_vib_Roja()
    row5 = Transliteration_Dict_old()
    row6 = Domain_Specific_Alignment_Dict()
    row7 = Bharatvani_Dict()
    row9 = Kishori_exact_match_WSD_modulo()

    print("0 :",row0)
    print("1 :",row1)
    print("2 :",row1_2)
    print("3 :",row2)
    print("4 :",row3)
    print("5 :",row4)
    print("6 :",row5)
    print("7 :",row6)
    print("8 :",row7)
    print("9 :",row8)
    print("10 :",row9)
    print()

    with open(All_resources_filename , 'w') as csvfile :
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row0)
        csvwriter.writerow(row1)
        csvwriter.writerow(row1_2)
        csvwriter.writerow(row2)
        csvwriter.writerow(row3)
        csvwriter.writerow(row4)
        csvwriter.writerow(row5)
        csvwriter.writerow(row6)
        csvwriter.writerow(row7)
        csvwriter.writerow(row8)
        csvwriter.writerow(row9)
        csvwriter.writerow(row10)
        csvwriter.writerow(row11)

#######################################################Set_Path#######################################################

tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
path_tmp= tmp_path + eng_file_name + "_tmp"
sent_dir =  tmp_path + eng_file_name + "_tmp/" + sent_no

######################################################Open_Files######################################################

hfilename = sent_dir +  '/H_wordid-word_mapping.dat'
efilename = sent_dir + '/E_wordid-word_mapping.dat'
efilename_alternate = sent_dir + '/word.dat'
esent = sent_dir + '/E_sentence'
hsent = sent_dir + '/H_sentence'
hparserid_to_wid = sent_dir + '/H_parserid-wordid_mapping.dat'
nandani_file = sent_dir +  '/corpus_specific_dic_facts_for_one_sent.dat'
roja_transliterate_file = sent_dir +  '/Tranliterated_words_first_run.dat'
k_layer_ids_file= sent_dir + '/H_alignment_parserid-new.csv'
All_resources_filename = sent_dir+'/All_Resources.csv'
log_file = sent_dir + '/All_Resources.log'
MW_PP_file  = sent_dir + '/MW_Preprocessing_Output.dat'
k_tam_file = sent_dir + '/K_tam_layer.csv'

#################################################CREATING_LOG_OBJECT##################################################

if os.path.exists(log_file):
    os.remove(log_file)
log = open(log_file,'a')

############################################Deleting_old_All_Resources.csv############################################

if os.path.exists(All_resources_filename):
    os.remove(All_resources_filename)

######################################################################################################################

try :
    eng=open(efilename,"r").read().strip("\n")
    no_of_eng_words=len(eng.split("\n"))

except :
    eng=open(esent,"r").read().strip("\n")
    no_of_eng_words=len(eng.split(" "))

######################################################################################################################

h2w=creating_h2w_dict()

e2w=creating_e2w_dict()

add_MW_PP_layer()

integrating_all_rows()