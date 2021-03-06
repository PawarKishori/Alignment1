import re, os
from wxconv import WXC
import pandas as pd
import numpy as np
from anytree.importer import JsonImporter
from anytree import (RenderTree, ContRoundStyle)
from anytree.exporter import DotExporter 
from subprocess import check_call

#Function to get list of vibhakti
def get_vib():
	#HOME_alignment=<path of Alignment1>
	alignment_path=os.getenv('HOME_alignment')
	path_vib = alignment_path + '/vibhakti' #"/home/aishwarya/Aishu_code/n_tree-master/vibhakti"
	f = open(path_vib)
	vib = list(f)
	f.close()
	return(vib)

#Function to delete old log 
def clear_logs(path):
	f = open(path+'/H_log.dat', 'w+')
	f = open(path+'/H_obl_log.dat', 'w+')
	f = open(path+'/H_cc_log.dat', 'w+')
	f = open(path+'/H_tam_vib_log.dat', 'w+')
	f = open(path+'/H_sanity_log.dat', 'w+')
	f = open(path+'/H_vib_check.dat', 'w+')
	f = open(path+'/H_other_vibhaktis', 'w+')
	f.close()

#Function to clear residue files from previous run
def clear_files(path_des):
	f = open(path_des+'/H_grouping_ids.dat', 'w+')
	f = open(path_des+'/H_grouping_words.dat', 'w+')
	f = open(path_des+'/H_grouping_template.dat', 'w+')
	f = open(path_des+'/H_log.dat', 'w+')
	f.close()

def check_if_sentence_file_present(path, path_des, filename):
	try:
		error_flag = 0
		f = open(path_des+'/H_sentence')
		f.close()
	except:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tH_sentence not present\n')
		f.close()
		f = open(path_des+'/H_log.dat', 'a+')
		f.write('\tH_sentence not present\n')
		f.close()
	return(error_flag)

#Function to create dataframe
def create_dataframe(parse, path, filename):
	count = 0
	error_flag = 0
	df = pd.read_csv(parse, sep='\t',names=['PID','WORD','1-','POS','2-','3-','PIDWITH','RELATION','4-','5-'], quoting = 3, index_col = False)
	df.index = np.arange(1,len(df)+1)
	df1 = df[['PID','WORD','POS','RELATION','PIDWITH']]
	relation_df =  pd.concat([df1.PID, df1.WORD,df1.POS, df1.RELATION, df1.PIDWITH], axis=1)
	for i in range(len(relation_df)):
		if relation_df.iloc[i]['PID'] == 1:
			count = count+1
	if type(relation_df.PID[1]) != np.int64:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tTree has non-int PID\n')
		f.close()
		f = open(path+'/'+filename+'/H_log.dat', 'a+')
		f.write('\tTree has non-int PID\n')
		f.close()
	if count != 1:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tMore than 1 tree\n')
		f.close()
		f = open(path+'/'+filename+'/H_log.dat', 'a+')
		f.write('\tMore than 1 tree\n')
		f.close()
	return ([relation_df, error_flag])

def remove_punct(relation_df):
	punct=['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']
	for i in relation_df.index:
		if relation_df.WORD[i] in punct:
			relation_df = relation_df.drop([relation_df.loc[relation_df.index == i].index[0]], axis = 0)
	return(relation_df)

#Function to save punctuation information
def punct_info(path_des, path, filename):
	try:
		punct_info1 = []
		punct=['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']
		f = open(path_des+'/H_sentence')
		space_separate_final = []
		sentence = f.readline()
		space_separate = re.split(r' ',sentence)
		space_separate[-1] = space_separate[-1].rstrip()
		k = 0
		for i in range(0, len(space_separate)):
			if space_separate[i] != '':
				space_separate_final.append(space_separate[i])
		space_separate = space_separate_final
		f2 = open(path_des+"/H_sentence_updated", 'w+')
		for i in range(0, len(space_separate)):
			if i == len(space_separate) - 1:
				f2.write(space_separate[i]+'\n')
			else:
				f2.write(space_separate[i]+' ')
		f2.close()
		for i in range(0, len(space_separate)):
			if space_separate[i] not in punct:
				k = k+1
				right = 0
				left = 0
				middle = 0
			if space_separate[i][-1] in punct:
				right = 1
				word_r = space_separate[i][0:-1]
			if space_separate[i][0] in punct:
				left = 1
				word_l = space_separate[i][1:]
			if space_separate[i] in punct:
				middle = 1
			if middle == 1:
				punct_info1.append([space_separate[i], 'M', k, k+1])
			elif left == 1:
				punct_info1.append([space_separate[i][0], 'L', k, -1])
			elif right == 1:
				punct_info1.append([space_separate[i][-1], 'R', -1, k])
		f.close()
		return([k, punct_info1])
	except:
		k = 0
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tError while writing punct info\n')
		f.close()
		f = open(path_des+'/H_log.dat', 'a+')
		f.write('\tError while writing punct info\n')
		f.close()
		return([k, punct_info1])

