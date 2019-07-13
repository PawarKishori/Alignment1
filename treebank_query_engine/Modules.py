import re
from wxconv import WXC
import pandas as pd
import numpy as np
from anytree.importer import JsonImporter
from anytree import (RenderTree, ContRoundStyle)
from anytree.exporter import DotExporter
from IPython.display import Image

#Function to create dataframe
def create_dataframe(parse, path, filename):
	count = 0
	error_flag = 0
	df= pd.read_csv(parse, sep='\t',names=['PID','WORD','1-','POS','2-','3-','PIDWITH','RELATION','4-','5-'], index_col=False)
	print(df)
	df.index = np.arange(1,len(df)+1)
	df1= df[['PID','WORD','POS','RELATION','PIDWITH']]
	relation_df =  pd.concat([df1.PID, df1.WORD,df1.POS, df1.RELATION, df1.PIDWITH], axis=1)
	for i in range(len(relation_df)):
		if relation_df.iloc[i]['RELATION'] == 'root':
			count = count+1
	if count != 1:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tMore than 1 tree\n')
		f.close()
	return ([relation_df, error_flag])

#Function to convert PID to WID and update corresponding Parent ID's
def data_PID_PIDWITH_mod(relation_df, dflen, path, filename):
	error_flag = 0
	list1 = relation_df.PID
	k = 1
	for i in range(1, dflen):
		try:
			list1[i]
			relation_df.at[i,'PID'] = k
			k = k+1
		except:
			print('')
	for i in range(1, dflen):
		try:
			list1[i]
			relation_df.PIDWITH[i] = relation_df.at[relation_df.PIDWITH[i], 'PID']
		except:
			print('')
	for i in relation_df.index:
		if relation_df.PIDWITH[i] > len(relation_df):
			error_flag = 1
			f = open(path+'/H_log.dat', 'a+')
			f.write(filename +'\tPIDWITH assignment error\n')
			f.close()
			break
	return([relation_df, error_flag])

#Function to create Dictionary
def create_dict(relation_df):
	sub_tree={}
	cid = relation_df['PID'].tolist()
	hid = relation_df['PIDWITH'].tolist()
	rel = relation_df['RELATION'].tolist()
	word = relation_df['WORD'].tolist()
	for h,c,r,w in zip(hid, cid, rel, word):
		if h in sub_tree:
			sub_tree[h].append([c,r,h,w])
		else:
			sub_tree[h] = [[c,r,h,w]]
	return(sub_tree)

#Function to get json format
def form_final_json_tree(relation_df, node, sub_tree, clause):
	if node == 0:
		clause.append('{\n"name": "'+str(node)+'_root'+'",\n"children": [')
	else:
		for i in relation_df.index:
			if relation_df.PID[i] == node:
				clause.append('{\n"name": "'+str(node)+'_'+relation_df.UTF_hindi[i]+'_'+relation_df.RELATION[i]+'",\n"children": [')
	if node in sub_tree:
		for i in sub_tree[node]:
			form_final_json_tree(relation_df, i[0], sub_tree, clause)
	clause.append(']\n}')
	return(clause)

#Function to add a column with words in utf to dataframe
def wx_utf_converter(relation_df):
	a = []
	con = WXC(order='wx2utf', lang = 'hin')
	for i in relation_df.index:
		a.append(con.convert(relation_df.WORD[i]))
	relation_df['UTF_hindi'] = a
	return(relation_df)

#Function to convert a string from wx to utf
def wx_utf_converter_sentence(sentence):
	con = WXC(order='wx2utf', lang = 'hin')
	sentence1 = con.convert(sentence)
	return(sentence1)

#Function to form Word-ID to Word mappings
def wordid_word_mapping(path_des, relation_df):
	f = open(path_des+'/H_wordid-word_mapping.dat','w+')
	for i in relation_df.index:
		f.write("(H_wordid-word\t"+str(relation_df.PID[i])+"\t"+str(relation_df.WORD[i])+")\n")
	f.close()

#Function to form Parser-ID to Word-ID mappings
def parserid_wordid_mapping(path_des, relation_df):
	f = open(path_des+'/H_parserid-wordid_mapping.dat','w+')
	for i in relation_df.index:
		f.write("(H_parserid-wordid\tP"+str(i)+"\t"+str(relation_df.PID[i])+")\n")
	f.close()

