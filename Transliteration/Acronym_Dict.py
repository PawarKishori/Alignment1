
# coding: utf-8

# In[49]:


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
        while "" in plain_words:    #If E_sentence/H_sentence contains 2 sentence remove an empty word
            plain_words.remove("")
    return(plain_words)
def acronym():
    acr=[]
    e_words=extract_only_words_from_sent(e_sen)
    for i in e_words:
        if i.isupper() :
            acr.append(i)
    return acr
def find_acronym():
    final=[]
    a=acronym()
    #print(a)
    h_word_list=[]
    e_alpha=[]
    h_alpha=[]
    f = open(Acro_Dict, 'r')
    line= f.read()
    lines= line.split('\n')
    for i in lines :
        str1=i.split("\t")
        e_alpha+=str1[::2]  #list slicing 
        h_alpha+=str1[1::2]
    h_words=extract_only_words_from_sent(h_sen)
    #print(h_words)
    for i in a :
        h_word=""
        temp=[]
        for j in i :
            [temp.append(h_alpha[k]) for k in range(len(e_alpha)) if j == e_alpha[k]]
        h_word="".join(temp)
        h_word_list.append(h_word)
        for h in h_words :
            if h == h_word :
                temp_str=i+" <> "+h
                if temp_str not in final:
                    final.append(temp_str)

    for i in final :
        print("Acronym:",i)
        fi.write(i+"\n")


import string,sys, os
e_sen=sys.argv[1]
h_sen=sys.argv[2]
dict_path = os.getenv('HOME_alignment')+'/Transliteration/dictionary'
Acro_Dict=dict_path+"/Acronym_Dict"
fi=open(dict_path+"/lookups/Lookup_transliteration_acronym" + e_sen + ".txt", "w")
#tmp_path="/".join(sys.argv[2].split("/")[:-1])
#print(tmp_path)
#fi=open(tmp_path+"/Acronym.txt",'w+')
find_acronym()

