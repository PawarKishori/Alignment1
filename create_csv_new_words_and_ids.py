#Author: Ayushi
import sys
import subprocess
import re
import os
# from wxconv import WXC  #Irshad's wx_utf8 convertor
from collections import defaultdict

f1 = open("clips_to_csv_words.csv",'w')
f11 = open("clips_to_csv_ids.csv",'w')
f3 = open("Sentences_for_alignment.dat",'w')
# con = WXC(order='wx2utf', lang='hin')
#sent_path='/home/user/collaborator/tmp_anu_dir/tmp/rGitaE_Up_035_tmp/2.15/'
#Modularize the code for some parts
Oth=[]
mid_mng=[]
R_temp=[]
original_cl_words=[]
H_parserid_wordid=[]
def replace_uneven_spaces_by_a_single_space(line):
	return (re.sub( '\s+', ' ', line ).strip());

def create_dummy_list(length,col_length):
	listname=[]
	for i in range(length):
		temp_tuple=tuple([i+1]+['-' for k in range(col_length)])
		listname.append(temp_tuple)
	return listname;

def write_layer_to_file(list_wx,field):
	for i in list_wx:
		f1.write("#"+i[field])  #to print string without '@'
		
def check_if_list1_is_sublist_of_list2(lst1,lst2):
	return set(lst1) <= set(lst2)

def check_file_to_be_read(filename):
    if (os.path.exists(filename)):
        if(os.path.getsize(filename)==0):
            print(filename + " is empty") 
            return 1;
    else:
        print(filename + " is not created") 
        return 2;

def create_lists_with_hindi_word_ids(X_sorted_list, hindi_words_list, layer_name, max_len, H_pid_wid_word):
	#print(layer_name+": hindi_words_list",hindi_words_list)
	X_layer_indices = phrase_occuring_indices_count(X_sorted_list,hindi_words_list)	
	phrase_id_mapping, phrase_having_occurence_count_zero, phrases_having_unresolved_multiple_occurences = extracting_x_layer_ids(X_layer_indices, X_sorted_list)
	# print("phrase_having_occurence_count_zero", phrase_having_occurence_count_zero)
	#print("phrases_having_unresolved_multiple_occurences", phrases_having_unresolved_multiple_occurences)
	X_sorted_for_hids = [(r[0],r[1],str(r[2])) for r in X_sorted_list]
	X_sorted_for_hids = sorted(X_sorted_for_hids, key=lambda x: x[1])
	phrase_id_mapping = sorted(phrase_id_mapping, key=lambda x: x[1])
	#print(layer_name+": phrase_id_mapping before", phrase_id_mapping)
	for ph in phrase_id_mapping:
		for index,k in enumerate(X_sorted_for_hids):
			#print("before",ph,k)
			if k[1].startswith('@h:'):
				k1_mod = " ".join(k[1].split()[1:])
			else:
				k1_mod = k[1]
			if ph[0]==k[1] or ph[0]==k1_mod:
				#print("inside",ph,k)
				X_sorted_for_hids[index]=(k[0],k1_mod,'K'+" ".join(map(str,ph[1])))
				break
	# Mapping manju mam's ids with kishori's ids for phrases which have zero occurence in the hwords1 (Discontinued word groups won't get matched. Eg: {nirmANa} waWA saMSoXana {huA hE})
	#print(layer_name+": X_sorted_for_hids", X_sorted_for_hids)
	H_parserid_dict = {str(elem[0]):elem[1] for elem in H_parserid_wordid}
	#H_parserid_dict_rev = {str(elem[1]):elem[0] for elem in H_parserid_wordid}
	#print("H_parserid_dict",H_parserid_dict)
	for each_index,each_tup in enumerate(X_sorted_for_hids):
		if each_tup[1] in phrase_having_occurence_count_zero:
			if each_tup[2] in H_parserid_dict: #str(et[0]):
				X_sorted_for_hids[each_index]=(each_tup[0],each_tup[1],'K'+str(H_parserid_dict[each_tup[2]]))
		for p_ind, p_tup in enumerate(phrases_having_unresolved_multiple_occurences):
			for l1 in p_tup[1]: 
				if not each_tup[2].startswith('K'): 
					if H_parserid_dict[each_tup[2]] == l1[0]:
						X_sorted_for_hids[each_index]=(each_tup[0],each_tup[1],'K'+str(H_parserid_dict[each_tup[2]]))
						#print(H_parserid_dict[each_tup[2]],l1[0])
	# print(layer_name+": phrase_id_mapping", phrase_id_mapping)
	X_sorted_for_hids_filled = create_dummy_list(max_len ,3)
	X_sorted_for_hids = sorted(X_sorted_for_hids, key=lambda x: x[0])
	for ind,l in enumerate(X_sorted_for_hids_filled):
		for m in X_sorted_for_hids:
			if l[0]==m[0]:
				X_sorted_for_hids_filled[ind] = (m[0],m[1],m[2])
	f11.write("\n"+layer_name)

	
	#print(layer_name+": X_sorted_for_hids_filled", X_sorted_for_hids_filled) 
	for tup in X_sorted_for_hids_filled:
		if layer_name == 'P' and tup[1] == '-':
			f11.write("#"+tup[1])
		else:
			f11.write("#"+str(tup[2]))

