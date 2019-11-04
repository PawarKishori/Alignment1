#Create_potential_and_current_anchors.py


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

def create_df_from_all_rows_list(all_resources):
    df = pd.DataFrame(all_resources)
    return(df)


def generate_tmp_row_before_current_and_potential(all_columns_list,eng_ids_list):
    columns_except_label = all_columns_list[1:]
    for i,val in enumerate(eng_ids_list,1):
        #print(i)
        #print(columns_except_label[val])
        column_list_except_eng_id_label = columns_except_label[val][1:]
        chosen_entry = find_first_nonzero_entry_for_a_column_in_csv(column_list_except_eng_id_label)
        tmp.append(chosen_entry)
    #print(tmp)
    return(tmp)


def return_list_of_columns_from_df(df):
    all_columns_list=[]
    for label, content in df.items():
        all_columns_list.append(list(content))
    return(all_columns_list)


def get_number_of_eng_words_and_number_of_resources(df):
    return(df.shape[1]-1, df.shape[0]-1)

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


def create_dict_from_tmp_row(tmp):
    e2h_dict = {}
    for i, val in enumerate(tmp,1):
         for v in str(val[0]).split('/'):
             if i not in e2h_dict.keys():
                 e2h_dict[i] = [(v,val[1])]
             else:
                 e2h_dict[i].append((v,val[1]))
    return(e2h_dict)

def intersection_of_two_list(lst1, lst2):
    common_element = [value for value in lst1 if value in lst2]
    return common_element
def remove_duplicates(mylist):
    mylist = list(dict.fromkeys(mylist))
    return(mylist)
def create_tmp_from_dict_of_key_val_priority(new_dict):
    print('++++++++++++++++++++++++++++++++++++++++++')
    tmp=[]
    print("new_tmp")
    new_tmp = [x[1] for x in sorted(new_dict.items())]
    final_tmp=[]
    for item in new_tmp:
        if len(item)==1:
            val = item[0][0]
        else:
            t=[]
            for x in item:
                if x[0] != '0':
                    t.append(x[0])
            val = "/".join(t)
        #print(val)
        final_tmp.append(val)
    print(final_tmp)
    print('++++++++++++++++++++++++++++++++++++++++++')
    return(final_tmp)



def compare_two_cells(val, val1):
    val_new=[]
    val1_new=[]
    for v in val:
        to_be_deleted = 0
        for v1 in val1:
            v_list = v[0].split(' ')
            v1_list = v1[0].split(' ')
            #print(v_list, v1_list)
            common = intersection_of_two_list(v_list,v1_list)
            v_new= (v[0],v[1])
            v1_new= (v1[0],v1[1])
            if (len(common) > 0):
               print("candidate")
               #print("----")
               if (v[1]>v1[1]):
                   #v_new = (v[0],v[1])
                   v_new = ('0',0)
               elif (v1[1]<v[1]):
                   #v1_new = (v1[0],v1[1])
                   v1_new = ('0',0)
               else:
                   #[key,val] if len(val) > len(val1) else [key1,val1]
                   if len(val) > len(val1):
                       #v_new = (v[0],v[1])
                       v_new = ('0',0)
                   else:
                       v1_new = ('0',0)
               #print(val_new)
               #print(val1_new)
            val_new.append(v_new)
            val1_new.append(v1_new)
    val_new = remove_duplicates(val_new)
    val1_new = remove_duplicates(val1_new)
    return([val_new, val1_new])



def resolve_overlapping_entries(e2h_dict):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    new_dict={}
    print(e2h_dict)
    keys = list(e2h_dict.keys())
    values = list(e2h_dict.values())
    for i in range(0, len(keys)):
        for j in range(i,len(keys)):
            if keys[i]!=keys[j]:
                print(keys[i], values[i], "=>", keys[j], values[j])
                #compare_two_cells(keys[i], values[i], keys[j], values[j])
                x, y = compare_two_cells( values[i], values[j])
                #print(x)
                #print(y)
                new_dict[keys[i]] = x
                new_dict[keys[j]] = y
    print(new_dict)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return(new_dict)

