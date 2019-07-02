import re
from wxconv import WXC
import pandas as pd
import numpy as np
from anytree.importer import JsonImporter
from anytree import (RenderTree, ContRoundStyle)
from anytree.exporter import DotExporter 
from IPython.display import Image
from subprocess import check_call

#Function to get list of vibhakti
def get_vib():
	path_vib ="/home/kailash/n_tree-master/vibhakti"
	f1 = open(path_vib)
	vib = list(f1)
	f1.close()
	return(vib)

#Function to delete old log 
def clear_logs(path):
	f = open(path+'/H_log.dat', 'w+')
	f = open(path+'/H_obl_log.dat', 'w+')
	f = open(path+'/H_cc_log.dat', 'w+')
	f.close()

#Function to clear residue files from previous run
def clear_files(path_des):
	f = open(path_des+'/H_grouping_ids.dat', 'w+')
	f = open(path_des+'/H_grouping_words.dat', 'w+')
	f = open(path_des+'/H_grouping_template.dat', 'w+')
	f.close()

#Function to create dataframe
def create_dataframe(parse, path, filename):
	count = 0
	error_flag = 0
	df = pd.read_csv(parse, sep='\t',names=['PID','WORD','1-','POS','2-','3-','PIDWITH','RELATION','4-','5-'], quoting = 3, index_col = False)
	df.index = np.arange(1,len(df)+1)
	df1 = df[['PID','WORD','POS','RELATION','PIDWITH']]
	relation_df =  pd.concat([df1.PID, df1.WORD,df1.POS, df1.RELATION, df1.PIDWITH], axis=1)
	for i in range(len(relation_df)):
		if relation_df.iloc[i]['RELATION'] == 'root':
			count = count+1
	if type(relation_df.PID[1]) != np.int64:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tTree has non-int PID\n')
		f.close()
	if count != 1:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tMore than 1 tree\n')
		f.close()
	return ([relation_df, error_flag])

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
				word_l = space_separate[i-1]
				word_r = space_separate[i+1]
			if middle == 1:
				punct_info1.append([space_separate[i], 'M', k, k+1])
			elif left == 1:
				punct_info1.append([space_separate[i][0], 'L', k, -1])
			elif right == 1:
				punct_info1.append([space_separate[i][-1], 'R', -1, k])
		f.close()
		return([k, punct_info1])
	except Exception as e:
		print(e)
		k = 0
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tH_sentence not present\n')
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
		return(error_flag)

#Function to correct obl errors
def obl_err(relation_df, sub_tree, path, filename):
	vib = get_vib()
	for i in range(0, len(vib)):
		vib[i] = vib[i].rstrip()
	new_rel = ""
	no = 0
	f = open(path+'/H_log.dat', 'a+')
	fobl = open(path+'/H_obl_log.dat','a+')
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
							word0 = sub_tree[lol][k][0]
							word1 = relation_df.loc[relation_df['PID'] == word0, 'WORD'].iloc[0]
							no = 1
							if relation_df.loc[relation_df['PID'] == word0+1, 'RELATION'].iloc[0] == "case" or relation_df.loc[relation_df['PID'] == word0+1, 'RELATION'].iloc[0] == "mark":
								word1 = relation_df.WORD[relation_df['PID'] == word0].iloc[0] + " " + relation_df.WORD[relation_df['PID'] == word0+1].iloc[0]
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
						sub_tree[i][j][1] = new_rel
						relation_df.at[relation_df.loc[relation_df['PID'] == sub_tree[i][j][0]].index[0], 'RELATION'] = new_rel
						fobl.write(filename+'\t'+str(lol)+'\tobl correction made\n')
					if ("error" in w and w != []):
						f.write(filename+'\t'+str(lol)+'\tOccuring vibhakti not in list of vibhakti\n')
					if w == []:
						f.write(filename+'\t'+str(lol)+'\tobl occurs without case or mark as children\n')
				else:
					f.write(filename+'\t'+str(lol)+'\tobl occurs without case or mark as children\n')
	f.close()
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
	conjunctions = ['Ora']
	solo_conj = ['jabaki', 'lekina']
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
	fcc = open(path+'/H_cc_log.dat', 'a+')
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
		fcc.write(str(filename)+'\tconj-cc correction made\n')
		for i in sub_tree:
			sub_tree[i].sort()
			for j in sub_tree[i]:
				for k in relation_df.index:
					if relation_df.PID[k] == j[0]:
						relation_df.at[k, 'RELATION'] = j[1]
						relation_df.at[k, 'PIDWITH'] = j[2]
	else:
		sub_tree = create_dict(relation_df)
	fcclist = open(path+'/H_cc_list.dat', 'w+')
	for i in range(0, len(list_of_cc)):
		fcclist.write(list_of_cc[i]+'\n')
	fcclist.close()
	fcc.close()
	f.close()
	return([relation_df, stack, sub_tree])