#Function to convert PID to WID and update corresponding Parent ID's
def data_PID_PIDWITH_mod(relation_df, dflen, path, filename):
	error_flag = 0
	list1 = relation_df.PID
	k = 1
	for i in range(1, dflen+1):
		try:
			list1[i]
			relation_df.at[i,'PID'] = k
			k = k+1
		except:
			print('')
	for i in range(1, dflen+1):
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
			f = open(path+'/'+filename+'/H_log.dat', 'a+')
			f.write('\tPIDWITH assignment error\n')
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

#Function to modify output to add edge labels
def add_edge_labels(path_des, filename):
	f = open(path_des+filename)
	h = list(f)
	f.close()
	space_separate = {}
	for i in range(len(h)):
		space_separate[i] = re.split(r' ', h[i])
	for i in range(len(space_separate)):
		if len(space_separate[i]) == 5:
			und_sep = []
			und_sep = re.split(r'[_]', space_separate[i][-1])
			und_sep[-2] = und_sep[-2]+'";\n'
			und_sep = und_sep[0:-1]
			ele = und_sep[0]
			for j in range(1, len(und_sep)):
				ele = ele+'_'+und_sep[j]
			space_separate[i][-1] = ele
		for j in range(len(space_separate[i])):
			if space_separate[i][j] == '->':
				und_sep = []
				und_sep = re.split(r'[_]', space_separate[i][j-1])
				ele = und_sep[0]
				for k in range(1, len(und_sep)-1):
					ele = ele+'_'+und_sep[k]
				ele = ele+'"'
				space_separate[i][j-1] = ele
				und_sep = []
				und_sep = re.split(r'[_]', space_separate[i][j+1])
				ele = und_sep[0]
				for k in range(1, len(und_sep)-1):
					ele = ele+'_'+und_sep[k]
				ele = ele+'"'
				space_separate[i][j+1] = ele
				space_separate[i].append('[label="'+und_sep[-1][0:-3]+'" fontcolor="Red"]'+und_sep[-1][-2:])
	f = open(path_des+'/H_sentence_updated')
	sentence = f.readline()
	f.close()
	sentence1 = wx_utf_converter_sentence(sentence).rstrip()
	f = open(path_des+filename, 'w+')
	for i in range(len(space_separate)):
		for j in space_separate[i]:
			if j[-2:] != '\n':
				f.write(str(j)+' ')
			else:
				f.write(str(j)) 
		if i == 0:
			f.write('    labelloc="t";\n     label="'+sentence1+'\\n\\n"\n ')
	f.close()

#Function to draw tree
def drawtree(string, path_des, path, filename, file):
	try:
		error_flag = 0
		importer = JsonImporter()
		root = importer.import_(string)
		file1 = file+'.dot'
		print(RenderTree(root, style=ContRoundStyle()))
		DotExporter(root).to_dotfile(path_des+file1)
		add_edge_labels(path_des, file1)
		check_call(['dot','-Tpng',path_des+file1,'-o',path_des+file+'.png'])
		return(error_flag)
	except:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tInvalid Drawtree input format\n')
		f.close()
		f = open(path_des+'/H_log.dat', 'a+')
		f.write('Invalid Drawtree input format\n')
		f.close()
		return(error_flag)

