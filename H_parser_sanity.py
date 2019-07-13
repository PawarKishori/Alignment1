from __future__ import print_function
import glob,re
import pandas as pd
import numpy as np

exception_list = []

#file path and name
path = input ("Enter path: ")
path1 = path+'/2.25/hindi_dep_parser_original.dat'
files = sorted(glob.glob(path1))
for parse in files:
	res = re.split(r'/', parse)
	filename = res[-2]
	path_des = path+'/'+filename

	#Create dataframe
	df = pd.read_csv(parse, sep='\t',names=['PID','WORD','1-','POS','2-','3-','PIDWITH','RELATION','4-','5-'], quoting = 3, index_col = False)
	df.index = np.arange(1,len(df)+1)
	df1 = df[['PID','WORD','POS','RELATION','PIDWITH']]
	relation_df =  pd.concat([df1.PID, df1.WORD,df1.POS, df1.RELATION, df1.PIDWITH], axis=1)
	
	#Check for no or multi-root errors
	def multi_root(relation_df, error_flag):
		count = 0
		for i in range(len(relation_df)):
			if relation_df.iloc[i]['RELATION'] == 'root':
				count = count + 1
		if count == 0:
			f = open(path+'/sanity_log.dat', 'a+')
			f.write(filename+'\tParsed output has no root\n')
			f.close()
			if filename not in exception_list:
				exception_list.append(filename)
				error_flag = 1
		elif count != 1:
			f = open(path+'/sanity_log.dat', 'a+')
			f.write(filename+'\tParsed output has more than 1 root, i.e multiple trees\n')
			f.close()
			if filename not in exception_list:
				exception_list.append(filename)
				error_flag = 1
		return(error_flag)

	#Check for relations that shoudn't have children
	def children_check(relation_df, filename, error_flag):
		list1 = ['punct', 'mark', 'case', 'cc']
		list2 = []
		for i in range(1, len(relation_df)+1):
			if relation_df.RELATION[i] in list1:
				list2.append(relation_df.PID[i])
		list3 = []
		for i in range(1, len(relation_df)+1):
			if relation_df.PIDWITH[i] in list2:
				if relation_df.PIDWITH[i] not in list3:
					list3.append(relation_df.PIDWITH[i])
		f = open(path+'/sanity_log.dat', 'a+')
		for i in range(0, len(list3)):
			f.write(str(filename)+'\t'+str(list3[i])+'\t'+relation_df.WORD[list3[i]]+'\t'+relation_df.RELATION[list3[i]]+' has children\n')
		f.close()
		if len(list3) != 0:
			if filename not in exception_list:
				exception_list.append(filename)
				error_flag = 1
		return(error_flag)

	#Modification cc-conj corrections ASSUMING THAT HINDI PARSER PUTS CC ALWAYS AS CHILD OF CONJ INSTEAD OF AS SIBBLING
	def cc-conj-transformation(relation_df):
		transform_flag = 0
		for i in relation_df.index:
			if relation_df.RELATION[i] == "cc":
				par = relation_df.PIDWITH[i]
				parent_relation = relation_df.loc[relation_df.PID == par, 'RELATION'].iloc[0]
				if parent_relation == "conj":
					grandparent = relation_df.loc[relation_df.PID == par, 'PIDWITH'].iloc[0]
					relation_df.PIDWITH[i] = grandparent
					transform_flag = 1
		return[relation_df, transform_flag]

	# f = open(path_des+'hindi_dep_parser_modi.dat', 'w+')
	# for i in range(len(relation_df)):
	# 	f.write()