def phrasal_layers(layer_name,filename, hindi_id_word):
	d1 = defaultdict(list)
	temp1=[]
	hindi_id_word = sorted(hindi_id_word, key=lambda x: x[1])
	# print ("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", hindi_id_word)
	f1.write("\n$ENG_"+layer_name+'_ENG$')
	f11.write("\n"+layer_name)
	x4 = check_file_to_be_read(filename)
	if x4!=1 and x4!=2:
		f2 = open(filename,'r')
		for line in f2:
			l=line.strip().split()
			temp1.append((int(l[1]),l[3].split(')')[0]))
		temp1 = sorted(temp1, key=lambda x: x[1])
		# print temp1
		temp1_filtered=filter(lambda x: '-' not in x[1],temp1)
		temp1_rest=list(set(temp1)-set(temp1_filtered))
		# assert len(temp1_filtered)==len(hindi_id_word), "Some error in "+filename
		for t,w in zip(temp1_filtered,hindi_id_word):
			temp1_filtered[temp1_filtered.index(t)]=(t[0],int(w[0]))
		temp1_filtered+=temp1_rest
		temp1_filtered = sorted(temp1_filtered, key=lambda x: x[0])
	
		for v in temp1_filtered:
			f11.write("#"+str(v[1]))
		f2.close()
	# combining values with similar word_ids
	for k,v in temp1:
		d1[k].append(v)
	for key in d1:
		term=" ".join(d1[key])
		if '@' in term:
			term=term.split('-')[0]
		f1.write("#"+term)
	

def Nth_Oth_P1th_layers(layer_name,filename, fact_to_be_matched, max_id, hwords1_list, H_parserid_wordid):
	count=0
	global Oth 
	temp_Oth = []
	unsorted=[]
	Anu_padded=[]
	f1.write("\n$ENG_"+layer_name+'_ENG$')
	x10 = check_file_to_be_read(filename)
	if x10!=1 and x10!=2:		
		f2 = open(filename,'r')
		if layer_name=='O':
			Oth = create_dummy_list(max_id,4)
		# for line in f2:
		# 	m=re.match(fact_to_be_matched,line)
		# 	print("m",m)
		# 	anu_id, anu_meaning, man_id, man_meaning = [m.group(i) for i in range(1,5)] 
		# 	anu_meaning = [str(conv_to_canonical(w)) for w in anu_meaning.strip().split()]
		# 	man_id = [int(i) for i in man_id.strip().split()]
		# 	man_meaning = [str(conv_to_canonical(w)) for w in man_meaning.strip().split()]
		# 	# man_group_ids = [int(i) for i in man_group_ids.strip().split()]
		for line in f2:
			l=line.strip().split('(')
			anu_id=l[2].split(')')[0].split(' ',1)[1]
			if layer_name == 'N' or layer_name == 'O':
				anu_mng = l[4].split(')')[0].split(' ',1)
				man_id = l[3].split(')')[0].split(' ',1)[1]
			else:
				man_id = l[4].split(')')[0].split(' ',1)[1]
				anu_mng = l[3].split(')')[0].split(' ',1)
			man_mng=l[5].split(')')[0].split(' ',1)
			# To handle when there is absence of any anu_mng
			'''['anu_meaning']
			['anu_meaning', 'panKA karawA hE']
			['anu_meaning', 'CIlA huA']'''
			if len(anu_mng)>1:
				anu_mng=anu_mng[1]
			else: 
				anu_mng=' '
			if len(man_mng)>1:
				man_mng=man_mng[1]
			else:
				man_mng=' '
			# print ("THISSSSSSSSSSS:"+layer_name+":",anu_id, anu_mng, man_id, man_mng)
			unsorted.append((int(anu_id),anu_mng,man_mng,int(man_id)))
			if (layer_name=='O'):
				temp_Oth.append((int(anu_id),man_mng,anu_mng,int(man_id)))
		temp_Oth.sort()
		Anu=sorted(unsorted) 
		Anu_columns_swapped=[(c[0],c[2],c[3],c[1]) for c in Anu]
		# print (layer_name+": Anu:",Anu_columns_swapped)
		create_lists_with_hindi_word_ids(Anu_columns_swapped, hwords1_list, layer_name, max_id, H_parserid_wordid)
		Anu_padded=create_dummy_list(max_id,3)
		# Replacing required tuples in the padded list # 
		for t in Anu:
			for i,v in enumerate(Anu_padded):
				if v[0]==t[0]:
					Anu_padded[i]=t
					break
		if (layer_name=='O'):
			for o in temp_Oth:
				for l,m in enumerate(Oth):
					if m[0]==o[0]:
						Oth[l]=o
						break
		write_layer_to_file(Anu_padded,2)
		f2.close();