#Function to save punctuation information
def punct_info(path_des, relation_df, relation_old_df, path, filename):
	try:
		error_flag = 0
		f = open(path_des+'/H_sentence')
		sentence = f.readline()
		space_separate = re.split(r' ',sentence)
		space_separate[-1] = space_separate[-1].rstrip()
		f.close()
		f = open(path_des+'/H_punct_info.dat','w+')
		hindi_punct=['_','_',"'","!",'"',"#","$","%","&","'","(",")",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","|","}","~","'"]
		list5 = []
		n = len(space_separate)
		i = 0
		while i < n:
			if space_separate[i] in hindi_punct:
				list5.append(space_separate[i])
				space_separate.pop(i)
				n = n-1
			i = i+1
		for k in range(1, len(relation_old_df)+1):
			if relation_old_df.WORD[k] in list5:
				j = relation_old_df.PID[k-1]
				f.write("(H_punc-pos-ID\t"+relation_old_df.WORD[k]+"\t"+'M\t'+str(relation_df.PID[j])+"\t"+str(relation_df.PID[j]+1)+')\n')
		for i in range(1, len(relation_old_df)+1):
			if relation_old_df.POS[i] == "PUNCT" and relation_old_df.WORD[i] not in list5:
				word = relation_old_df.WORD[i]
				j = relation_old_df.PID[i-1]
				if word == space_separate[relation_df.PID[j]-1][-1]:
					f.write("(H_punc-pos-ID\t"+relation_old_df.WORD[i]+"\t"+'R\t'+str(relation_df.PID[j])+')\n')
				else:
					f.write("(H_punc-pos-ID\t"+relation_old_df.WORD[i]+"\t"+'L\t'+str(relation_df.PID[j])+')\n')
		f.close()
		return(error_flag)
	except:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tRequired files not present-1\n')
		f.close()
		return(error_flag)

#Function to draw tree
def drawtree(string, path_des, path, filename):
	try:
		error_flag = 0
		importer = JsonImporter()
		root = importer.import_(string)
		print(RenderTree(root, style=ContRoundStyle()))
		DotExporter(root).to_picture(path_des+filename)
		Image(filename=path_des+filename)
		return(error_flag)
	except:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tInvalid JSON format\n')
		f.close()
		return(error_flag)

#Function to print tree tree in single line
def DFS(node, sub_tree, relation_df, clause):
	if node == 0:
		clause.append('(root')
		clause.append('(')
	else:
		for j in relation_df.index:
			if relation_df.PID[j] == node:
				clause.append(relation_df.UTF_hindi[j])
				clause.append('(')
	if node in sub_tree:
		for i in sub_tree[node]:
			DFS(i[0], sub_tree, relation_df, clause)
	clause.append(')')
	return(clause)

#Function to find BFS of tree
def BFS(relation_df, sub_tree):
	stack = [[0, 'root', '-', 'root']]
	n = 0
	while n < len(relation_df)+1:
		i = stack[n][0]
		if i in sub_tree:
			for j in sub_tree[i]:
				stack.append(j)
		n = n+1
	return(stack)

#Function to resolve conj-cc error
def conj_cc_resolution(relation_df, stack, sub_tree, path, filename):
	conjunctions = ['Ora']
	solo_conj = ['jabaki', 'lekina']
	try:
		f = open(path+'/cc_list', 'r+')
		list_of_cc = list(f)
		f.close()
	except:
		list_of_cc = []
	for i in range(0, len(list_of_cc)):
		list_of_cc[i] = list_of_cc[i].rstrip()
	mod = 0
	conj = 1
	f = open(path+'/cc_errors_log.dat', 'a+')
	i = -1
	while i < len(stack)-1:
		i = i+1
		if stack[i][1] == 'conj':
			conj = 1
			cc = 0
			if stack[i][0] in sub_tree:
				for j in sub_tree[stack[i][0]]:
					if j[1] =='cc':
						if j[3] not in list_of_cc:
							list_of_cc.append(j[3])
						if cc == 0:
							cc = 1
							g_child = j[0]
						else:
							cc = 2
							mod = 0
							f.write(filename+'\tconj exists with more than 1 cc\n')
							break
			else:
				cc = 0
			if cc == 0:
				continue
			elif cc == 2:
				break
			else:
				for j in sub_tree[stack[i][2]]:
					if stack[i][0] != j[0] and j[1] == 'conj':
						if j[0] in sub_tree:
							for k in sub_tree[j[0]]:
								if k[1] == 'cc':
									if k[3] not in list_of_cc:
										list_of_cc.append(k[3])
									conj = 0
									mod = 0
									f.write(filename+'\tconj in parallel with both having cc\n')
									break
					if conj == 0:
						break
			if conj == 0:
				break
			else:
				parent = stack[i][2]
				child = stack[i][0]
				mod = 1
				for j in stack:
					if j[0] == parent:
						g_parent = j[2]
						g_rel = j[1]
					if j[0] == g_child:
						if j[3] in conjunctions:
							rel = 'conjunction'
						else:
							rel = 'disjunction'
				for j in stack:
					if j[0] == g_child:
						sub_tree[j[2]].remove(j)
						j[2] = g_parent
						j[1] = g_rel
						sub_tree[g_parent].append(j)
					if j[0] == parent or j[0] == child or (j[2] == parent and j[1] == 'conj'):
						sub_tree[j[2]].remove(j)
						j[2] = g_child
						j[1] = rel
						if g_child in sub_tree:
							sub_tree[g_child].append(j)
						else:
							sub_tree[g_child] = [j]
				sub_tree1 = {}
				for i in sub_tree:
					if len(sub_tree[i]) != 0:
						sub_tree1[i] = sub_tree[i]
				sub_tree = sub_tree1
				i = -1
				stack = BFS(relation_df, sub_tree)
	for i in stack:
		if i[1] == 'cc':
			if i[3] not in list_of_cc:
				list_of_cc.append(i[3])
				if i[3] not in solo_conj:
					for j in stack:
						if j[0] == i[2] and j[1] != 'conj':
							f.write(filename+'\t'+i[3]+' cannot ocur without conj\n')
							mod = 0
							break
	if mod == 1:
		f.write(str(filename)+'\tconj-cc correction made\n')
		for i in sub_tree:
			sub_tree[i].sort()
			for j in sub_tree[i]:
				for k in relation_df.index:
					if relation_df.PID[k] == j[0]:
						relation_df.at[k, 'RELATION'] = j[1]
						relation_df.at[k, 'PIDWITH'] = j[2]
	else:
		sub_tree = create_dict(relation_df)
	f.close()
	f = open(path+'/cc_list', 'w+')
	for i in range(0, len(list_of_cc)):
		f.write(list_of_cc[i]+'\n')
	f.close()
	return([relation_df, stack, sub_tree])