#Generate lwg file
def lwg(path_des, path, filename):
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
		for i in range(0, len(vib_list)):
			if vib_list[i][-1] in punct:
				vib_list[i] = vib_list[i][0:-1]
		f_lwg = open(path_des+'/H_def_lwg-wid-word-postpositions_new','w+')
		for i in range(0, len(vib_list)):
			word = ""
			word1 = ""
			word2 = ""
			if vib_list[i] in vib:
				word = vib_list[i-1]+"_"+vib_list[i]
				word1 = vib_list[i]+" "+vib_list[i+1]
				if word1 in vib:
					word = word+"_"+vib_list[i+1]
					word2 = vib_list[i]+" "+vib_list[i+1]+" "+vib_list[i+2]
					if word2 in vib:
						word = word+ "_" + vib_list[i+2]
				f_lwg.write("(H_def_lwg-wid-word-postpositions\t"+word+"\t"+str(i)+"\t"+vib_list[i-1]+"\t"+str(i+1)+")\n")
	except:
		error_flag = 1
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tH_sentence not present\n')
		f.close()
	return(error_flag)

#Function to update tam and vibakthi details
def tam_and_vib_lwg(error_flag, sub_tree, relation_df, path, path_des, filename):
	list1 = []
	stack = BFS(relation_df, sub_tree)
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
			relation_df.loc[relation_df.PID == int(vibs[i][2]), 'WORD'] = vibs[i][1]
			pos = int(vibs[i][2])+1
			list1.append(pos)
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
					dele = []
					for j in range(0, len(stack)):
						if stack[j][0] in pos1 and stack[j][0] != head:
							dele.append(stack[j][0])
					dele.reverse()
					for j in range(0, len(dele)):
						list1.append(dele[j])
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
								break
							else:
								head = pos1[j]
					if error_flag != 1:
						relation_df.loc[relation_df.PID == head, 'WORD'] = tam[i][2]
						dele = []
						for j in range(0, len(stack)):
							if stack[i][0] in pos:
								dele.append(stack[i][0])
						dele.reverse()
						for i in range(0, len(dele)):
							list1.append(dele[i])
		except:
			print('')
	if flag == 1:
		#relation deletion and updation
		f = open(path+'/tam_vib_error_log', 'a+')
		for j in list1:
			if j not in sub_tree:
				relation_df = relation_df.drop([relation_df.loc[relation_df['PID'] == j].index[0]], axis = 0)
			else:
				f.write(filename+'\t'+str(j)+'\t'+'has children but is trying to be deleted\n')
		f.close()
		return(relation_df)
	else:
		f = open(path+'/H_log.dat', 'a+')
		f.write(filename +'\tBoth revised_manual_local_word_group.dat as well as manual_local_word_group.dat are not present\n')
		f.close()
		return(relation_df)

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
		relation_facts1.append([relation_df.PID[i], relation_df.WORD[i], relation_df.PIDWITH[i], relation_df.POS[i], relation_df.RELATION[i]])
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
		clause = []
		clause_list = []
		clause_list = find_single_line_tree(i[0], sub_tree, clause_list)
		clause_list.sort()
		clause_list_string = [str(i) for i in clause_list]
		string = " ".join(clause_list_string)
		f = open(path_des + '/H_grouping_ids.dat', 'a+')
		f.write('(H_grp_hid-grp_elem_ids\t'+ str(i[0]) + '\t' + string + ')\n')
		f.close()
		clause_list_word = [wordid_word_dict[i] for i in clause_list]
		string_words = ' '.join(clause_list_word)
		f = open(path_des + '/H_grouping_words.dat', 'a+')
		f.write('(H_grp_hword-grp_elem_words\t'+ wordid_word_dict[i[0]] + '\t' + string_words + ')\n')
		f.close()
		f = open(path_des + '/H_grouping_template.dat', 'a+')
		f.write('(H_group (language hindi) (grp_hid '+ str(i[0]) +') (grp_head_word '+  wordid_word_dict[i[0]] +' ) (grp_element_ids '+ string +') (grp_element_words '+ string_words +'))\n')
		f.close()

#Function to store the punct details
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
		f.write('(H_cid-word-hid-pos-relation\t'+str(relation_facts[i][0])+'\t'+relation_facts[i][1]+'\t'+str(relation_facts[i][2])+'\t'+relation_facts[i][3]+'\t'+relation_facts[i][4]+')\n')
	f.close()