def check_word_in_list_of_clauses(clauses, word, hids, layer):	
	res=[]
	res1=[]
	for clause in clauses:
		# print (clause, word, hids, layer)
		word=str(conv_to_canonical(word))
		if len(clause[2])<0: continue
		if len(word.strip().split()) == 1 : 
			if word == clause[0][0] and hids == clause[1][0] :  
				res.append(word)
			elif word in clause[2] and hids in clause[3]:
				res.append('2')
			else: 
				# print(word+" not found in clauses")
				res.append(word)
		else:
			if word == " ".join(clause[0]) and hids == clause[1]:
				res.append(word)
			elif word in " ".join(clause[0]) and hids in clause[1]:
				res1.append('2')
			elif word in " ".join(clause[2]) and hids in clause[3]:
				res1.append('3')
			else:
				# print(word+" not found in clauses")
				res.append(word)
	if '2' in res or '2' in res1 or '3' in res1:  
		# print(word+" found in clause words and has ids: ", hids, layer)
		return 1;
	else: return word;	

def check_left_over_word_in_list_of_aligned_clauses(aligned_clauses, word, eids, hids, layer):	
	res1=[]
	for c in aligned_clauses:
		if eids in c[0] and hids in c[2]:
			# print (word+" found in respective clause")
			# print(c[0],c[2], word, eids, hids)
			res1.append('1')
		else:
			# print (word+" not found in respective clauses")
			res1.append(word)
	if '1' in res1: 
		return 1;
	else:
		return (word)

def check_morph(word1):
	f1=open("hi","w")
	f1.write(word1)
	f1.close()
	cmd="echo $HOME"
	bin_path=subprocess.check_output(cmd, shell=True)
	cmd1="sh "+bin_path.decode("utf-8").strip()+"/bin/hin_morph.sh < hi"
	result=subprocess.check_output(cmd1, shell=True)
	return(result.decode("utf-8"))

def conv_to_canonical(word):
	f1 = open('canonical',"w")
	f1.write(word)
	f1.close()
	cmd="echo $HOME_anu_test"
	path = "/Anu_data/canonical_form_dictionary"
	bin_path=subprocess.check_output(cmd, shell=True)
	cmd1=bin_path.decode("utf-8").strip()+path+"/canonical_form.out < canonical"
	result=subprocess.check_output(cmd1, shell=True)
	return(result.decode("utf8"))

def extracting_x_layer_ids(X_layer_indices, X_sorted_list=[]):
	X_layer_indices = sorted(X_layer_indices, key= lambda x: len(x[0]), reverse=True)
	# print ("X_layer_indices: ",X_layer_indices)
	answer=[]
	completed_indices=[]
	phrases_with_count_zero_in_X_layer_indices=[]
	phrases_with_multiple_occurence_unresolved=[]
	while X_layer_indices:
		#print ("In while loop:",X_layer_indices)
		new_X_layer_indices=[]
		for p,i,c in X_layer_indices:
			if c==0:
				phrases_with_count_zero_in_X_layer_indices.append(" ".join(p))
			elif  c==1:
				answer.append((" ".join(p),i[0]))
				completed_indices.extend(i[0])
			else:
				i = [elist for elist in i if not set(elist).intersection(set(completed_indices))]
				c = len(i)
				new_X_layer_indices.append((p,i,c))
		if X_layer_indices == new_X_layer_indices:
			break
		X_layer_indices = new_X_layer_indices
	#print("X_sorted_list",X_sorted_list)
	#print("H_parserid_wordid", H_parserid_wordid)
	for e,n in enumerate(X_layer_indices):
		for l in n[1]:
			for entry in X_sorted_list:
				if l[0]==entry[2]:
					X_layer_indices[e] = (n[0],n[1],l[0])
	phrases_with_multiple_occurence_unresolved = X_layer_indices
	# print("In extracting_x_layer_ids")
	return answer, phrases_with_count_zero_in_X_layer_indices, phrases_with_multiple_occurence_unresolved;

