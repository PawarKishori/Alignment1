###Pre-requisite: Roza ma'am's transliteration module###
import commands,os
cwd=os.getcwd().split('/')[-1]
print cwd
flag = 0
eids = []
hids = []
e_word = []
h_word = []
wx = []
wx_ids = []
eng = []
eng_ids = []
log = open("/home/kishori/a/tmp_anu_dir/tmp/BUgol2.2E_tmp/transliterate_log.dat",'a')
out = open("results_of_transliteration.dat",'w')
try :
	inp = open("E_sentence" , 'r')
except(IOError) :
	log.write(cwd + "\tE_sentence file is absent\n")
	exit()
try :
	wx_inp = open("H_sentence", 'r')
except(IOError) :
	log.write(cwd + "\tH_sentence file is absent\n")
	exit()
try :
	inp_id = open("E_wordid-word_mapping.dat" , 'r')
except(IOError) :
	log.write(cwd + "\tE_wordid-word_mapping.dat file is absent\n")
	exit()
try :
	wx_id = open("H_wordid-word_mapping.dat", 'r')
except(IOError) :
	log.write(cwd + "\tH_wordid-word_mapping.dat file is absent\n")
	exit()
###break the english sentene into words###
for sent in inp :
	sent = sent.replace("(","").replace(")","").replace(".","").replace(";","").replace(":","").replace("'","").replace("-","").replace(",","")
	word = sent.strip().split(" ")
	

###break the wx sentence into words###
for wxsent in wx_inp :
	wxsent = wxsent.replace("(","").replace(")","").replace(".","").replace(";","").replace(":","").replace("'","").replace("-","").replace(",","")
	wxword = wxsent.strip().split(" ")


###if the first letter of the word is capital indicates it is a proper noun###
for trans in word[1:] :
	
	if trans[0].isupper() :
###compare it to all the wx converted words###
		for cmpword in wxword :
###comapre the wx conversion and word with check_transliteration program###
				a = commands.getoutput(" python /home/kishori/a/Alignment1/Transliteration/check_transliteration.py " + trans + " " + cmpword + " /home/kishori/a/Alignment1/Transliteration/Sound-dic.txt ")
				if a == "Given word is transliterate word" :
					e_word.append(trans)
					h_word.append(cmpword)
					flag = 1

#print e_word
#print h_word
###find id of the english word and its correct wx conversion###
if flag == 1 :
	for form in inp_id :
		form=form.replace("(","").replace(")","")
		temp = form.strip().split("E_wordid-word")
		temp=temp[1].strip().split("\t")
		eng.append(temp[1])
		eng_ids.append(temp[0])
	for e in e_word :	
		for i in range(len(eng)) :
			if e == eng[i] :
				eids.append(eng_ids[i])
				print eids

	for h_form in wx_id :
		h_form=h_form.replace("(","").replace(")","")
		h_temp = h_form.strip().split("H_wordid-word")
		h_temp = h_temp[1].strip().split("\t")
		wx.append(h_temp[1])
		wx_ids.append(h_temp[0])
	for h in h_word :	
		for j in range(len(wx)) :
			if h == wx[j] :
				hids.append(wx_ids[j])
				print hids
				


							
							
###write it is the given format in results_of_check_transliteration###
	
	for i in range(len(eids)) :
		out.write( "(Edict-Hdict (E_id "+eids[i]+") (E_word "+e_word[i]+") (H_id "+hids[i]+") (H_word "+h_word[i]+"))\n")
		#out.write("(Transliterate_check (eid "+eid+")(hid "+hid+")(eword "+e_word+")(hword "+h_word+"))\n") 
		log.write(cwd + "\tFact Created\n")


