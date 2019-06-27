from __future__ import print_function
import glob,re,Modules, sys, os

#file path and name
#path = input ("Enter path: ")
#path = '/home/kishori/a/tmp_anu_dir/tmp/Geo_chap2_E1_detok_tmp'
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'

path = tmp_path  +sys.argv[1] + '_tmp'
path1 = path+'/*/hindi_dep_parser_original.dat'
files = sorted(glob.glob(path1))
for parse in files:   
	res = re.split(r'/', parse)
	filename = res[-2]
	path_des = path+'/'+filename

	#create dataframe
	relation_df = Modules.create_dataframe(parse)
	dflen = len(relation_df) 
	relation_old_df = relation_df

	#step to remove all records with punctuations
	relation_df = relation_df[~relation_df.POS.str.contains("PUNCT")]
	
	#Calling function to convert PID to WID and assign correct Parent ID's
	Modules.data_PID_PIDWITH_mod(relation_df, dflen)

	#Calling function to create a dictionary
	sub_tree1 = Modules.create_dict(relation_df)

	#Calling wx_to_utf converter
	relation_df = Modules.wx_utf_converter(relation_df)

	#Calling function to create json input string
	with open(path_des+'/H__clause_single_line_words' , 'w') as f:
		clause = []
		clause = Modules.form_final_json_tree(relation_df, 0, sub_tree1, clause)
		n = len(clause)
		for i in range(n-1):
			if clause[i][2] == '}' and clause[i+1][0] == '{':
				clause[i]=']\n},'
		string = "".join(clause)
		f.write(string)

	#Calling functions from Mapping.py to save mappings in wordid-word_mapping.dat and parserid-word_mapping.dat
	Modules.wordid_word_mapping(path_des, relation_df)
	Modules.parserid_wordid_mapping(path_des, relation_df)

	#Calling function to save Punctuation Information
	try:
		Modules.punct_info(path_des, relation_df, relation_old_df)
	except:
		print('Required files not present')

	#Calling function to draw tree
	filename = '/H_tree_initial.png'
	Modules.drawtree(string, path_des, filename)

	#Calling function to store DFS of tree
	try:
		f1 = open(path_des+'/H_sentence')
		clause = []
		clause = Modules.DFS(0, sub_tree1, relation_df, clause)
		f = open(path_des+'/H_DFS.dat', 'w+')
		sentence = f1.readline()
		sentence1 = Modules.wx_utf_converter_sentence(sentence)
		f.write(sentence1+'\n')
		for i in range(0, len(clause)):
			f.write(clause[i])
		f.close()
		f1.close()
	except:
		print('Required file not present')