#Function to modify nmod relation
def nmod_case(relation_df, sub_tree, path_des):
	mod_flag = 0
	for i in relation_df.index:
		if relation_df.RELATION[i] == 'nmod':
			head = relation_df.PID[i]
			if head in sub_tree:
				for j in sub_tree[head]:
					if j[1] == 'case':
						mod_flag = 1
						relation_df.RELATION[i] = relation_df.RELATION[i]+'-'+j[3]
	if mod_flag == 1:	
		f = open(path_des+'/H_log.dat', 'a+')
		f.write('nmod correction made\n')
		f.close()
	sub_tree = create_dict(relation_df)
	return[relation_df, sub_tree]

def obl_err(relation_df, sub_tree, path, filename):
	vib = get_vib()
	list_add_vib = ["ke"]
	for i in range(0, len(vib)):
		vib[i] = vib[i].rstrip()
	new_rel = ""
	f = open(path+'/H_log.dat', 'a+')
	fobl = open(path+'/H_obl_log.dat', 'a+')
	f1 = open(path+'/'+filename+'/H_log.dat', 'a+')
	f_other_vibhaktis = open(path+'/H_other_vibhaktis', 'a+')
	for i in sorted(sub_tree.keys()):
		for j in range(0, len(sub_tree[i])):
			if sub_tree[i][j][1] == "obl":
				lol = sub_tree[i][j][0]
				w = []
				new_rel = ""
				word1 = ""
				if lol in sub_tree:
					no = 0
					for k in range(0, len(sub_tree[lol])):
						if sub_tree[lol][k][1] == "case" or sub_tree[lol][k][1] == "mark":
							word0 = sub_tree[lol][k][0]
							word1 = relation_df.loc[relation_df['PID'] == word0, 'WORD'].iloc[0]
							word2 = word1
							no = 1
							if relation_df.loc[relation_df['PID'] == word0+1, 'RELATION'].iloc[0] == "case" or relation_df.loc[relation_df['PID'] == word0+1, 'RELATION'].iloc[0] == "mark":
								word1 = relation_df.WORD[relation_df['PID'] == word0].iloc[0] + " " + relation_df.WORD[relation_df['PID'] == word0+1].iloc[0]
								no = 2
								if relation_df.loc[relation_df['PID'] == word0+2, 'RELATION'].iloc[0] == "case" or relation_df.loc[relation_df['PID'] == word0+2, 'RELATION'].iloc[0] == "mark":
									word1 = relation_df.loc[relation_df['PID'] == word0, 'WORD'].iloc[0] + " " + relation_df.loc[relation_df['PID'] == word0+1, 'WORD'].iloc[0]+ " " + relation_df.loc[relation_df['PID'] == word0+2, 'WORD'].iloc[0]
									no = 3
							if word1 in vib:
								if no == 3:
									word1 = relation_df.loc[relation_df['PID'] == word0, 'WORD'].iloc[0] + "-" + relation_df.loc[relation_df['PID'] == word0+1, 'WORD'].iloc[0]+ "-" + relation_df.loc[relation_df['PID'] == word0+2, 'WORD'].iloc[0]
								elif no == 2:
									word1 = relation_df.loc[relation_df['PID'] == word0, 'WORD'].iloc[0] + "-" + relation_df.loc[relation_df['PID'] == word0+1, 'WORD'].iloc[0]
								w.append(word1)
								w.append("-")
							else:
								w.append("error")
								w.append("-")
								f_other_vibhaktis.write(filename+'\t'+word1+'\n')
						if no!=0:
							break
					if "error" not in w and w != []:
						new_rel = new_rel.join(w)+"sambandhi"
						sub_tree[i][j][1] = new_rel
						relation_df.at[relation_df.loc[relation_df['PID'] == sub_tree[i][j][0]].index[0], 'RELATION'] = new_rel
						fobl.write(filename+'\t'+str(lol)+'\tobl correction made\n')
						f1.write(str(lol)+'\tobl correction made\n')
					if "error" in w and w != []:
						f.write(filename+'\t'+str(lol)+'\tOccuring vibhakti not in list of vibhakti\n')
						f1.write(str(lol)+'\tOccuring vibhakti not in list of vibhakti\n')
					if w == []:
						f.write(filename+'\t'+str(lol)+'\tobl occurs without case or mark as children\n')
						f1.write(str(lol)+'\tobl occurs without case or mark as children\n')
				else:
					f.write(filename+'\t'+str(lol)+'\tobl occurs without case or mark as children\n')
					f1.write(str(lol)+'\tobl occurs without case or mark as children\n')
	f.close()
	f1.close()
	fobl.close()
	return ([relation_df, sub_tree])

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
	conjunctions = ['Ora', 'waWa']
	solo_conj = ['jabaki', 'lekina']
	error_flag = 0
	try:
		fcclist = open(path+'/H_cc_list.dat', 'r+')
		list_of_cc = list(fcclist)
		fcclist.close()
	except:
		list_of_cc = []
	for i in range(0, len(list_of_cc)):
		list_of_cc[i] = list_of_cc[i].rstrip()
	mod = 0
	conj = 1
	f = open(path+'/H_log.dat', 'a+')
	f1 = open(path+'/'+filename+'/H_log.dat', 'a+')
	fcc = open(path+'/H_cc_log.dat', 'a+')
	i = -1
	while i < len(stack)-1:
		i = i+1
		if stack[i][1] == 'conj':
			cc = 0
			for j in sub_tree[stack[i][2]]:
				if j[1] =='cc' and j[3] not in solo_conj:
					if j[3] not in list_of_cc:
						list_of_cc.append(j[3])
					if cc == 0:
						cc = 1
						g_child = j[0]
					else:
						cc = 2
						mod = 0
						error_flag = 1
						f.write(filename+'\tconj exists with more than 1 cc\n')
						f1.write('conj exists with more than 1 cc\n')
						break
			if cc == 0:
				continue
			elif cc == 2:
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
	if error_flag == 0:
		for i in stack:
			if i[1] == 'cc':
				if i[3] not in list_of_cc:
					list_of_cc.append(i[3])
				if i[3] not in solo_conj:
					for j in stack:
						if j[0] == i[2] and j[1] != 'conj':
							f.write(filename+'\t'+i[3]+' cannot ocur without conj\n')
							f1.write(i[3]+' cannot ocur without conj\n')
							mod = 0
							break
	if mod == 1:
		fcc.write(str(filename)+'\tconj-cc correction made\n')
		f1.write('conj-cc correction made\n')
		for i in sub_tree:
			sub_tree[i].sort()
			for j in sub_tree[i]:
				for k in relation_df.index:
					if relation_df.PID[k] == j[0]:
						relation_df.at[k, 'RELATION'] = j[1]
						relation_df.at[k, 'PIDWITH'] = j[2]
	else:
		sub_tree = create_dict(relation_df)
		stack = BFS(relation_df, sub_tree)
	fcclist = open(path+'/H_cc_list.dat', 'w+')
	for i in range(0, len(list_of_cc)):
		fcclist.write(list_of_cc[i]+'\n')
	fcclist.close()
	fcc.close()
	f.close()
	return([relation_df, stack, sub_tree])