#----
def finding_potential_entries(tmp):
    #Handling hindi 1 to english multiple entries eg. hindi id 5 in multiple cells in the same row
    dict1 = {}
    #tmp = ['1', '0', '4/7', '5', '5', '0', '8', '9 10 11']
    tmp_new = []
    potential_indexes_in_tmp = []
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
            if (dict1[str(v)]>1) and i not in potential_indexes_in_tmp and v!='0':
                potential_indexes_in_tmp.append(i)
    #print(potential_indexes_in_tmp)

    #Handling eng 1 to hindi multiple entries eg. 6/9 in a cell
    
    #print(tmp)
    for i, val in enumerate(tmp,1):
        if '/' in str(val):
            #print(i,val)
            potential_indexes_in_tmp.append(i) 
    return(potential_indexes_in_tmp)

#----
def current_entries(eng_ids_list, potential_indexes_in_tmp):
    current_indexes_in_tmp=[]
    #print(potential_indexes_in_tmp)
    for i,v in enumerate(eng_ids_list,1):
        #print(i)
        if i not in potential_indexes_in_tmp:
            #print(i)
            current_indexes_in_tmp.append(i)
    return(current_indexes_in_tmp)


def generate_current_and_potential_from_tmp(p_word_index, c_word_index, tmp, eng_words_count):
    #print(p_word_index)
    #print(c_word_index)
    p_index = [int(x)-1 for x in p_word_index ]
    c_index = [int(x)-1 for x in c_word_index ]
    
    #print(p_index)
    #print(c_index)
    
    potential=['0']* eng_words_count
    current = ['0']* eng_words_count
    for i in range(0,len(tmp)):
        for p in p_index:
            if i == p:
                potential[i] = tmp[i] 
    for i in range(0,len(tmp)):
        for c in c_index:
            if i == c:
                current[i] = tmp[i] 
    potential.insert(0,"Potential")
    current.insert(0,"Current")

    return([potential, current])



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
print('-------------------------------------------------')
all_resources = reading_all_resources()
print('-------------------------------------------------')
return_if_all_rows_of_same_length()
print('-------------------------------------------------')
df = create_df_from_all_rows_list(all_resources)
print(df)
print('-------------------------------------------------')
all_columns_list = return_list_of_columns_from_df(df)

print('-------------------------------------------------')
eng_words_count, resource_count = get_number_of_eng_words_and_number_of_resources(df)

eng_ids_list = list(range(0,eng_words_count))


print('-------------------------------------------------')
tmp=[]
tmp = generate_tmp_row_before_current_and_potential(all_columns_list,eng_ids_list)
print(tmp)
tmp_value = [x[0] for x in tmp]
print(tmp_value)
print('-------------------------------------------------')

e2h_dict = create_dict_from_tmp_row(tmp)
print(e2h_dict)
print('-------------------------------------------------')

new_dict = resolve_overlapping_entries(e2h_dict)
print("old_tmp")
print(tmp)
tmp = create_tmp_from_dict_of_key_val_priority(new_dict)
print("after resolving intersecting:",tmp)
print('-------------------------------------------------')

potential_indexes_in_tmp = finding_potential_entries(tmp)
potential_indexes_in_tmp = remove_duplicates(potential_indexes_in_tmp)
print("potential indexes: ",potential_indexes_in_tmp)
print('-------------------------------------------------')
current_indexes_in_tmp = current_entries(eng_ids_list, potential_indexes_in_tmp)
print("current_indexes_in_tmp:", current_indexes_in_tmp)
print('-------------------------------------------------')
potential, current = generate_current_and_potential_from_tmp(potential_indexes_in_tmp, current_indexes_in_tmp,tmp, eng_words_count)
print("potetial:", potential)
print("current:", current)
print('-------------------------------------------------')
with open(sent_dir+'/All_Resources.csv','a')as f1:
        dwrite = csv.writer(f1)
        dwrite.writerow(potential)
        dwrite.writerow(current)