def phrase_occuring_indices_count(sorted_list,hwords_list):
	# print("sorted_list,hwords_list",sorted_list,hwords_list)
	temp_layer_indices=[]
	for item in sorted_list:
		it = item[1].strip()
		it = [x for x in it.split() if '@' not in x if not x.startswith('-')]
		if it:
			item_occurence_index = [range(r+1,r+1+len(it)) for r,val in enumerate(hwords_list) if hwords_list[r:r+len(it)]==it]
			count=len(item_occurence_index)
			if (it, item_occurence_index, count) not in temp_layer_indices:
				temp_layer_indices.append((it, item_occurence_index, count))
	# print("Inside phrase_occuring_indices_count")
	# print (temp_layer_indices,hwords_list)
	return temp_layer_indices;

def main():
	global original_cl_words
	sym=['.',',',';',':','-',')','?']
	manual_word = []
	Hwid_word = []
	global H_parserid_wordid
	# for line in open("manual_word.dat","r") :
	# 	line = line.strip().split()
	# 	manual_word.append((line[1], str(conv_to_canonical(line[2][:-1]))))
	x6 = check_file_to_be_read("H_wordid-word_mapping.dat")
	if x6!=1 and x6!=2:
		for line in open("H_wordid-word_mapping.dat","r"):
			line = line.strip().split()
			Hwid_word.append((line[1], str(conv_to_canonical(line[2].strip(')')))))
	x7 = check_file_to_be_read("H_parserid-wordid_mapping.dat")
	if x7!=1 and x7!=2:
		with open("H_parserid-wordid_mapping.dat") as g:
			H_parserid_wordid = g.read().strip().split('\n')
		H_parserid_wordid = [p.strip(')').split('\t') for p in H_parserid_wordid ]
		H_parserid_wordid = [(q[1].strip('P'),q[2]) for q in H_parserid_wordid]
		temp3 = zip(H_parserid_wordid, Hwid_word)
		for num,val in enumerate(H_parserid_wordid):
			if temp3[num][0][1]==temp3[num][1][0]: #val[0][1]==val[1][0]:
				H_parserid_wordid[num] = (int(temp3[num][0][0]),int(temp3[num][1][0]),temp3[num][1][1])
	# print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",H_parserid_wordid)

 # Writing English sentence to csv file #
	for line in open("English_sentence.dat",'r'):
		f3.write("English Sent: "+line.strip().split("\"")[1]+"\n")
	f11.write("English Sent:")
	for eid, eword in enumerate(line.strip().split("\"")[1].split()):
		f11.write(" "+str(eid+1))

 # Writing Hindi Translation to csv file #
	try:
		x8 = check_file_to_be_read("H_sentence_updated")
		if x8!=1 and x8!=2:
			f_name = "H_sentence_updated"
		else:
			x9 = check_file_to_be_read("H_sentence")
			if x9!=1 and x9!=2:
				f_name = "H_sentence"
		for line in open(f_name,"r"):
			f3.write("Hindi Tansl: "+line.strip()+"\n")
			f11.write("\nHindi Tansl:")
		for hid, hword in enumerate(line.strip().split()):
			f11.write(" "+str(hid+1))


	except (KeyError):
		print("Encoding issue in hindi translation.")
 
# Writing Anusaaraka's Translation to csv file #
	# f3.write("Anu Translation: ")
	# # f11.write("\nAnu Translation: ")
	# missing_root=[]
	# # pick words which have missing roots in Anusaaraka
	# for line in open("errors.txt"):
	# 	if line.startswith("Warning: root missing for"):
	# 		missing_root.append(line.strip().split()[4])
 
	# for line in open("hindi_sentence.dat"):
	# 	hwords=[h.strip() for h in line.strip().split()]
	# 	hwords=[h1.strip("".join(sym)) for h1 in hwords]
	# 	hwords_for_ids=[s[len('PropN-'):-len('-PropN')] if s.startswith('PropN-') and s.endswith('-PropN') else s for s in hwords]
	# 	anu_translation_h_ids = [str(hid+1) for hid,hword in enumerate(hwords_for_ids)]
	# f11.write(" ".join(a for a in anu_translation_h_ids))
	# print ("hwords",hwords)
	# for i in hwords: 
	# 	#print(i,missing_root)
	# 	if any([i in word for word in missing_root]):    
	# 		f3.write(" "+i)
	# 	else:
	# 		f3.write(" "+i)
	# print ("anu_translation_h_ids", anu_translation_h_ids)

