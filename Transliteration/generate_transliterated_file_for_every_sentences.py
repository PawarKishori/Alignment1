
#def distribute_transliterated_entries_in_sent_folder():


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


import sys, os
import string
e_filename = sys.argv[1]

#lookup_dict_path = os.getenv('HOME_alignment')+'/Transliteration/dictionary/lookups'+'/Lookup_transliteration_final_AI_all_eng.txt'
lookup_dict_path = os.getenv('HOME_alignment')+'/Transliteration/dictionary/lookups/'+ sys.argv[2]

t_dict={}
with open( lookup_dict_path ,"r") as f:
    t = f.read().split("\n")
    while "" in t:
        t.remove("")
    for i in t:
        t_dict[i.split(" <> ")[0]]=i.split(" <> ")[1]
        #print(i.split(" <> ")[1])#=i.split(" <> ")[1]

sent_num = sys.argv[3]

sent_tmp_path = os.getenv('HOME_anu_tmp')+'/tmp/'+ e_filename + '_tmp/' + sent_num
print(sent_tmp_path)

with open(sent_tmp_path+"/E_sentence","r") as f:
   ewords =extract_only_words_from_sent( f.read().strip("\n") )

with open(sent_tmp_path+"/H_sentence","r") as f:
   hwords = extract_only_words_from_sent(f.read().strip("\n"))



#print(ewords)
#print(hwords)
#print(t_dict)

#print(lookup_dict_path)


import os
def add(fact_items,string,filename):
    #print("inside writefact.add")
    #print(fact_items)
    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename,"a") as f:
        for line in fact_items:
            tokens=len(fact_items)
            fact="("+string
            for i,a in enumerate(line):
                fact=fact+"\t"+str(a)
                #print(fact)
            fact=fact+")\n"
            #print(fact)
            f.write(fact)
            #print("File created")


t_pair=[]
for i in ewords:
    if i in t_dict.keys():
        if t_dict[i] in hwords:
            print(i,t_dict[i])
            t_pair.append([i,t_dict[i]])

print(sent_num)
print(t_pair)
print("____________________________________________________________________")
tmp_dir = os.getenv('HOME_anu_tmp')+'/tmp/'+ e_filename + '_tmp/' + sent_num

add(t_pair, "E_word-H_word" , tmp_dir + "/Tranliterated_words_first_run.dat" )




