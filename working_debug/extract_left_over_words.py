
def create_dict(filename,string):
    with open(filename,"r") as f1:  
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        p2w = {} 
        for line in text:
            t = line.lstrip(string).strip(')').split("\t")
            p2w[int(t[1].lstrip("P"))] = t[2] 
    return(p2w)

def create_dict_org_word(filename,string):
    with open(filename,"r") as f1:  
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        #print(text)
        p2w = {} 
        for line in text:
            #print(line)
            t = line.lstrip(string).strip(')').split(" ")
            #print(t[1], t[3])
            p2w[int(t[1].lstrip("P"))] = t[3] 
    return(p2w)


import os, re, sys 
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'+sys.argv[1]+'_tmp/'+sys.argv[2]+'/'
 

eng_file = tmp_path + 'original_word.dat'
hindi_file = tmp_path + 'H_wordid-word_mapping.dat'

h2w  = create_dict(hindi_file,'H_wordid-word' )
print(h2w)

e2w = create_dict_org_word(eng_file, 'id-original_word')
print(e2w)

lo_hin = open(tmp_path + "hindi_leftover_ids.dat", "r").read()
lo_eng = open(tmp_path + "english_leftover_ids.dat","r").read()

hin_lo_dict={}
eng_lo_dict={}

#print(lo_hin.split())
with open(tmp_path + "hindi_leftover_words.dat","w") as f:
    tmp = []
    for i in lo_hin.split():
        print(int(i),h2w[int(i)])
        hin_lo_dict[int(i)]=h2w[int(i)]
        tmp.append(h2w[int(i)])

    f.write(" ".join(tmp))


print("------------------------")
with open(tmp_path + "english_leftover_words.dat","w") as f:
    tmp = []
    for i in lo_eng.split():
        print(int(i),e2w[int(i)])
        eng_lo_dict[int(i)]=e2w[int(i)]
        tmp.append(e2w[int(i)])
    f.write(" ".join(tmp))



print("**************************************************")