#Generate lwg file
def lwg(path_des, path, filename, relation_df):
	try:
		error_flag = 0
		vib = get_vib()
		for i in range(0, len(vib)):
			vib[i] = vib[i].rstrip()
		vib_list = []
		with open(path_des + "/H_sentence_updated", "r") as f:
			for line in f:
				vib_list.extend(line.split())
		punct = ['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']
		len1 = len(vib_list)
		n_del = 0
		i = 0
		while i < len1:
			if vib_list[i-n_del] in punct:
				del vib_list[i-n_del]
				n_del = n_del + 1
			else:
				if vib_list[i-n_del][-1] in punct:
					vib_list[i-n_del] = vib_list[i-n_del][0:-1]
				if vib_list[i-n_del][0] in punct:
					vib_list[i-n_del] = vib_list[i-n_del][1:]
			i = i + 1
		f_lwg = open(path_des+'/H_def_lwg-wid-word-postpositions_new','w+')
		lwg_list = []
		for i in range(0, len(vib_list)):
			lwg_flag = 0
			if i not in lwg_list:
				if i < len(vib_list)-2:
					grp = vib_list[i]+" "+vib_list[i+1]+" "+vib_list[i+2]
					if grp in vib:
						lwg_flag = 1
						lwg_list.append(i)
						lwg_list.append(i+1)
						lwg_list.append(i+2)
						lwg = vib_list[i-1]+"_"+vib_list[i]+"_"+vib_list[i+1]+"_"+vib_list[i+2]
						f_lwg.write("(H_def_lwg-wid-word-postpositions\t"+lwg+"\t"+str(i)+"\t"+vib_list[i-1]+"\t"+str(i+1)+" "+str(i+2)+" "+str(i+3)+")\n")
				if i < len(vib_list)-1 and lwg_flag == 0:
					grp = vib_list[i]+" "+vib_list[i+1]
					if grp in vib:
						lwg_flag = 1
						lwg_list.append(i)
						lwg_list.append(i+1)
						lwg = vib_list[i-1]+"_"+vib_list[i]+"_"+vib_list[i+1]
						f_lwg.write("(H_def_lwg-wid-word-postpositions\t"+lwg+"\t"+str(i)+"\t"+vib_list[i-1]+"\t"+str(i+1)+" "+str(i+2)+")\n")
				if lwg_flag == 0:
						grp = vib_list[i]
						if grp in vib:
							lwg_list.append(i)
							lwg = vib_list[i-1]+"_"+vib_list[i]
							f_lwg.write("(H_def_lwg-wid-word-postpositions\t"+lwg+"\t"+str(i)+"\t"+vib_list[i-1]+"\t"+str(i+1)+")\n")
	except:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tError in lwg module\n')
		f.close()
		f = open(path_des+'/H_log.dat', 'a+')
		f.write('Error in lwg module\n')
		f.close()
	return(error_flag)

