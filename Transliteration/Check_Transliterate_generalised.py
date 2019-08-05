#python Check_Transliterate_generalised.py -f E_sentence_file H_sentence_file
#import check_transliteration.py as ct
import sys, string, commands, os
tmp_path="/".join(sys.argv[2].split("/")[:-1])


def remove_punct_from_word(word):
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

def chk_trans_from_files():
	e_words = extract_only_words_from_sent(sys.argv[2])
	e_words = e_words[1:]
	upper_words = [word for word in e_words if word[0].isupper()]
	#print(upper_words)
	h_words = extract_only_words_from_sent(sys.argv[3])
	#print(h_words)
	for e in upper_words:
		for h in h_words:
			#ct.check(e,w)
			call_roja_prog = "python /home/kishori/a/Alignment1/Transliteration/check_transliteration.py "+ e + " " + h + " /home/kishori/a/Alignment1/Transliteration/Sound-dic.txt"
			#print(e,h,commands.getoutput(call_roja_prog))
			if commands.getoutput(call_roja_prog)=="Given word is transliterate word":
				#print(call_roja_prog)
				print(e,h)
				with open(tmp_path+"/Roja_chk_transliterated_words.dat", "a") as f:
					f.write("(E_word-H_word\t"+ e + "\t"+ h + ")\n")
if sys.argv[1]=="-f":		
	chk_trans_from_files()
