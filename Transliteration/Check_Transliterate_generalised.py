#python Check_Transliterate_generalised.py -f E_sentence_file H_sentence_file
#import check_transliteration.py as ct
import sys, string, commands, os
tmp_path="/".join(sys.argv[2].split("/")[:-1])


def remove_punct_from_word(word):
	#print(word, word.strip(string.punctuation))
	return(word.strip(string.punctuation))

def extract_only_words_from_sent(sent_file):
	with open(sent_file, 'r') as f:
		sent = " ".join(f.read().split()).strip("\n") #If sent contains extra spaces, cleaning it
		all_words = sent.split(" ")
		#print(all_words)
		plain_words=[]
		for word in all_words:
			plain_words.append(remove_punct_from_word(word))
		#print(plain_words)
		while "" in plain_words:		#If E_sentence/H_sentence contains 2 sentence remove an empty word
			plain_words.remove("")
	return(plain_words)

def create_dictionary_from_exceptional_dictionary(filename):
	ex = open(filename,"r")
	ex_dic = {}
	for line in ex :
		ex_lst = line.strip().split('\t')
		ex_dic[ex_lst[0]] = ex_lst[1]
	return(ex_dic)

def check_from_exceptional_dic(ex_dic, e,h):
	flag=0
	dic_stack=[]
	with open(tmp_path+"/Roja_chk_transliterated_words.dat", "a") as f:
		for key in ex_dic:
			ex_list = ex_dic[key].split('/')
			for each in ex_list:
				val = key + ' ' + each
				dic_stack.append(val)
		for i in range(0, len(dic_stack)):
			e_key = dic_stack[i].split()
			if e_key[0]==e and e_key[1]==h :
				flag=1
				break
		if flag == 1 :
			print(e,h)
			f.write("(E_word-H_word\t"+ e + "\t"+ h + ")\n")

def chk_trans_from_files():
	e_words = extract_only_words_from_sent(sys.argv[2])
	e_words = e_words[1:]
	#print(e_words)
	upper_words = [word for word in e_words if word[0].isupper()]
	#print(upper_words)
	h_words = extract_only_words_from_sent(sys.argv[3])
	#print(h_words)
	with open(tmp_path+"/Roja_chk_transliterated_words.dat", "a") as f:
		for e in upper_words:
			for h in h_words:
				check_from_exceptional_dic(excep_dic, e,h)
				#ct.check(e,w)
				call_roja_prog = "python /home/kishori/a/Alignment1/Transliteration/check_transliteration.py "+ e + " " + h + " /home/kishori/a/Alignment1/Transliteration/dictionary/Sound-dic.txt"
				#print(e,h,commands.getoutput(call_roja_prog))
				if commands.getoutput(call_roja_prog)=="Given word is transliterate word":
					#print(call_roja_prog)
					print(e,h)
					f.write("(E_word-H_word\t"+ e + "\t"+ h + ")\n")

excep_dic = create_dictionary_from_exceptional_dictionary("/home/kishori/a/Alignment1/Transliteration/dictionary/Exception-dic.txt")

if sys.argv[1]=="-f":		
	if os.path.exists(tmp_path+"/Roja_chk_transliterated_words.dat"):
		os.remove(tmp_path+"/Roja_chk_transliterated_words.dat")
	chk_trans_from_files()
