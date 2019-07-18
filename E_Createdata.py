from __future__ import print_function
import glob,re,E_Modules,csv,E_parser_sanity_modules

#file path and name
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'

path = tmp_path  +sys.argv[1] + '_tmp'
path1 = path+'/*/hindi_dep_parser_original.dat'
files = sorted(glob.glob(path1))

E_Modules.clear_logs(path)

for parse in files:
	print(parse)   
	res = re.split(r'/', parse)
	filename = res[-2]
	path_des = path+'/'+filename

	E_Modules.clear_files(path_des)

	#create dataframe and combine sentences
	[relation_df, error_flag] = E_Modules.create_dataframe(parse, path, filename)
	if error_flag == 1:
		continue
	elif error_flag == 2:
		relation_df = E_parser_sanity_modules.combine_sentences(relation_df, path_des)	
	dflen = len(relation_df) 

	#call apostrophe transformation function
	relation_df = E_Modules.apostrophe_parser_tranformation(relation_df, path_des)

	#Parser sanity check for multiple roots
	error_flag = E_parser_sanity_modules.multi_root(relation_df, error_flag, path, filename)
	if error_flag == 1:
		continue

	#Parser sanity check for punct/ase/mark with children
	error_flag = E_parser_sanity_modules.children_check(relation_df, filename, error_flag, path)
	if error_flag == 1:
		continue

	#Parser sanity check for punctuation mistag
	error_flag = E_parser_sanity_modules.punct_mistag(relation_df, filename, path)
	if error_flag == 1:
		continue

	#step to remove all records with punctuations
	relation_df = E_Modules.remove_punct(relation_df)


	#Calling function to get Punctuation Information
	[len_wid, punct_info] = E_Modules.punct_info(path_des, path, filename)
	if len_wid != len(relation_df):
		f = open(path+'/E_log.dat', 'a+')
		f.write(filename +'\tIncorrect splitting of words\n')
		f.close()
		continue
	
	#Calling function to store punct info
	E_Modules.write_punct_info(path_des, punct_info)

	#Calling function to convert PID to WID and assign correct Parent ID's
	[relation_df, error_flag] = E_Modules.data_PID_PIDWITH_mod(relation_df, dflen, path, filename)
	if error_flag == 1:
		continue

	#Calling function to create a dictionary
	sub_tree = E_Modules.create_dict(relation_df)

	#Calling wx_to_utf converter
	#relation_df = H_Modules.wx_utf_converter(relation_df)

	#Calling function to create json input string
	with open(path_des+'/E_clause_single_line_words_initial' , 'w') as f:
		clause = []
		clause = E_Modules.form_final_json_tree(relation_df, 0, sub_tree, clause)
		n = len(clause)
		for i in range(n-1):
			if clause[i][2] == '}' and clause[i+1][0] == '{':
				clause[i]=']\n},'
		string = "".join(clause)
		f.write(string)

	#Calling function to draw tree initial tree
	file = '/E_tree_initial'

	E_Modules.drawtree(string, path_des, path, filename, file)


	#Calling function to perform while construct transformation
	relation_df = E_Modules.while_semantic(relation_df)

	sub_tree = E_Modules.create_dict(relation_df)

	# #Calling wx_to_utf converter
	# relation_df = H_Modules.wx_utf_converter(relation_df)

	#Calling function to create json input string
	with open(path_des+'/E_clause_single_line_words_initial' , 'w') as f:
		clause = []
		clause = E_Modules.form_final_json_tree(relation_df, 0, sub_tree, clause)
		n = len(clause)
		for i in range(n-1):
			if clause[i][2] == '}' and clause[i+1][0] == '{':
				clause[i]=']\n},'
		string = "".join(clause)
		f.write(string)

	#Calling function to correct obl errors
	#[relation_df, sub_tree] = E_Modules.obl_err(relation_df, sub_tree, path, filename)

	#Calling function to correct cc-conj errors
	stack = E_Modules.BFS(relation_df, sub_tree)
	[relation_df, stack, sub_tree, cc_list] = E_Modules.conj_cc_resolution(relation_df, stack, sub_tree, path, filename)

	#Calling function to create json input string
	with open(path_des+'/E_clause_single_line_words_corrected' , 'w') as f:
		clause = []
		clause = E_Modules.form_final_json_tree(relation_df, 0, sub_tree, clause)
		n = len(clause)
		for i in range(n-1):
			if clause[i][2] == '}' and clause[i+1][0] == '{':
				clause[i]=']\n},'
		string = "".join(clause)
		f.write(string)

	#Calling function to draw tree corrected tree
	file = '/E_tree_corrected'
	error_flag = E_Modules.drawtree(string, path_des, path, filename, file)
	if error_flag == 1:
		continue

	#Calling function to perform cop word transformation
	relation_df = E_Modules.cop_transformation(relation_df,sub_tree, cc_list)
	sub_tree = E_Modules.create_dict(relation_df)


	with open(path_des+'/E_clause_single_line_words_final' , 'w') as f:
		clause = []
		clause = E_Modules.form_final_json_tree(relation_df, 0, sub_tree, clause)
		n = len(clause)
		for i in range(n-1):
			if clause[i][2] == '}' and clause[i+1][0] == '{':
				clause[i]=']\n},'
		string = "".join(clause)
		f.write(string)

	#Calling function to draw tree corrected tree
	file = '/E_tree_final'
	error_flag = E_Modules.drawtree(string, path_des, path, filename, file)
	if error_flag == 1:
		continue


	#Calling function to get mappings in wordid-word and parserid-word
	wordid_word = E_Modules.wordid_word_mapping(relation_df)
	parserid_wordid = E_Modules.parserid_wordid_mapping(relation_df)
	
	#calling function to get wordid_word as dict
	wordid_word_dict = E_Modules.wordid_word_dict(wordid_word)

	#Calling function to store wordid word mappings
	E_Modules.write_wordid_word(path_des, wordid_word)

	#Calling function to store parserid wordid mappings
	E_Modules.write_parserid_wordid(path_des, parserid_wordid)

	# #Calling function to create lwg
	# error_flag = E_Modules.lwg(patE_des, path, filename)

	# #Calling function to update tam and vibakthi details
	# relation_df = E_Modules.tam_and_vib_lwg(error_flag, sub_tree, relation_df, path, patE_des, filename)

	# #Calling function to create a dictionary
	# sub_tree = E_Modules.create_dict(relation_df)

	# #Udpate UTF
	# relation_df = E_Modules.wx_utf_converter(relation_df.iloc[:, 0:-1])

	# #Calling function to create json input string
	# with open(patE_des+'/E_clause_single_line_words_final' , 'w') as f:
	# 	clause = []
	# 	clause = E_Modules.form_final_json_tree(relation_df, 0, sub_tree, clause)
	# 	n = len(clause)
	# 	for i in range(n-1):
	# 		if clause[i][2] == '}' and clause[i+1][0] == '{':
	# 			clause[i]=']\n},'
	# 	string = "".join(clause)
	# 	f.write(string)

	# #Calling function to draw tree final tree
	# file = '/E_tree_final.png'
	# error_flag = E_Modules.drawtree(string, patE_des, path, file)
	# if error_flag == 1:
	# 	continue

	#Calling function to get Relation Information 
	relation_details = E_Modules.relation_facts(relation_df)

	#Calling function to store relation details
	E_Modules.write_relation_facts(path_des, relation_details)

	#Calling function to store DFS of tree
	try:
		f1 = open(path_des+'/E_sentence_updated')
		clause = []
		clause = E_Modules.DFS(0, sub_tree, relation_df, clause)
		f = open(path_des+'/E_DFS.dat', 'w+')
		sentence1 = f1.readline()
		#sentence1 = H_Modules.wx_utf_converter_sentence(sentence)
		f.write(sentence1+'\n')
		for i in range(0, len(clause)):
			f.write(clause[i])
		f.close()
		f1.close()
	except:
			f = open(path+'/E_log.dat', 'a+')
			f.write(filename +'\tRequired files not present-3\n')
			f.close()

	#Calling function to create grouping info
	E_Modules.write_groupings(path_des, wordid_word, wordid_word_dict, sub_tree)