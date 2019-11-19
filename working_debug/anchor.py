import csv
import re


'''def cleaning_list(k_layer_ids):
    for n, i in enumerate(k_layer_ids):
        if i == '-': 
            k_layer_ids[n] = '0'
#     for n, i in enumerate(k_layer_ids):
#         if i == '_':
#             k_layer_ids[n] = 0
    return(k_layer_ids)'''


def return_key_from_value(dictionary, value):
    ids_to_return=[]
    for ids, words in dictionary.items(): 
        if str(words) == str(value):
            ids_to_return.append(str(ids))

    ids = "/".join(ids_to_return) 
    return ids

def return_key_from_value_without_case(dictionary, value):
    ids_to_return=[]
    for ids, words in dictionary.items(): 
        if str(words.lower()) == str(value.lower()):
            ids_to_return.append(str(ids))
    if len(ids_to_return) == 1 :
        id_to_return=ids_to_return[0]
    
    ids = "/".join(ids_to_return) 
       
    return ids   

def load_row_from_csv(filename, row_number):
    try:
        with open(filename, newline='') as iris:
            # returning from 2nd row
            return list(csv.reader(iris, delimiter=','))[row_number]
    except FileNotFoundError as e:
        raise e


#=====================================================
#Prashant's and Saumya's grouping information
def extract_from_grouping_ordered_facts(filename):
    with open(filename, "r") as f:
        data = f.read().split("\n")
        while "" in data:
            data.remove("")
        egroups=[]
        for x in data:
            tmp_str = x.split(')')[1].split('ids ')[-1]
            tmp_list = create_list_from_space_seperated_string(tmp_str)
            tmp_list = [int(x) for x in tmp_list]
            egroups.append(tmp_list)
    return(egroups)

#=====================================================
# #10 11 12 => [10, 11, 12]
def create_list_from_space_seperated_string(string):
    if " " not in string:
        return([string])
    return(string.split(" "))

#=====================================================
def grouping_with_border_color_in_dataframe(egroups, lang_dataframe, color):
    
    tmp=[]
    for i in range(0,len(egroups)):
        for j in range(0, len(egroups[i])):
            tmp.append(".{} tbody tr >td:nth-child({}){{\nborder: 10px solid {};\n}}\n".format(lang_dataframe,egroups[i][j],color[i]))
            ecode="".join(tmp)
    return(ecode)
#=====================================================
def extract_row_from_df_as_list_by_column_name_and_cell_value(dfs,col_name, cell_vale):
    x = dfs.loc[dfs[col_name] == cell_vale]
    y=x.values.tolist()[0]
    return(y)
#=====================================================
#Function to extract dictionary from H_wordid-word_mapping.dat
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

#=====================================================

#Changes every cell value[hindi ids] from id to is_word pair
def id_to_word(x):
    show_hindi[0]='0'
#     print(show_hindi)
    col = x.tolist()
    new_col=[];all_series=[];final_cell_value=""

    if '   anu_exact_match  ' in col:
        new_col =[str(i) for i in col]
    else:
        for count, i in enumerate(col,0):
#             print(i, type(i))
            if i == '~':
                final_cell_value = '~'           #converted all int 0 to '0'
                new_col.append(final_cell_value)
                
            elif(i!= '0' and i!=0 ):  #code for those cell values which are neither '0' nor 0.
                i=str(i)           #changed all int to string
                change = i.lstrip().rstrip()
#                 print("===>", change) 
                pchange1 = change.replace('#', ' # ')
                pchange = pchange1.replace('/', ' / ')
#                 print(pchange)
                pchange_list = pchange.split()
#                 print(pchange_list)
                change1=[]
                for item in pchange_list:
                    if item=='#' :  #dont replace # and / with any word.
                        change1.append('#')
                    elif item =='/':
                        change1.append('/')
                    else:
                        if int(item) in show_hindi.keys():  # dict keys are int so typecasting item to int
                            change1.append(show_hindi[int(item)])  #here too typecasting needed
                    
#                 print(change1)
                final_cell_value=" ".join(change1)
                new_col.append(final_cell_value)
            
            
                
            else:
                final_cell_value = '0'           #converted all int 0 to '0'
                new_col.append(final_cell_value)
#         print("=======")        
            
    new_col.append(final_cell_value)
    new_col = new_col[:-1]
    new_x = pd.Series(new_col)
    return(new_x)

#=====================================================
# This function extracts head id and group ids in a dictionary/hash format, from tam_id.dat.
def extract_eng_lwg_dictionary_from_ordered_fact_tam_id(filename):
	hindi_dict_id_root={}
	with open(filename, "r") as f:
		data = f.read().split("\n")
		while "" in data:
			data.remove("")
	hid_gid_dict={}
	for entry in data:
		hid_tam=re.findall("(id-TAM \w+ \w+)",entry)
		if(len(hid_tam)>0):
			hid_tam=re.findall("(id-TAM \w+ \w+)",entry)[0].split(" ")
			#print(hid_tam)
			hid=hid_tam[1]                
			tam=hid_tam[2]
			#print(hid,tam,tam.count('_'), range(int(hid)-tam.count('_'), int(hid)+1))
			#hid_gid_dict[int(hid)]=range(int(hid)-tam.count('_'), int(hid)+1)
			seq=range(int(hid)-tam.count('_'), int(hid)+1)
			str_seq=[str(i) for i in seq]
			hid_gid_dict[hid]=" ".join(str_seq)
	return(hid_gid_dict)
#=====================================================
#This functions writes a key value paired hash into fact format in filename with fact label as factlabel.
def write_dictionary_row_by_row_in_fact_file(dict1, fact_label, filepath):
	with open(filepath, 'w') as f:
		for k,v in dict1.items():
			print('('+fact_label+'\t'+ k + '\t'+v+')\n')
			f.write('('+fact_label+'\t'+ k + '\t'+v+')\n')
#=====================================================

#Cleaning csv rows from H_alignment_parserid.csv
def cleaning_list(k_layer_ids):
    for n, i in enumerate(k_layer_ids):
        if i == '-':
            k_layer_ids[n] = '0'
    return(k_layer_ids)

#Extracting a row from csv file
def load_row_from_csv(filename, row_number):
    try:
        with open(filename, newline='') as iris:
            # returning from 2nd row
            return list(csv.reader(iris, delimiter=','))[row_number]
    except FileNotFoundError as e:
        raise e