#Function to update tam and vibakthi details
def tam_and_vib_lwg(error_flag, sub_tree, relation_df, path, path_des, filename):
	list1 = []
	list2 = []
	unable_to_delete = []
	stack = BFS(relation_df, sub_tree)
	word_final = ""
	if error_flag == 0:
		#Vib file opening
		vib_path = path_des+'/H_def_lwg-wid-word-postpositions_new'
		f = open(vib_path)
		vibs = list(f)
		for i in range(0, len(vibs)):
			vibs[i] = vibs[i].rstrip()
			vibs[i] = re.split(r'\t', vibs[i])
		#Vib updation
		for i in range(0, len(vibs)):
			word = re.split(r'_', vibs[i][1])
			for j in range(len(word)):
				if j == 0:
					word_final = word[j]
				else:
					word_final = word_final+"-"+word[j]
			relation_df.loc[relation_df.PID == int(vibs[i][2]), 'WORD'] = word_final
			pos = re.split(r' ', vibs[i][4])
			for j in range(len(pos)):
				if pos[j][-1] == ')':
					pos[j] = pos[j][0:-1]
				list1.append(int(pos[j]))
		list1.reverse()
	#TAM file opening
	flag = 0
	try:
		tam_path =path_des + "/revised_manual_local_word_group.dat"
		f = open(tam_path)
		flag = 1
		tam = list(f)
		for i in range(0, len(tam)):
			tam[i] = tam[i].rstrip()
			tam[i] = re.split(r'\t', tam[i])
		for i in range(0, len(tam)):
			word = re.split(r'_', tam[i][4])
			for j in range(len(word)):
				if j == 0:
					word_final = word[j]
				else:
					word_final = word_final+"-"+word[j]
			tam[i][4] = word_final
		#TAM updation
		for i in range(0, len(tam)):
			if tam[i][5] != '0)':
				error_flag = 0                                                                                   
				pos1 = []
				head = -1
				split = tam[i][5].split()
				for j in range(0, len(split)):
					if j == len(split) - 1:
						pos = int(split[j][0:-1])
					else:
						pos = int(split[j])
					pos1.append(pos)
				for j in range(0, len(pos1)):
					id = relation_df.loc[relation_df.PID == pos1[j], 'PIDWITH'].iloc[0]
					if id not in pos1:
						if head != -1:
							error_flag = 1
							f = open(path+'/H_log.dat', 'a+')
							f.write(str(filename) +'\tlwg parser mismatch around node '+str(head)+'\n')
							f.close()
							break
						else:
							head = pos1[j]
				if error_flag != 1:
					relation_df.loc[relation_df.PID == head, 'WORD'] = tam[i][4]
					for j in range(0, len(stack)):
						if stack[j][0] in pos1 and stack[j][0] != head:
							list2.append(stack[j][0])
		list2.reverse()			
	except:
		print('')
	if flag == 0:
		try:
			tam_path =path_des + "/manual_local_word_group.dat"
			f = open(tam_path)
			flag == 1
			tam = list(f)
			for i in range(0, len(tam)):
				tam[i] = tam[i].rstrip()
				tam[i] = re.split(r'\t', tam[i])
			#TAM updation
			for i in range(0, len(tam)):
				if tam[i][3] != '0)':
					error_flag = 0
					pos1 = []
					head = -1
					split = tam[i][3].split()
					for j in range(0, len(split)):
						if j == len(split) - 1:
							pos = int(split[j][0:-1])
						else:
							pos = int(split[j])
						pos1.append(pos)
					for i in range(0, len(pos1)):
						id = relation_df.loc[relation_df.PID == pos1[i], 'PIDWITH'].iloc[0]
						if id not in pos1:
							if head != -1:
								error_flag = 1
								f = open(path+'/H_log.dat', 'a+')
								f.write(str(filename) +'\tSubtree error around node '+str(head)+'\n')
								f.close()
								f = open(path_des+'/H_log.dat', 'a+')
								f.write('Subtree error around node '+str(head)+'\n')
								f.close()
								break
							else:
								head = pos1[j]
					if error_flag != 1:
						relation_df.loc[relation_df.PID == head, 'WORD'] = tam[i][2]
						for j in range(0, len(stack)):
							if stack[i][0] in pos:
								list2.append(stack[i][0])
			list2.reverse()
		except:
			print('')
	f = open(path+'/H_tam_vib_log.dat', 'a+')
	f1 = open(path+'/H_log.dat', 'a+')
	f2 = open(path_des+'/H_log.dat', 'a+')
	for j in list1:
		if j not in sub_tree:
			relation_df = relation_df.drop(relation_df[relation_df.PID == j].index[0])
			sub_tree = create_dict(relation_df)
			f.write(filename+'\t'+str(j)+'\t'+'has been deleted\n')
			f2.write(str(j)+'\t'+'has been deleted\n')
		else:
			unable_to_delete.append(j)
	f.close()
	f1.close()
	f2.close()	
	if flag == 1:
		#relation deletion and updation
		f = open(path+'/H_tam_vib_log.dat', 'a+')
		f1 = open(path+'/H_log.dat', 'a+')
		f2 = open(path_des+'/H_log.dat', 'a+')
		for j in list2:
			if j not in list1 and j not in sub_tree:
				relation_df = relation_df.drop([relation_df.loc[relation_df['PID'] == j].index[0]], axis = 0)
				sub_tree = create_dict(relation_df)
				f.write(filename+'\t'+str(j)+'\t'+'has been deleted\n')
				f2.write(str(j)+'\t'+'has been deleted\n')
			else:
				unable_to_delete.append(j)
		f.close()
		f1.close()
		f2.close()
		return[relation_df, unable_to_delete]
	else:
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tBoth revised_manual_local_word_group.dat as well as manual_local_word_group.dat are not present\n')
		f.close()
		f = open(path_des+'/H_log.dat', 'a+')
		f.write('Both revised_manual_local_word_group.dat as well as manual_local_word_group.dat are not present\n')
		f.close()
		return(relation_df, unable_to_delete)

