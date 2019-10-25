import csv,sys, os
import pandas as pd
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
# eng_file_name = 'ai1E'
# sent_no='2.78'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
sent_dir = tmp_path + eng_file_name + "_tmp/" + sent_no
log_file = sent_dir + "/Deciding_Anchor_sequence.log"
old_csv = sent_dir + "/All_Resources.csv"
log = open(log_file,'a')

##############################################CREATING LOG OBJECT##################################################
if os.path.exists(log_file):
    os.remove(log_file)
log = open(log_file,'a')

#if os.path.exists(old_csv):
#    os.remove(log_file)
#log = open(log_file,'a')



######################################################################################################################
def reading_all_resources():
    try :
        with open(sent_dir+'/All_Resources.csv','rt')as f: 
            data = csv.reader(f)
            rows=list(data)
    except :
        print("All_Resources.csv is Missing")
        log.write("In "+sent_no+" All_resources.csv is missing")
        sys.exit(0)
        
    return rows

#-----------------------------------------------------------------------------------------------------------------
all_resources = reading_all_resources()
#print(all_resources)

######################################################################################################################

'''def resources_for_deciding_potential_anchor():
    anu_exact_match=[]
    nandani_dict=[]
    tech_dict=[]
    roja_transliterate=[]
    kishori_WSD_modulo=[]
    K_exact = []
    K_partial = []
    K_root = []
    K_dict = []
    Eng_ids = all_resources[0]
    K_exact = all_resources[1]
    anu_exact_wo_vib = all_resources[2]
    roja_transliterate = all_resources[3]
    nandani_dict = all_resources[4]
    tech_dict = all_resources[5]
    K_partial = all_resources[6]
    K_dict = all_resources[7]
    kishori_WSD_modulo =all_resources[8]
    K_root = all_resources[9]
    return ([Eng_ids, K_exact,anu_exact_wo_vib, roja_transliterate, nandani_dict, tech_dict, K_partial, K_dict, kishori_WSD_modulo, K_root ])

        
all_rows_list = resources_for_deciding_potential_anchor()'''

###################################################################################################################
# Checking whether all rows has equal number of entries for each english word.
def return_if_all_rows_of_same_length():
    all_rows_list = reading_all_resources()
    #print(nested_list)
    n = len(all_rows_list[0])
    if all(len(x) == n for x in all_rows_list):
        print("ALL ROWS HAVE EQUAL LENGTH")
    else:
        print("ROWS length mismatch")
        sys.exit(0)
        log.write("ROWS length mismatch")
#-----------------------------------------------------------------------------------------------------------------
# Checking whether all rows has equal number of entries for each english word.
return_if_all_rows_of_same_length()
###################################################################################################################
def create_df_from_all_rows_list():
    print(")))))")
    df = pd.DataFrame(all_resources)
    return(df)
#-----------------------------------------------------------------------------------------------------------------
#print(all_rows_list)
df = create_df_from_all_rows_list()
print(df)

###################################################################################################################

def get_number_of_eng_words_and_number_of_resources():
    #print("Dataframe shape: ",df.shape)
    return(df.shape[1]-1, df.shape[0]-1)
#-----------------------------------------------------------------------------------------------------------------
eng_words_count, resource_count = get_number_of_eng_words_and_number_of_resources()
#print("eng_words_count,resource_count=",eng_words_count,resource_count)
eng_ids_list = list(range(0,eng_words_count))
###################################################################################################################

def return_list_of_columns_from_df():
    for label, content in df.items():
        all_columns_list.append(list(content))
    return(all_columns_list)    
#-----------------------------------------------------------------------------------------------------------------
all_columns_list=[]
all_columns_list = return_list_of_columns_from_df()
#print(all_columns_list)

###################################################################################################################

# Called for every column/word entries
def find_first_nonzero_entry_for_a_column_in_csv(l):
    leng = len(l)
    i=0;final=0
    while (i < leng):
       if(l[i]!='0'):
           final = l[i]
           break
       i+=1
    #print("final:",final) 
    return(final)
###################################################################################################################
        
def generate_tmp_row_before_current_and_potential():
    columns_except_label = all_columns_list[1:] 
    for i,val in enumerate(eng_ids_list,1):
        #print(i)
        #print(columns_except_label[val])
        column_list_except_eng_id_label = columns_except_label[val][1:]  
        chosen_entry = find_first_nonzero_entry_for_a_column_in_csv(column_list_except_eng_id_label)
        tmp.append(chosen_entry) 
    return(tmp)
        

#-----------------------------------------------------------------------------------------------------------------
tmp=[]
tmp = generate_tmp_row_before_current_and_potential()
#print(tmp)

###################################################################################################################
def finding_potential_entries():
    #Handling hindi 1 to english multiple entries eg. hindi id 5 in multiple cells in the same row
    dict1 = {}
    tmp_new = []
    for i in tmp:
        new=str(i).split('/')
        tmp_new.append(new)

    for i in tmp_new:
        #print(i)
        for j in i:
            if j not in dict1.keys():
                dict1[j]=1
            else:
                dict1[j]+=1  
    print(dict1)
    
    for i, val in enumerate(tmp,1):
        for v in str(val).split('/'): 
            #print(i,v, dict1[str(v)])
            if (dict1[str(v)]>1) and i not in potential_eng_ids and v!='0':
                potential_eng_ids.append(i)
    #print(potential_eng_ids)

    #Handling eng 1 to hindi multiple entries eg. 6/9 in a cell
    for i, val in enumerate(tmp,1):
        if '/' in str(val):
            #print(i,val)
            potential_eng_ids.append(i) 

    return(potential_eng_ids)

#-----------------------------------------------------------------------------------------------------------------
potential_eng_ids = []
potential_eng_ids = finding_potential_entries()


###################################################################################################################
def current_entries():
    for i,v in enumerate(eng_ids_list,1):
        if i not in potential_eng_ids:
            #print(i)
            current_eng_ids.append(i)
    return current_eng_ids

#-----------------------------------------------------------------------------------------------------------------
current_eng_ids=[]
current_eng_ids = current_entries()

###################################################################################################################
def generate_current_and_potential_from_tmp():
    #print(potential_eng_ids)
    #print(current_eng_ids)

    for i, val in enumerate(tmp,1):
        for eng_id in potential_eng_ids:
            if i == eng_id:
                #print(i,val, eng_id)
                potential[i-1] = val
            
    for i, val in enumerate(tmp,1):
        for eng_id in current_eng_ids:
            if i == eng_id:
                #print(i,val, eng_id)
                current[i-1]=val

    #print(tmp)
    #print(potential)
    #print(current)
    return([potential, current])   
        
#-----------------------------------------------------------------------------------------------------------------
potential = [0]*eng_words_count
current = [0]*eng_words_count

potential, current = generate_current_and_potential_from_tmp()

potential.insert(0,"Potential")
current.insert(0,"Current")
print(potential)
print(current)

#print(len(potential))
#
###################################################################################################################
#generate_current_and_potential_from_tmp()
##################################################################################################################a
with open(sent_dir+'/All_Resources.csv','a')as f1:
        dwrite = csv.writer(f1)  
        dwrite.writerow(potential)
        dwrite.writerow(current)
        #dwrite.writerow(prob_potential_anchor)