# Writing A layer to csv file #
	f1.write("$ENG_A_ENG$#")
	for line in open("English_sentence.dat",'r'):
		f1.write("#".join(['$ENG_'+x+'_ENG$' for x in line.strip().split("\"")[1].split()]))
		arr_words=['$ENG_'+x+'_ENG$' for x in line.strip().split("\"")[1].split()]
	f11.write("\nA")
	for eid, eword in enumerate(line.strip().split("\"")[1].split()):
		f11.write("#"+str(eid+1))
	f11.write("\nK")
	for eid, eword in enumerate(line.strip().split("\"")[1].split()):
		f11.write("#"+str(eid+1))

 # Writing K layer to csv file #
	unsorted=[]
	f1.write("\n$ENG_K_ENG$")
	for line in open("id_Apertium_output_with_grp.dat",'r'):
		l= replace_uneven_spaces_by_a_single_space(line)
		id=int(l.strip().split()[1])
		if id<500:
			unsorted.append((id,l.strip().split(" ",2)[2].split(')')[0].strip(),'0'))
	K_sorted=sorted(unsorted)
	if K_sorted[-1][0]==10000:
		max_len=K_sorted[-2][0]
	if K_sorted[-1][0]==10000:
		max_len=K_sorted[-2][0]
	else:
		max_len=K_sorted[-1][0]
	
	K_sorted = [(s[0],s[1].replace("@PUNCT-OpenParen@PUNCT-OpenParen","((").replace("@PUNCT-ClosedParen@PUNCT-ClosedParen","))"),s[2]) for s in K_sorted]
	# create_lists_with_hindi_word_ids(K_sorted_for_ids, hwords, 'K', max_len)	
	
	# Filling the list for missing word_ids
	K_sorted_filled=[]
	count=0
	for i in range(len(K_sorted)):
		count=count+1
		if count<K_sorted[i][0]:
			K_sorted_filled.append((count,'-'))
			count=count+1
		K_sorted_filled.append(K_sorted[i])
	
	write_layer_to_file(K_sorted_filled,1)
 
 # Writing L,M layers to csv file #
	phrasal_layers('L',"word-alignment.dat",Hwid_word)
	phrasal_layers('M',"word-alignment-hi-en.dat",Hwid_word)

 # Writing Nth,Oth layer to csv file #
 	hwords1=[]
	with open("manual_word.dat") as g:
		hwords1 = g.read().strip().split('\n')
 		hwords1 = [d.strip().split()[2].strip(')') for d in hwords1 if not d.strip().split()[2].startswith('@PUNCT')]	 
	#print("hwords1",hwords1)
	hwords1=[h.strip("".join(sym)) for h in hwords1]
	hwords1=[str(conv_to_canonical(i)) for i in hwords1]
	fact_to_match3 = r"\(alignment \(anu_id (.*)\) \(man_id (.*)\) \(anu_meaning (.*)\) \(man_meaning (.*)\)\)"	
	Nth_Oth_P1th_layers('N', "parser_alignment.dat", fact_to_match3, max_len, hwords1, H_parserid_wordid)
	Nth_Oth_P1th_layers('O', "word_alignment_tmp.dat",fact_to_match3, max_len, hwords1, H_parserid_wordid)

 # Writing Pth layer to csv file #
	P_sorted=[]
	P_sorted_filled=[]
	P_layer_indices=[]
	P_sorted_with_brackets=[]
	f1.write("\n$ENG_P_ENG$")
	for line in open ("word_alignment.dat","r"):
		l=line.strip().split(' - ')
		anu_id = re.findall("\d+", l[0])[0]
		manual_word = l[1].split(re.findall("\d+", l[1])[0])[1].strip().split(")")[0]
		manual_word_with_brackets = manual_word.replace("@PUNCT-OpenParen","(").replace("@PUNCT-ClosedParen",")")
		man_id = re.findall("\d+", l[1])[0]
		# print (manual_word,manual_word_with_brackets)
		P_sorted_with_brackets.append((int(anu_id),manual_word_with_brackets,int(man_id)))
		if manual_word.startswith("@PUNCT"):
			x=manual_word.split()
			x=[i for i in x if "@" not in i]
			P_sorted.append((int(anu_id)," ".join(x).strip(),int(man_id)))
		else:
			P_sorted.append((int(anu_id),manual_word.split("@")[0].strip(), int(man_id)))
	P_sorted.sort()
	P_sorted_filled=create_dummy_list(max_len,3)
	create_lists_with_hindi_word_ids(P_sorted, hwords1, 'P', max_len, H_parserid_wordid)
	for w in P_sorted_with_brackets:
		for s in P_sorted_filled:
			if s[0]==w[0]:
				P_sorted_filled[P_sorted_filled.index(s)]=(s[0],w[1].strip(),w[2])
	write_layer_to_file(P_sorted_filled,1)

	#writing P1th layer 
	fact_to_match4 = r"\(alignment_info \(anu_id (.*)\) \(anu_meaning (.*)\) \(man_id (.*)\) \(man_meaning (.*)\) \(man_group_ids (.*)\)\)"
	Nth_Oth_P1th_layers('P1', "corrected_pth.dat", fact_to_match4, max_len, hwords1, H_parserid_wordid)

 # Making list of clauses for each sentence: clause boundary
	list_of_clauses=[]
	x2 = check_file_to_be_read("finite_clause.dat")
	if x2!=1 and x2!=2:
		for line in open("finite_clause.dat",'r'):
			fact_to_match=r"\(clause \(cl_id (.*)\) \(cl_words (.*)\) \(cl_member_ids (.*)\) \(finite_verb_grp (.*)\) \(finite_verb_grp_ids (.*)\) \(finite_verb_root (.*)\) \(finite_verb_root_id (.*)\) \(finite_verb_tam (.*)\)\)"
			m=re.match(fact_to_match,line)
			cl_id, cl_words, cl_member_ids, finite_verb_grp, finite_verb_grp_ids, finite_verb_root, finite_verb_root_id, finite_verb_tam=[m.group(i) for i in range(1,9)]
			cl_words = [str(conv_to_canonical(w)) for w in cl_words.strip().split()]
			cl_member_ids = [int(i) for i in cl_member_ids.strip().split()]
			finite_verb_grp = finite_verb_grp.strip().split("_")
			finite_verb_grp_ids = [int(i) for i in finite_verb_grp_ids.strip().split()]
			list_of_clauses.append([finite_verb_grp, finite_verb_grp_ids, cl_words, cl_member_ids])
			
			for i,word in enumerate(cl_words): 
				if word[-1] in sym: 
					cl_words[i] = word[:-1]
			
	list_of_aligned_clauses=[]
	sym=['.',',',';',':','-',')',]
	
	x3 = check_file_to_be_read("Aligned_clauses")
	if x3!=1 and x3!=2:
		for line in open("Aligned_clauses.dat",'r'):
			fact_to_match1=r"\(EClause-HClause \(EClauseIds (.*)\) \(EClauseMemberIds (.*)\) \(EClauseMemberWords (.*)\) \(HClauseIds (.*)\) \(HClauseMemberIds (.*)\) \(HClauseMemberWords (.*)\)\)"
			m1=re.match(fact_to_match1,line)
			EClauseIds, EClauseMemberIds, EClauseMemberWords, HClauseIds, HClauseMemberIds, HClauseMemberWords=[m1.group(i) for i in range(1,7)]
			EClauseMemberIds = [int(i) for i in EClauseMemberIds.strip().split()]
			EClauseMemberWords = [str(conv_to_canonical(w)) for w in EClauseMemberWords.strip().split()]
			HClauseMemberIds = [int(i) for i in HClauseMemberIds.strip().split()]
			HClauseMemberWords = [str(conv_to_canonical(w)) for w in HClauseMemberWords.strip().split()]
			list_of_aligned_clauses.append((EClauseMemberIds, EClauseMemberWords, HClauseMemberIds, HClauseMemberWords))
			
			for i,word in enumerate(EClauseMemberWords): 
				if word[-1] in sym: 
					EClauseMemberWords[i] = word[:-1]
	# print ("LLLLLLLLLLLLLLLLLList of aligned clauses", list_of_aligned_clauses)
 # Writing Rth layer to the file
	f1.write("\n$ENG_R_ENG$")
	temp_fact=[]
	gita_ras_ratnakar_dic_facts=create_dummy_list(max_len,4)
	
	x1 = check_file_to_be_read("R_layer_final_facts.dat")
	if x1!=1 and x1!=2:
		for line in open("R_layer_final_facts.dat",'r'):
			fact_to_match=r"\(Eid-Eword-Hid-Hword \(E_id (.*)\) \(E_word (.*)\) \(H_id (.*)\) \(H_word (.*)\)\)"
			m=re.match(fact_to_match,line)
			e_id,e_word,h_id,h_word=[m.group(i) for i in range(1,5)]
			e_id=[int(i) for i in e_id.split()]
			e_word=e_word.split()
			anu_head_id, anu_rest_ids, h_id=[e_id[-1],e_id[:-1], h_id]
			manual_word=h_word.replace("_"," ")
			temp_fact.extend(h_word.split())
			for k in gita_ras_ratnakar_dic_facts:
				if k[0]==anu_head_id:
					gita_ras_ratnakar_dic_facts[gita_ras_ratnakar_dic_facts.index(k)]=(k[0],manual_word,"R_layer",h_id)
					
				else:
					for i in anu_rest_ids:
						if k[0]==int(i):
							gita_ras_ratnakar_dic_facts[gita_ras_ratnakar_dic_facts.index(k)]=(k[0],"*", k[2],k[3]) 
	#print ("gita_ras_ratnakar_dic_facts", gita_ras_ratnakar_dic_facts)
	gita_ras_ratnakar_dic_facts_columns_swapped = [(c[0],c[1],c[3] if c[3]!='-' else '0' ,c[2]) for c in gita_ras_ratnakar_dic_facts]
	#print ("gita_ras_ratnakar_dic_facts_columns_swapped", gita_ras_ratnakar_dic_facts_columns_swapped)
	create_lists_with_hindi_word_ids(gita_ras_ratnakar_dic_facts_columns_swapped, hwords1, 'R', max_len, H_parserid_wordid)
	# print("R                   ",gita_ras_ratnakar_dic_facts)
	temp2=[]
	for i,j in zip(gita_ras_ratnakar_dic_facts, P_sorted_filled):
		if i[0]==j[0] :
			if j[1]=="-" or j[1]==" ": continue
			else:
				for s in H_parserid_wordid:
					if s[1] == j[2]: 
						if i[1]=="-":
							result = check_word_in_list_of_clauses(list_of_clauses, j[1].strip(), s[0], 'P')
							# print(result)
							if result == 1:
								r = check_left_over_word_in_list_of_aligned_clauses(list_of_aligned_clauses, j[1].strip(),j[0], s[0], 'P')
								# print (r)
								n = ''
								l = j[1].strip().split()
								if len(l)>1: n = "_".join(l)
								else: n = j[1].strip()
								if r ==1: 
									if n not in " ".join(temp_fact):
										gita_ras_ratnakar_dic_facts[gita_ras_ratnakar_dic_facts.index(i)]=(i[0],j[1].strip(),"Pth_layer")
									else:
										gita_ras_ratnakar_dic_facts[gita_ras_ratnakar_dic_facts.index(i)]=(i[0],i[1], "Pth layer: no change in R")
						elif len(j[1].split()) > 1 and len(i[1].split()) >1 and i[1]==j[1].split()[0] :
							# wrd = [w for w in j[1].split()][1:]
							if j[1].split()[1] not in temp_fact:
								gita_ras_ratnakar_dic_facts[gita_ras_ratnakar_dic_facts.index(i)]=(i[0],j[1].strip(),"Pth_layer: first word same as R")
							else:
								gita_ras_ratnakar_dic_facts[gita_ras_ratnakar_dic_facts.index(i)]=(i[0],i[1], "Pth layer: not copied words to R")
						elif  i[1]!=j[1].split()[0] and i[1] in j[1]:
							result1 = check_left_over_word_in_list_of_aligned_clauses(list_of_aligned_clauses, j[1].strip(), j[0], s[0], 'P')
							# print(result1)
							t = "_".join(j[1].strip().split()[1:])
							if result1 == 1 and t not in temp_fact:	
								gita_ras_ratnakar_dic_facts[gita_ras_ratnakar_dic_facts.index(i)]=(i[0],j[1].strip(),"Pth_layer: extra words") 
							else:
								gita_ras_ratnakar_dic_facts[gita_ras_ratnakar_dic_facts.index(i)]=(i[0],i[1], "Pth layer: not copied extra words") 
						else: continue

						break

			
				
	# print ("____________________________________________",P_sorted_filled)
						
	# print("R after P                   ",gita_ras_ratnakar_dic_facts)
	

	PropNouns = [(int(tup[0]),tup[1].strip().replace('@PropN-@','').replace('-@PropN','')) for tup in K_sorted_filled if '@PropN' in tup[1]]
	symbol_words = [(int(tup[0]),tup[1].strip().replace('@','')) for tup in K_sorted_filled if tup[1].startswith('@')]
	# print("Othhhhhhhhhhhhhhhhhhhhhhhhhhhh:", Oth)
	for i,j in zip(gita_ras_ratnakar_dic_facts, Oth):
		ind = gita_ras_ratnakar_dic_facts.index(i)
		if i[0]==j[0]: 
			if i[1]=="-" and j[1]!="-" and j[1]!=' ': 
				morph_roots_j1 = list(set(map(lambda x: x.split("<")[0].strip("$").strip("*"), check_morph(conv_to_canonical(j[1])).split("/")[1:])))
				morph_roots_j1 = [str(k) for k in morph_roots_j1]
				morph_roots_j2 = list(set(map(lambda x: x.split("<")[0].strip("$").strip("*"), check_morph(conv_to_canonical(j[2])).split("/")[1:])))
				morph_roots_j2 = [str(k) for k in morph_roots_j2]
				# print ("RRRRRRRoots",morph_roots_j1, morph_roots_j2)	
				for root in morph_roots_j1: 
					if root in morph_roots_j2:
						for s in H_parserid_wordid:
							if s[1] == j[3]:
								result = check_word_in_list_of_clauses(list_of_clauses, j[1].strip(), s[0], 'O')
								# print (result)
								if result== 1:
									r1 = check_left_over_word_in_list_of_aligned_clauses(list_of_aligned_clauses, j[1].strip(), j[0], s[0], 'O')
									# print (r1)
									n1 = ''
									l1 = j[1].strip().split()
									if len(l1)>1: n1 = "_".join(l1)
									else: n1 = j[1].strip()
									if r1 == 1 and n1 not in " ".join(temp_fact):
										gita_ras_ratnakar_dic_facts[ind]=(i[0],j[1].strip(),"Oth_layer")
									else:
										gita_ras_ratnakar_dic_facts[ind]=(i[0],i[1],"Oth_layer: no change in R")
								break
		# print ("VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV",j[3],i[1])
					elif len(PropNouns)>0:
							for q in PropNouns:
								if i[0]==q[0] and q[1][1:] in j[2]: 
									gita_ras_ratnakar_dic_facts[ind]=(i[0],j[1].strip(),"Oth_layer")
									break
					elif len(symbol_words)>0:
							for s1 in symbol_words:
								if "PUNCT" in s1[1]: continue
								if i[0]==s1[0] and s1[1][1:] in j[2]: 
									gita_ras_ratnakar_dic_facts[ind]=(i[0],j[1].strip(),"Oth_layer")
									break
					else: continue
		if len(j[1].split())>0 and i[1]==j[1].split()[0] :   #to include vibhaktis and other extra words
			if j[1].split()[0]=="-" or i[2].startswith("Pth") or i[2].startswith("Oth") :
				continue
			if len(i[1].strip()) < len(j[1].strip()) and "_".join(j[1].strip().split()[1:]) not in temp_fact: entry=j[1]
			else:	entry=i[1]
			gita_ras_ratnakar_dic_facts[gita_ras_ratnakar_dic_facts.index(i)]=(i[0],entry,"Oth_layer:extra words")

	#print("after O                   ",gita_ras_ratnakar_dic_facts)
	write_layer_to_file(gita_ras_ratnakar_dic_facts,1)
	
	f1.write("\n$ENG_Domain_Spec_Dict_ENG$")
	x5 = check_file_to_be_read("corpus_specific_dic_facts_for_one_sent.dat")
	corpus_specific_dict = create_dummy_list(max_len,4)
	if x5!=1 and x5!=2:
		temp_fact=[]
		for line in open("corpus_specific_dic_facts_for_one_sent.dat",'r'):
			fact_to_match2=r"\(Edict-Hdict \(E_id (.*)\) \(E_word (.*)\) \(H_id (.*)\) \(H_word (.*)\)\)"
			m=re.match(fact_to_match2,line)
			e_id,e_word,h_id,h_word=[m.group(i) for i in range(1,5)]
			e_id=[int(i) for i in e_id.split()]
			e_word=e_word.split()
			anu_head_id, anu_rest_ids, h_id=[e_id[-1],e_id[:-1], h_id]
			manual_word=h_word.replace("_"," ")
			temp_fact.extend(h_word.split())
			for ind,s in enumerate(corpus_specific_dict):
				if s[0]==anu_head_id:
					corpus_specific_dict[ind]=(s[0]," ".join(e_word),h_id,manual_word)
					
				else:
					for j in anu_rest_ids:
						if s[0]==int(j):
							corpus_specific_dict[ind]=(s[0],s[1], s[2],"*")

	write_layer_to_file(corpus_specific_dict,3)
	f1.close()
if __name__ == "__main__":main()
