import csv, E_Modules

#Check for no or multi-root errors
def multi_root(relation_df, error_flag, path, filename):
	count = 0
	for i in range(len(relation_df)):
		if relation_df.iloc[i]['PID'] == 1:
			count = count + 1
	if count == 0:
		f = open(path+'/E_sanity_log.dat', 'a+')
		f.write(filename+'\tParsed output has no root\n')
		f.close()
		error_flag = 1
	elif count != 1:
		f = open(path+'/E_sanity_log.dat', 'a+')
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
	f = open(path+'/E_sanity_log.dat', 'a+')
	for i in range(0, len(list3)):
		f.write(str(filename)+'\t'+str(list3[i])+'\t'+relation_df.WORD[list3[i]]+'\t'+relation_df.RELATION[list3[i]]+' has children\n')
	f.close()
	if len(list3) != 0:
		error_flag = 1
	return(error_flag)

#Check for relations where the parser has mistagged punctuations
def punct_mistag(relation_df, filename, path):
	error_flag = 0
	f = open(path+'/E_sanity_log.dat', 'a+')
	punct = ['`',"'","'","''",'``','--','`','!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']'    ,'^','_','`','{','|','}','~']
	#punct=['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']
	for i in relation_df.index:
		if relation_df.RELATION[i] != "punct" and relation_df.POS[i] != "PUNCT" and relation_df.WORD[i] in punct:
			error_flag = 1
			f.write(filename+"\t"+relation_df.WORD[i]+"\tPunctuation has been mistagged in sentence\n")
			break
		if relation_df.RELATION[i] == "punct" and relation_df.WORD[i] not in punct:
			error_flag = 1
			f.write(filename+"\t"+relation_df.WORD[i]+"\tWord mistagged as punctuation in sentence\n")
			break	
	return(error_flag)

#Combine sentences if two/more are present in E_sentence
def combine_sentences(relation_df, path_des):
	list1 = []
	total_length = len(relation_df)
	for i in relation_df.index:
		if i != 1:
			temp = relation_df.PID[i-1]
			temp1 = relation_df.PID[i]
			modified_pid = i-1
			if temp > temp1:
				new_len = total_length - temp
				m = i
				for k in range(1, new_len+1):
					if relation_df.PIDWITH[m] != 0:
						relation_df.PIDWITH[m] = relation_df.PIDWITH[m] + modified_pid
					relation_df.PID[m] = m
					m = m+1
	relation_df.to_csv(path_des+'/E_conll_parse_combined_sentences',sep='\t', quoting=csv.QUOTE_NONE, header = False, index = False)
	E_Modules.write_modified_file(path_des, '/E_conll_parse_combined_sentences')
	return(relation_df)
