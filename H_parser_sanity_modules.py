import csv

#Check for no or multi-root errors
def multi_root(relation_df, error_flag, path, filename):
	count = 0
	for i in range(len(relation_df)):
		if relation_df.iloc[i]['RELATION'] == 'root':
			count = count + 1
	if count == 0:
		f = open(path+'/H_sanity_log.dat', 'a+')
		f.write(filename+'\tParsed output has no root\n')
		f.close()
		error_flag = 1
	elif count != 1:
		f = open(path+'/H_sanity_log.dat', 'a+')
		f.write(filename+'\tParsed output has more than 1 root, i.e multiple trees\n')
		f.close()
		error_flag = 1
	return(error_flag)

#Check for relations that shoudn't have children
def children_check(relation_df, filename, error_flag, path):
    list1 = ['mark', 'case', 'cc']
    list2_0 = []
    list2_1 = []
    for i in relation_df.index:
        if relation_df.RELATION[i] in list1:
            list2_0.append(relation_df.PID[i])
        if relation_df.RELATION[i] == 'punct':
            list2_1.append(relation_df.PID[i])
    list3 = []
    for i in relation_df.index:
        if relation_df.PIDWITH[i] in list2_0:
            if relation_df.PIDWITH[i] not in list3:
                list3.append(relation_df.PIDWITH[i])
        if relation_df.PIDWITH[i] in list2_1 and relation_df.RELATION[i] != "punct":
            if relation_df.PIDWITH[i] not in list3:
                list3.append(relation_df.PIDWITH[i])
    f = open(path+'/H_sanity_log.dat', 'a+')
    for i in range(0, len(list3)):
        f.write(str(filename)+'\t'+str(list3[i])+'\t'+relation_df.WORD[list3[i]]+'\t'+relation_df.RELATION[list3[i]]+' has children\n')
    f.close()
    if len(list3) != 0:
        error_flag = 1
    return(error_flag)

#Modification cc-conj corrections ASSUMING THAT HINDI PARSER PUTS CC ALWAYS AS CHILD OF CONJ INSTEAD OF AS SIBBLING
def cc_conj_transformation(relation_df, path_des):
	transform_flag = 0
	for i in relation_df.index:
		if relation_df.RELATION[i] == "cc":
			par = relation_df.PIDWITH[i]
			parent_relation = relation_df.loc[relation_df.PID == par, 'RELATION'].iloc[0]
			if parent_relation == "conj":
				grandparent = relation_df.loc[relation_df.PID == par, 'PIDWITH'].iloc[0]
				relation_df.PIDWITH[i] = grandparent
				transform_flag = 1
	if transform_flag == 1:
		relation_df.to_csv(path_des+'/hindi_dep_parser_modified',sep='\t', quoting=csv.QUOTE_NONE, header = False, index = False)
	return(relation_df)

def punct_mistag(relation_df, filename, path):
    f = open(path+'/H_sanity_log.dat', 'a+')
    punct=['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']
    for i in relation_df.index:
        if relation_df.RELATION[i] != "punct" and relation_df.POS[i] != "PUNCT" and relation_df.WORD[i] in punct:
            f.write(filename+"\t"+relation_df.WORD[i]+"\tPunctuation has been mistagged in sentence")
            break
        if relation_df.RELATION[i] == "punct" and relation_df.WORD[i] not in punct:
            f.write(filename+"\t"+relation_df.WORD[i]+"\tWord mistagged as punctuation in sentence")
            break