#Function to combine compound relations
def compound_combine(unable_to_delete, relation_df, path, path_des, filename):
	mod_flag = 0
	f = open(path_des+'/H_parser-lwg-wid-word-postpositions.dat', 'w+')
	for i in relation_df.index:
		if relation_df.RELATION[i] == 'compound':
			mod_flag = 1
			child = relation_df.PID[i]
			head = relation_df.PIDWITH[i]
			if child in unable_to_delete:
				unable_to_delete.remove(relation_df.PID[i])
			else:
				if head > child:
					if relation_df.loc[relation_df.PID == head, 'WORD'].iloc[0] == 'kI':
						combine = relation_df.loc[relation_df.PID == child, 'WORD'].iloc[0]
					else:
						combine = relation_df.loc[relation_df.PID == child, 'WORD'].iloc[0]+'-'+relation_df.loc[relation_df.PID == head, 'WORD'].iloc[0]
				else:
					combine = relation_df.loc[relation_df.PID == head, 'WORD'].iloc[0]+'-'+relation_df.loc[relation_df.PID == child, 'WORD'].iloc[0]
				combine1 = re.split(r'-', combine)
				head1 = re.split(r'-', relation_df.loc[relation_df.PID == head, 'WORD'].iloc[0])
				for j in range(len(combine1)):
					if j == 0:
						lwg = combine1[j]
					else:
						lwg = lwg+'_'+combine1[j]
				for j in range(len(head1)):
					if j == 0:
						word = head1[j]
					else:
						word = word+'_'+head1[j]
				f.write('(H_parser-lwg-wid-word-postpositions\t'+lwg+'\t'+str(head)+'\t'+word+'\t'+str(child)+')\n')
				relation_df.loc[relation_df.PID == head, 'WORD'] = combine
			for j in relation_df.index:
				if relation_df.PIDWITH[j] == child:
					relation_df.PIDWITH[j] = head
			relation_df = relation_df.drop([relation_df.loc[relation_df['PID'] == child].index[0]], axis = 0)
	f.close()
	if mod_flag == 1:	
		f = open(path_des+'/H_log.dat', 'a+')
		f.write('compound combine made\n')
		f.close()
	return[relation_df, unable_to_delete]

