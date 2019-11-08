import os,sys,string,subprocess,re
def remove_punctuation(sentence):
    sentence=sentence.replace("'s","")#.replace("s'","")
    #re.sub("(?<=[a-z])'s(?=[a-z])", "", sentence)
    sentence=sentence.translate(sentence.maketrans('', '', string.punctuation))
    return sentence

def sentence_to_words(sentence):
    sentence=remove_punctuation(sentence)
    words=sentence.split(" ")
    words[-1]=words[-1].rstrip("\n")
    return words
'''def lower_e_words_of_list(e_list):
    e_list=[x.lower() for x in e_list]
    return e_list'''
def eng_root_word_from_morph(e_word):
    cmd='echo "'+e_word+'" | lt-proc -ac $HOME_anu_test/apertium/en.morf.bin | apertium-retxt'
#     cmd1 = 'echo "work"'
    #print(cmd)
    output=subprocess.check_output(cmd, shell=True)
    final=output.decode("utf-8")
    #print(final)
    root=re.findall(r'\/(.*?)\<',final)
    if len(root)==0 :
        root.append(e_word)
 
    if(len(set(root))==1):
          e_root_word=root[0]
    else:
          return -1
    #print(e_root_word)
    return e_root_word

def hin_root_word_from_morph(h_word):
    cmd='echo "'+h_word+'" | lt-proc -ac $HOME_anu_test/bin/hi.morf.bin | apertium-retxt'
    output=subprocess.check_output(cmd, shell=True)
    final=output.decode("utf-8")
    #print(final)
    root=re.findall(r'\/(.*?)\<',final)
    if len(root)==0 :
        root.append(h_word)
    #listChar = ['z','z','z','z']
 
    if(len(set(root))==1):
          h_root_word=root[0]
    else:
          return -1
    return h_root_word
def root_for_the_sentence(e_sentence_file,h_sentence_file):
    e_roots_with_e=[]
    h_roots_with_h=[]
    #corpus="ai1E"
    #temp_dir=os.getenv("HOME_anu_tmp")+"/tmp/"+corpus+"_tmp/"+"2.88/"
    #temp_dir+"H_sentence"
    e_sentence=open(e_sentence_file,"r").read()
    h_sentence=open(h_sentence_file,"r").read()
    e_words=sentence_to_words(e_sentence)
    h_words=sentence_to_words(h_sentence)
    for e,h in zip(e_words,h_words) :
        e_root=eng_root_word_from_morph(e)
        h_root=hin_root_word_from_morph(h)
        e_root_word_pair=[]
        if e_root != -1 :
            e_root_word_pair.append(e_root)
            e_root_word_pair.append(e)
            e_roots_with_e.append(e_root_word_pair)
#     print(e_roots_with_e)
        h_root_word_pair=[]
        if h_root != -1 :
            h_root_word_pair.append(h_root)
            h_root_word_pair.append(h)
            h_roots_with_h.append(h_root_word_pair)
#     print(h_roots_with_h)
#     print(e_roots_with_e)
    return e_roots_with_e,h_roots_with_h

    

    #print(h_words)


def create_dictionary_from_exceptional_dictionary(filename):
    ex = open(filename, "r")
    ex_dic = {}
    for line in ex:
        ex_lst = line.strip().split('\t')
        ex_dic[ex_lst[0]] = ex_lst[1]
    return(ex_dic)
def check_from_exceptional_dic(ex_dic, e, h):
    flag = 0
    dic_stack = []
    
    for key in ex_dic:
        ex_list = ex_dic[key].split('/')
        for each in ex_list:
            val = key + ' ' + each
            dic_stack.append(val)
    for i in range(0, len(dic_stack)):
        e_key = dic_stack[i].split()
        if e_key[0] == e and e_key[1] == h:
            flag = 1
            break
    if flag == 1:

        tr.write(e+" <> "+h+"\n")
except_dict=create_dictionary_from_exceptional_dictionary(os.getenv("HOME_alignment")+"/Transliteration/dictionary/Exception-dic.txt")
def check_transliterate():
    for e in e_roots_with_e:
        for h in h_roots_with_h:
            #print(e[0],h[0])
            check_from_exceptional_dic(except_dict,e[0],h[0])
            call_roja_prog = "python "+os.getenv("HOME_alignment")+"/Transliteration/check_transliteration.py "+ e[0] + " " + h[0] +" "+ os.getenv("HOME_alignment")+"/Transliteration/dictionary/Sound-dic.txt"
            #print(call_roja_prog)
            if subprocess.getoutput(call_roja_prog)=="Given word is transliterate word":
                    print(e[1]," <> ",h[1])
                    tr.write(e[1]+" <> "+h[1]+"\n")


e_sentence_file=sys.argv[1]#temp_dir+"E_sentence"
h_sentence_file=sys.argv[2]
temp=sys.argv[1].split("/")[:-1]
temp_path="/".join(temp)
e_roots_with_e,h_roots_with_h=root_for_the_sentence(e_sentence_file,h_sentence_file) 
#print(e_roots_with_e) 
#print(h_roots_with_h) 
tr=open(temp_path+"/Tranliterated_words_2nd_run.dat","a")
check_transliterate()
