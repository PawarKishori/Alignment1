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
    #print(n)
    #for i in all_rows_list:
        #print(i)
        #print(len(i), i[0])
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
    i=0;final=0;index=0;chosen_=[]
    while (i < leng):
       if(l[i]!='0'):
           final = l[i]
           index = i
           chosen_ = [final,index]
           break
       i+=1
    if len(chosen_)==0:
        chosen_ = ['0',0]
    #print("final:",final) 
    #print(chosen_)
    return(chosen_)
###################################################################################################################
        
def generate_tmp_row_before_current_and_potential():
    columns_except_label = all_columns_list[1:] 
    for i,val in enumerate(eng_ids_list,1):
        #print(i)
        #print(columns_except_label[val])
        column_list_except_eng_id_label = columns_except_label[val][1:]  
        chosen_entry = find_first_nonzero_entry_for_a_column_in_csv(column_list_except_eng_id_label)
        tmp.append(chosen_entry)
    print(tmp) 
    return(tmp)
        

#-----------------------------------------------------------------------------------------------------------------
tmp=[]
tmp = generate_tmp_row_before_current_and_potential()
#print(tmp)
tmp_value = [x[0] for x in tmp]
#print(tmp_value)

#def check_intersecting_entries(v_list, v1_list):
#    if len(v_list) < len(v1_list) : 
        
def intersection_of_two_list(lst1, lst2): 
    common_element = [value for value in lst1 if value in lst2] 
    return common_element 
 
def set_difference(l1,l2):
       l3 = [x for x in l1 if x not in l2] 
       return l3
def remove_weak_tuple(b,weak_choice):
       to_be_removed=[]
       for i in b:
              if i[0] in weak_choice:
                     to_be_removed.append(i)
       b=set_difference(b, to_be_removed)
       return(b)

import operator
def resolve_overlapping_entries(e2h_dict):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    new_dict={}
    e2h_dict={3: [('4', 0), ('7', 0), ('11', 0)], 6: [('10 11', 2)], 8: [('9 10 11', 0)]}
    print(e2h_dict)
    
    for key, val in e2h_dict.items():
        print(key)
        #print("-",val)
        for key1, val1 in e2h_dict.items():
            if key!=key1:
                print(key, val, "=>", key1, val1)
                new_val=[]; new_val1=[]
                for v in val:
                    to_be_deleted = 0
                    for v1 in val1:
                        print(v[0], "--", v1[0])
                        v_list = v[0].split(' ')
                        v1_list = v1[0].split(' ')
                        #print(v_list, v1_list)
                        common = intersection_of_two_list(v_list,v1_list)
                        if (len(common) > 0): 
                            #vall = val
                            
                            if v[1] == v1[1]:                            # priority is same
                               print("Priority:",v[1],v1[1])
                               print("equal")
                               print("**",key,v[1], key1,v1[1])
                               entries_to_b_deleted_from = [key,val] if len(val) > len(val1) else [key1,val1]   # the entries whose vell contains multiple / is being removed
                               print("))))",entries_to_b_deleted_from)
                               print("--------------------------------")

                                                                                           
                            else:#if v[1] < v1[1]:                             # Highest priority element has choosen
                               print("Priority:",v[1],v1[1])
                               print(v[1],"</>", v1[1])
                               print("**",key,v[1], key1,v1[1])
                               entries_to_b_deleted_from = [key1,val1] if v1[1] > v[1] else [key,val]
                               print("))))",entries_to_b_deleted_from)                                                                                           
                               print("--------------------------------")

                            '''elif v[1] > v1[1]:
                               print("Priority:",v[1],v1[1])
                               print(v[1],">", v1[1])
                               print("**",key,v[1], key1,v1[1])
                               entries_to_b_deleted_from = [key,val] if len(val) > len(val1) else [key1,val1]
                               print("))))",entries_to_b_deleted_from)                                                                                           
                               print("--------------------------------")'''
                                  
                             
                        
                            '''if v[1] < v1[1]:
                                to_be_deleted = key1   
 
                            if v[1] < v1[1]:
                                to_be_deleted = key

                            if v[1] == v1[1]:
                                if len(v_list) < len(v1_list):
                                    to_be_deleted = key1
                                if len(v1_list) < len(v_list):
                                    to_be_deleted = key
                            print(to_be_deleted)
                                                                        
                        new_v =  v

                        if to_be_deleted == key:
                            new_v = '0'
                        if to_be_deleted == key1:
                            new_v = '0'
        
                                
                new_val.append(new_v)   
        print("=>",new_val)                       
        if key not in new_dict.keys():
                            new_dict[key] = [new_val]                         
                        else:
                            new_dict[key].append(new_val)'''
                            
    print(e2h_dict)
    #print(new_dict)                    
                         
                              
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def create_dict_from_tmp_row():
    e2h_dict = {}
    #for i, val in enumerate(tmp_value,1):
    for i, val in enumerate(tmp,1):
         #print(i,val,val[0])
         for v in str(val[0]).split('/'):  
             if i not in e2h_dict.keys():
                 e2h_dict[i] = [(v,val[1])]
             else:
                 e2h_dict[i].append((v,val[1]))
             #find_overlapping_entries(i,v) 
         #print(i,val)
    #print(e2h_dict)
    return(e2h_dict)
print("========== tmp dict:{eng_id1:[(hindi_id2, priority1)], eng_id2: [(hindi_id2,prority2), (hindi_id3, priority1)].....}\n ")
e2h_dict = create_dict_from_tmp_row()
print(e2h_dict)

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
    #print(dict1)
    
    for i, val in enumerate(tmp,1):
        for v in str(val).split('/'): 
            #print(i,v, dict1[str(v)])
            if (dict1[str(v)]>1) and i not in potential_eng_ids and v!='0':
                potential_eng_ids.append(i)
    #print(potential_eng_ids)

    #Handling eng 1 to hindi multiple entries eg. 6/9 in a cell
    resolve_overlapping_entries(e2h_dict) 
    
    '''for i, val in enumerate(tmp,1):
        if '/' in str(val):
            #print(i,val)
            potential_eng_ids.append(i) '''

    
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

    for i, val in enumerate(tmp_value,1):
        for eng_id in potential_eng_ids:
            if i == eng_id:
                #print(i,val, eng_id)
                potential[i-1] = val
            
    for i, val in enumerate(tmp_value,1):
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
