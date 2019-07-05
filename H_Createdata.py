from __future__ import print_function
import glob,re,H_Modules

#file path and name
path = input ("Enter path: ")
path1 = path+'/*/hindi_dep_parser_original.dat'
files = sorted(glob.glob(path1))

#calling function to clear old log
H_Modules.clear_logs(path)

for parse in files:
	print(parse)
	res = re.split(r'/', parse)
	filename = res[-2]
	path_des = path+'/'+filename

	#Calling function to clear old files
	H_Modules.clear_files(path_des)

	#create dataframe
	[relation_df, error_flag] = H_Modules.create_dataframe(parse, path, filename)
	if error_flag == 1:
		continue
	dflen = len(relation_df) 

	#step to remove all records with punctuations
	relation_df = relation_df[~relation_df.POS.str.contains("PUNCT")]

	#Calling function to get Punctuation Information
	[len_wid, punct_info] = H_Modules.punct_info(path_des, path, filename)
	print(punct_info)
	if len_wid != len(relation_df):
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tIncorrect splitting of words\n')
		f.close()
		f = open(path_des+'/H_log.dat', 'a+')
		f.write('Incorrect splitting of words\n')
		f.close()
		continue

	#Calling function to store punct info
	H_Modules.write_punct_info(path_des, punct_info)
	
	#Calling function to convert PID to WID and assign correct Parent ID's
	[relation_df, error_flag] = H_Modules.data_PID_PIDWITH_mod(relation_df, dflen, path, filename)
	if error_flag == 1:
		continue

	#Calling function to create a dictionary
	sub_tree = H_Modules.create_dict(relation_df)

	#Calling wx_to_utf converter
	relation_df = H_Modules.wx_utf_converter(relation_df)

	#Calling function to create json input string
	with open(path_des+'/H_clause_single_line_words_initial' , 'w+') as f:
		clause = []
		clause = H_Modules.form_final_json_tree(relation_df, 0, sub_tree, clause)
		n = len(clause)
		for i in range(n-1):
			if clause[i][2] == '}' and clause[i+1][0] == '{':
				clause[i]=']\n},'
		string = "".join(clause)
		f.write(string)

	#Calling function to draw tree initial tree
	file = '/H_tree_initial'
	H_Modules.drawtree(string, path_des, path, filename, file)

	#Calling function to correct obl errors
	[relation_df, sub_tree] = H_Modules.obl_err(relation_df, sub_tree, path, filename)

	#Calling function to correct cc-conj errors
	stack = H_Modules.BFS(relation_df, sub_tree)
	[relation_df, stack, sub_tree] = H_Modules.conj_cc_resolution(relation_df, stack, sub_tree, path, filename)

	#Calling function to create json input string
	with open(path_des+'/H_clause_single_line_words_corrected' , 'w+') as f:
		clause = []
		clause = H_Modules.form_final_json_tree(relation_df, 0, sub_tree, clause)
		n = len(clause)
		for i in range(n-1):
			if clause[i][2] == '}' and clause[i+1][0] == '{':
				clause[i]=']\n},'
		string = "".join(clause)
		f.write(string)

	#Calling function to draw tree corrected tree
	file = '/H_tree_corrected'
	error_flag = H_Modules.drawtree(string, path_des, path, filename, file)
	if error_flag == 1:
		continue

	#Calling function to get mappings of wordid-word and parserid-wordid
	wordid_word = H_Modules.wordid_word_mapping(relation_df)
	parserid_wordid = H_Modules.parserid_wordid_mapping(relation_df)

	#calling function to get wordid_word as dict
	wordid_word_dict = H_Modules.wordid_word_dict(wordid_word)
	
	#Calling function to store wordid word mappings
	H_Modules.write_wordid_word(path_des, wordid_word)

	#Calling function to store parserid wordid mappings
	H_Modules.write_parserid_wordid(path_des, parserid_wordid)

	#Calling function to create lwg
	error_flag = H_Modules.lwg(path_des, path, filename)

	#Calling function to update tam and vibakthi details
	relation_df = H_Modules.tam_and_vib_lwg(error_flag, sub_tree, relation_df, path, path_des, filename)

	#Calling function to create a dictionary
	sub_tree = H_Modules.create_dict(relation_df)

	#Udpate UTF
	relation_df = H_Modules.wx_utf_converter(relation_df.iloc[:, 0:-1])

	#Calling function to create json input string
	with open(path_des+'/H_clause_single_line_words_final' , 'w+') as f:
		clause = []
		clause = H_Modules.form_final_json_tree(relation_df, 0, sub_tree, clause)
		n = len(clause)
		for i in range(n-1):
			if clause[i][2] == '}' and clause[i+1][0] == '{':
				clause[i]=']\n},'
		string = "".join(clause)
		f.write(string)

	#Calling function to draw tree final tree
	file = '/H_tree_final'
	error_flag = H_Modules.drawtree(string, path_des, path, filename, file)
	if error_flag == 1:
		continue

	#Calling function to get Relation Information 
	relation_details = H_Modules.relation_facts(relation_df)
	
	#Calling function to store relation details
	H_Modules.write_relation_facts(path_des, relation_details)

	#Calling function to store DFS of tree
	try:
		f1 = open(path_des+'/H_sentence_updated')
		clause = []
		clause = H_Modules.DFS(0, sub_tree, relation_df, clause)
		f = open(path_des+'/H_DFS.dat', 'w+')
		sentence = f1.readline()
		sentence1 = H_Modules.wx_utf_converter_sentence(sentence)
		f.write(sentence1+'\n')
		for i in range(0, len(clause)):
			f.write(clause[i])
		f.close()
		f1.close()
	except:
			f = open(path+'/H_log.dat', 'a+')
			f.write(filename +'\tRequired files not present-2\n')
			f.close()

	#Calling function to create grouping info
	H_Modules.write_groupings(path_des, wordid_word, wordid_word_dict, sub_tree)