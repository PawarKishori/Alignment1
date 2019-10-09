#python Check_Transliterate_generalised.py -f E_sentence_file H_sentence_file
#import check_transliteration.py as ct
import sys, string, os, itertools, subprocess
tmp_path="/".join(sys.argv[2].split("/")[:-1])

def remove_punct_from_word(word):
    word=word.translate(word.maketrans('', '', string.punctuation))
    return word
def extract_only_words_from_sent(sent):
        all_words = sent.split(" ")
        #print(all_words)
        plain_words=[]
        for word in all_words:
            plain_words.append(remove_punct_from_word(word))
        #print(plain_words)
        while "" in plain_words:    #If E_sentence/H_sentence contains 2 sentence remove an empty word
            plain_words.remove("")
        return(plain_words)
def corpus_to_sentence(corpus):
    cor=open(corpus,"r")
    lines=cor.read().split("\n")
    return lines
def chk_trans_from_files():
    final=[]
    e_lines=corpus_to_sentence(e_corpus)
    h_lines=corpus_to_sentence(h_corpus)
    for e_line,h_line in zip(e_lines,h_lines[1:]):
        e_words=extract_only_words_from_sent(e_line)
        h_words=extract_only_words_from_sent(h_line)
        e_words = e_words[1:]
        #print(e_words)
        upper_words = [e_word for e_word in e_words if e_word[0].isupper()]
        #print(upper_words)
        for e in upper_words:
            for h in h_words:
            #ct.check(e,w)
                #print(e,h)
                call_roja_prog = "python "+os.getenv("HOME_alignment")+"/Transliteration/check_transliteration.py "+ e + " " + h + " "+os.getenv("HOME_alignment")+"/Transliteration/dictionary/Sound-dic.txt"
                
                if subprocess.getoutput(call_roja_prog)=="Given word is transliterate word":
                    #print(call_roja_prog)
                    #print(e,h)
                    str_temp=e +" <> "+ h
                    if str_temp not in final :
                        final.append(str_temp)
    with open(tmp_path+"/Transliteration_Lookup.txt", "w") as f :
        for i in final:
            print(i)
            f.write(i+"\n")
e_corpus=sys.argv[1]
h_corpus=sys.argv[2]
chk_trans_from_files()
