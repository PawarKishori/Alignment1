from __future__ import print_function
import glob,re,E_Modules, os, sys


#file path and name
#tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
#path = tmp_path  +sys.argv[1] + '_tmp'
#path1 = path+'/*/E_conll_parse'


path = input ("Enter path: ")
path1 = path+'/*/E_conll_parse'
files = sorted(glob.glob(path1))
for parse in files:
	print(parse)   
	res = re.split(r'/', parse)
	filename = res[-2]
	path_des = path+'/'+filename

	#create dataframe
	[relation_df, error_flag] = E_Modules.create_dataframe(parse, path, filename)
	if error_flag == 1:
		continue
	dflen = len(relation_df) 
	relation_old_df = relation_df

	#step to remove all records with punctuations
	relation_df = relation_df[~relation_df.POS.str.contains("PUNCT")]

	#Calling function to save Punctuation Information
	len_wid = E_Modules.punct_info(path_des, path, filename)
	if len_wid != len(relation_df):
		f = open(path+'/E_log.dat', 'a+')
		f.write(filename +'\tIncorrect splitting of words\n')
		f.close()
		continue
	
	#Calling function to convert PID to WID and assign correct Parent ID's
	[relation_df, error_flag] = E_Modules.data_PID_PIDWITH_mod(relation_df, dflen, path, filename)
	if error_flag == 1:
		continue

	#Calling function to create a dictionary
	sub_tree = E_Modules.create_dict(relation_df)

	#Calling wx_to_utf converter
	#relation_df = E_Modules.wx_utf_converter(relation_df)

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
	file = '/E_tree_initial.png'
	E_Modules.drawtree(string, path_des, path, file)

	#Calling function to correct obl errors
	# [relation_df, sub_tree] = E_Modules.obl_err(relation_df, sub_tree, path, filename)

	#Calling function to correct cc-conj errors
	stack = E_Modules.BFS(relation_df, sub_tree)
	[relation_df, stack, sub_tree] = E_Modules.conj_cc_resolution(relation_df, stack, sub_tree, path, filename)

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
	file = '/E_tree_corrected.png'
	error_flag = E_Modules.drawtree(string, path_des, path, file)
	if error_flag == 1:
		continue

	# #Calling function to create lwg
	# error_flag = E_Modules.lwg(patE_des, path, filename)

	# #Calling function to update tam and vibakthi details
	# relation_df = E_Modules.tam_and_vib_lwg(error_flag, sub_tree, relation_df, path, patE_des, filename)

	# #Calling function to create a dictionary
	# sub_tree = E_Modules.create_dict(relation_df)

	# #Udpate UTF
	# relation_df = E_Modules.wx_utf_converter(relation_df.iloc[:, 0:-1])
	# print(relation_df)

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

	#Calling functions from Mapping.py to save mappings in wordid-word_mapping.dat and parserid-word_mapping.dat
	E_Modules.wordid_word_mapping(path_des, relation_df)
	E_Modules.parserid_wordid_mapping(path_des, relation_df)

	#Calling function to save Relation Information 
	E_Modules.relation_facts(path_des, relation_df)

	#Calling function to store DFS of tree
	try:
		f1 = open(path_des+'/E_sentence')
		clause = []
		clause = E_Modules.DFS(0, sub_tree, relation_df, clause)
		f = open(path_des+'/E_DFS.dat', 'w+')
		sentence1 = f1.readline()
		f.write(sentence1+'\n')
		for i in range(0, len(clause)):
			f.write(clause[i])
		f.close()
		f1.close()
	except:
			f = open(path+'/E_log.dat', 'a+')
			f.write(filename +'\tRequired files not present-3\n')
			f.close()
