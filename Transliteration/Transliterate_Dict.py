#This program creates a transliteration dictionary for entire corpus once.

#This program calls Roja mam's program which runs in python2

#import check_transliteration.py as ct                          ##Pending task to do, once roja mam completes this will be complete


def remove_punct_from_word(word):
    word=word.translate(word.maketrans('','',string.punctuation))
    return(word)


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
            #print(e,h)
        str_temp=e +" <> "+ h
        if str_temp not in final :
            final.append(str_temp)


def transliterate_Dict():
    e_lines=corpus_to_sentence(e_corpus)
    h_lines=corpus_to_sentence(h_corpus)
    for e_line,h_line in zip(e_lines,h_lines):
        e_words=extract_only_words_from_sent(e_line)
        h_words=extract_only_words_from_sent(h_line)
        e_words = e_words[1:]
        #print(e_words)
        upper_words = [e_word for e_word in e_words if e_word[0].isupper()]
        #print(upper_words)
        for e in upper_words:
            for h in h_words:
                check_from_exceptional_dic(excep_dic, e,h)
            #ct.check(e,w)
                #print(e,h)
                call_roja_prog = "python "+roja_prog_path+" "+ e + " " + h +" "+ dict_path+"/Sound-dic.txt"
                #print(e,h,commands.getoutput(call_roja_prog))
                if subprocess.getoutput(call_roja_prog)=="Given word is transliterate word":
                    #print(call_roja_prog)
                    print(e,h)
                    str_temp=e +" <> "+ h
                    if str_temp not in final :
                        final.append(str_temp)
    for i in final:
        print(i)
        f.write(i+"\n")


import sys, string, os, itertools
import subprocess
e_corpus=sys.argv[1]
h_corpus=sys.argv[2]

roja_prog_path = os.getenv('HOME_alignment')+'/Transliteration/check_transliteration.py'
dict_path = os.getenv('HOME_alignment')+'/Transliteration/dictionary'
print(dict_path)

final=[]
f=open(dict_path+"/lookups/Lookup_transliteration_" + e_corpus + ".txt", "w")

excep_dic = create_dictionary_from_exceptional_dictionary(dict_path+"/Exception-dic.txt")
transliterate_Dict()