def obl_err(relation_df, sub_tree, path, filename):
	path_vib ="/home/kailash/n_tree-master/vibhakti"
	f1 = open(path_vib)
	vib = list(f1)
	for i in range(0, len(vib)):
		vib[i] = vib[i].rstrip()
	new_rel = ""
	no = 0
	fobl = open(path+'/obl_errors_log','a+')
	for i in sorted(sub_tree.keys()):
		for j in range(0, len(sub_tree[i])):
			if sub_tree[i][j][1] == "obl":
				lol = sub_tree[i][j][0]
				w = []
				new_rel = ""
				word1 = ""
				if lol in sub_tree:
					n = 0
					for k in range(0, len(sub_tree[lol])):
						if sub_tree[lol][k][1] == "case" or sub_tree[lol][k][1] == "mark":
							print(sub_tree[lol][k][0])
							word0 = sub_tree[lol][k][0]
							word1 = relation_df.loc[relation_df['PID'] == word0, 'WORD'].iloc[0]
							no = 1
							if relation_df.loc[relation_df['PID'] == word0+1, 'RELATION'].iloc[0] == "case" or relation_df.loc[relation_df['PID'] == word0+1, 'RELATION'].iloc[0] == "mark":
								word1 = relation_df.WORD[relation_df['PID'] == word0].iloc[0] + " " + relation_df.WORD[relation_df['PID'] == word0+1].iloc[0]
								print(word1)
								no = 2
								if relation_df.loc[relation_df['PID'] == word0+2, 'RELATION'].iloc[0] == "case" or relation_df.loc[relation_df['PID'] == word0+2, 'RELATION'].iloc[0] == "mark":
									word1 = relation_df.loc[relation_df['PID'] == word0, 'WORD'].iloc[0] + " " + relation_df.loc[relation_df['PID'] == word0+1, 'WORD'].iloc[0]+ " " + relation_df.loc[relation_df['PID'] == word0+2, 'WORD'].iloc[0]
									no = 3
							if word1 in vib :
								if no == 3:
									word1 = relation_df.loc[relation_df['PID'] == word0, 'WORD'].iloc[0] + "_" + relation_df.loc[relation_df['PID'] == word0+1, 'WORD'].iloc[0]+ "_" + relation_df.loc[relation_df['PID'] == word0+2, 'WORD'].iloc[0]
								elif no == 2:
									word1 = relation_df.loc[relation_df['PID'] == word0, 'WORD'].iloc[0] + "_" + relation_df.loc[relation_df['PID'] == word0+1, 'WORD'].iloc[0]
								w.append(word1)
								w.append("_")
							else:
								w.append("error")
								w.append("_")
						if n!=0:
							break
					if "error" not in w and w != []:
						new_rel = new_rel.join(w)+"sambandhi"
						print(new_rel)
						sub_tree[i][j][1] = new_rel
						relation_df.at[relation_df.loc[relation_df['PID'] == sub_tree[i][j][0]].index[0], 'RELATION'] = new_rel
						fobl.write(filename+'\t'+str(lol)+'\tobl correction made\n')
					if ("error" in w and w != []):
						fobl.write(filename+'\t'+str(lol)+'\tOccuring vibhakti not in list of vibhakti\n')
					if w == []:
						fobl.write(filename+'\t'+str(lol)+'\tobl occurs without case or mark as children\n')
				else:
					fobl.write(filename+'\t'+str(lol)+'\tobl occurs without case or mark as children\n')
	f1.close()
	fobl.close()
	return [relation_df, sub_tree]
