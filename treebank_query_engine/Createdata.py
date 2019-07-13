from __future__ import print_function
import glob,re,Modules
import sys

#file path and name
#path = input ("Enter path: ")
path="."
path1 = path+'/conll/conll_'+sys.argv[1]+'.dat'

files = sorted(glob.glob(path1))
for parse in files:
	print(parse)
	res = re.split(r'/', parse)
	filename = res[-2]
	path_des = path+'/'+'output/'+sys.argv[2]
	print(path_des)

	#create dataframe
	[relation_df, error_flag] = Modules.create_dataframe(parse, path, filename)
	if error_flag == 1:
		continue
	dflen = len(relation_df)
	relation_old_df = relation_df

	#step to remove all records with punctuations
	relation_df = relation_df[~relation_df.POS.str.contains("PUNCT")]

	#Calling function to convert PID to WID and assign correct Parent ID's
	[relation_df, error_flag] = Modules.data_PID_PIDWITH_mod(relation_df, dflen, path, filename)
	if error_flag == 1:
		continue

	#Calling function to create a dictionary
	sub_tree = Modules.create_dict(relation_df)

	#Calling wx_to_utf converter
	relation_df = Modules.wx_utf_converter(relation_df)

	#Calling function to create json input string
	with open(path_des+'/H_clause_single_line_words_initial' , 'w') as f:
		clause = []
		clause = Modules.form_final_json_tree(relation_df, 0, sub_tree, clause)
		n = len(clause)
		for i in range(n-1):
			if clause[i][2] == '}' and clause[i+1][0] == '{':
				clause[i]=']\n},'
		string = "".join(clause)
		f.write(string)

	#Calling function to draw tree initial tree
	file = '/'+sys.argv[1]+'.png'
	Modules.drawtree(string, path_des, path, file)