def undeletable_nodes(unable_to_delete, relation_df, path, path_des, filename):
	f1 = open(path+'/H_log.dat', 'a+')
	f2 = open(path_des+'/H_log.dat', 'a+')
	for i in range(len(unable_to_delete)):
		if relation_df.loc[relation_df.PID == unable_to_delete[i], 'POS'].iloc[0] == 'VERB':
			f1.write(filename+'\t'+str(unable_to_delete[i])+'\t'+'has children but is trying to be deleted. Here we are depending on parser output over def facts.\n')
			f2.write(str(unable_to_delete[i])+'\t'+'has children but is trying to be deleted. Here we are depending on parser output over def facts.\n')
		else:
			f1.write(filename+'\t'+str(unable_to_delete[i])+'\t'+'has children but is trying to be deleted\n')
			f2.write(str(unable_to_delete[i])+'\t'+'has children but is trying to be deleted\n')
	f1.close()
	f2.close()

#Function to store tree in single line
def find_single_line_tree(node, sub_tree, clause):
	clause.append(node)
	if node in sub_tree:
		for i in sub_tree[node]:
			find_single_line_tree(i[0], sub_tree, clause)
	return(clause)

#Function to form Word-ID to Word mappings
def wordid_word_mapping(relation_df):
	wordid_word = []
	for i in relation_df.index:
		wordid_word.append([relation_df.PID[i], relation_df.WORD[i]])
	return(wordid_word)

#Function create wordid word dictionary 
def wordid_word_dict(wordid_word):
	wordid_word_dict = {}
	for pair  in wordid_word:
		wordid_word_dict[0]='root'
		wordid_word_dict[pair[0]]=pair[1]
	return(wordid_word_dict)

#Function to form Parser-ID to Word-ID mappings
def parserid_wordid_mapping(relation_df):
	parserid_wordid = []
	for i in relation_df.index:
		parserid_wordid.append([i, relation_df.PID[i]])
	return(parserid_wordid)

#Function to creation relation facts
def relation_facts(relation_df):
	relation_facts1 = []
	for i in relation_df.index:
		if relation_df.PIDWITH[i] == 0:
			head_word = 'root'
		else:
			head_word = relation_df.loc[relation_df.PID == relation_df.PIDWITH[i], 'WORD'].iloc[0]
		relation_facts1.append([relation_df.PID[i], relation_df.WORD[i], relation_df.POS[i], relation_df.RELATION[i], relation_df.PIDWITH[i], head_word])		
	return(relation_facts1)
	
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

#Function to create groupings
def write_groupings(path_des, wordid_word, wordid_word_dict, sub_tree):
	for i in wordid_word:
		for j, values in sub_tree.items():
			for k in values:
				if k[0] == i[0]:
					lvl = k[4]
		clause_list = []
		clause_list = find_single_line_tree(i[0], sub_tree, clause_list)
		clause_list.sort()
		clause_list_string = [str(i) for i in clause_list]
		string = " ".join(clause_list_string)
		f = open(path_des + '/H_grouping_ids.dat', 'a+')
		f.write('(H_grp_hid-grp_hid-lvl_elem-ids\t'+ str(i[0]) + '\t' + str(lvl) + '\t' + string + ')\n')
		f.close()
		clause_list_word = [wordid_word_dict[i] for i in clause_list]
		string_words = ' '.join(clause_list_word)
		f = open(path_des + '/H_grouping_words.dat', 'a+')
		f.write('(H_grp_hword-grp_elem_words\t'+ wordid_word_dict[i[0]] + '\t' + string_words + ')\n')
		f.close()
		f = open(path_des + '/H_grouping_template.dat', 'a+')
		f.write('(H_group (language hindi) (grp_hid '+ str(i[0]) +') (grp_lvl '+ str(lvl) +') (grp_head_word '+  wordid_word_dict[i[0]] +' ) (grp_element_ids '+ string +') (grp_element_words '+ string_words +'))\n')
		f.close()

#Function to store the 67punct details
def write_punct_info(path_des, punct_info):
	f = open(path_des+"/H_punct_info.dat", 'w+')
	for i in range(0, len(punct_info)):
		if punct_info[i][1] == 'M':
			f.write("(H_punc-pos-ID\t"+punct_info[i][0]+"\tM\t"+str(punct_info[i][2])+"\t"+str(punct_info[i][3])+")\n")
		elif punct_info[i][1] == 'L':
			f.write("(H_punc-pos-ID\t"+punct_info[i][0]+"\tL\t"+str(punct_info[i][2])+")\n")
		else:
			f.write("(H_punc-pos-ID\t"+punct_info[i][0]+"\tR\t"+str(punct_info[i][3])+")\n")
	f.close()

#Function to store the wordid word mappings
def write_wordid_word(path_des, wordid_word):
	f = open(path_des+'/H_wordid-word_mapping.dat','w+')
	for i in range(0, len(wordid_word)):
		f.write("(H_wordid-word\t"+str(wordid_word[i][0])+"\t"+wordid_word[i][1]+")\n")
	f.close()

#Function to store the parserid wordid mappings
def write_parserid_wordid(path_des, parserid_wordid):
	f = open(path_des+'/H_parserid-wordid_mapping.dat', 'w+')
	for i in range(0, len(parserid_wordid)):
		f.write("(H_parserid-wordid\tP"+str(parserid_wordid[i][0])+"\t"+str(parserid_wordid[i][1])+")\n")
	f.close()

#Function to store the relation details
def write_relation_facts(path_des, relation_facts):
	f = open(path_des+'/H_relation_final_facts', 'w+')
	for i in range(0, len(relation_facts)):
		f.write('(H_cid-word-pos-relation-hid-hword\t'+str(relation_facts[i][0])+'\t'+relation_facts[i][1]+'\t'+relation_facts[i][2]+'\t'+relation_facts[i][3]+'\t'+str(relation_facts[i][4])+'\t'+relation_facts[i][5]+')\n')
	f.close()

#Funcction to add levels in subree
def add_lvl(stack, sub_tree):
	for i in stack:
		if i[0] in sub_tree:
			if i[0] == 0:
				lvl = 1
			else:
				for j, values in sub_tree.items():
					for k in values:
						if k[0] == i[0]:
							lvl  = k[4]+1
			for j in sub_tree[i[0]]:
				j.append(lvl)
	return(sub_tree)


#Function to write modified file in standard conll format(tab separated)
def write_modified_file(path_des, file):
	f = open(path_des+file)
	relation = list(f)
	f.close()
	set1 = [0, 1, ]
	for i in range(len(relation)):
		relation[i] = re.split(r'\t',relation[i])
	relation_df = []
	for i in relation:
		relation1 = []
		relation1.append(i[0])
		relation1.append(i[1])
		relation1.append('_')
		relation1.append(i[2])
		relation1.append('_\t_')
		relation1.append(i[4].rstrip())
		relation1.append(i[3])
		relation1.append('_\t_')
		relation_df.append(relation1)
	f = open(path_des+file, 'w+')
	for i in relation_df:
		for j in i:
			f.write(j+'\t')
		f.write('\n')
	f.close()
