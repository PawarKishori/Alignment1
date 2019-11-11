import re
import os
import sys
import glob

def obtaining_mapped_words(folder):
    input_file=open(folder+"/anu_root.dat",'r')
    eng_word_mapping=open(folder+'/E_wordid-word_mapping.dat','r')
    per_line_input=input_file.readlines()
    file_list=[]
    file_list_2=[]
    split_list=[]
    element=[]
    required={}
    for i in per_line_input:
        file_list.append(i.split("  "))
    for i in file_list:
        element.append(i[1][:-3].split(" "))


    per_line_mapping=eng_word_mapping.readlines()
    
    for i in per_line_mapping:
        split_list.append(i.split("\t"))
    
    for i in split_list:
        required[i[1]]=i[2][:-2]
    final_list=[]
    for i in element:
        
        for key in required:
            list_list=[]
            if key == i[0]:
                
                i[0]=required[key]
                list_list.append(i[0])
                list_list.append(i[1])
            if len(list_list)!=0:
            	final_list.append(list_list)
      
    return(final_list)
def process(eng,hin,sentence,folder):
    
    
    hnd_wordnet_adj=open(os.getenv("HOME_anu_test")+"/miscellaneous/SMT/MINION/dictionaries/hnd-wrdnet-adj.txt",'r')
    hnd_wordnet_adv=open(os.getenv("HOME_anu_test")+"/miscellaneous/SMT/MINION/dictionaries/hnd-wrdnet-adv.txt",'r')
    hnd_wordnet_noun=open(os.getenv("HOME_anu_test")+"/miscellaneous/SMT/MINION/dictionaries/hnd-wrdnet-noun.txt",'r')
    hnd_wordnet_verb=open(os.getenv("HOME_anu_test")+"/miscellaneous/SMT/MINION/dictionaries/hnd-wrdnet-verb.txt",'r')
    adj=hnd_wordnet_adj.readlines()
    adv=hnd_wordnet_adv.readlines()
    noun=hnd_wordnet_noun.readlines()
    verb=hnd_wordnet_verb.readlines()
    adj_list=[]
    adv_list=[]
    noun_list=[]
    verb_list=[]
    outcome=[]
    for i in adj: 
        adj_sublist=re.split(r'\t+', i)
        adj_list.append(adj_sublist)
    for i in adv:
        adv_sublist=re.split(r'\t+', i)
        adv_list.append(adv_sublist)
    for i in noun:
        noun_sublist=re.split(r'\t+', i)
        noun_list.append(noun_sublist)
    for i in verb:
        verb_sublist=re.split(r'\t+', i)
        verb_list.append(verb_sublist)
    try:
        for i in adj_list:
            if hin == i[0]:
                outcome.append(i[1])
        for j in adv_list:
            if hin == j[0]:
                if len(outcome)!=0: 
                    outcome.append('/'+j[1])
                else:
                    outcome.append(j[1])

        for k in noun_list:
            if hin == k[0]:
                if len(outcome)!=0: 
                    outcome.append('/'+k[1])
                else:
                    outcome.append(k[1])
        for w in verb_list:
            if hin == w[0]:
                if len(outcome)!=0: 
                    outcome.append('/'+w[1])
                else:
                    outcome.append(w[1])
        #print("outcome",outcome)
        words=outcome[0].split('/')
        for i in words:
            file_write=open(folder+"/srun_H_wordnet.dat",'a')
            if i in sentence:
                print(eng +" <> "+i+'\n')
                file_write.write(eng +" <> "+i+'\n')
        file_write.close()
    except:
        #print("no corresponding word")
        pass
            
            
# sentence1=open("/home/user/tmp_anu_dir/tmp/ai1E_tmp/2.68/hindi_leftover_words.dat",'r').readline()
tmp_path = os.getenv('HOME_anu_tmp')+'/tmp/'
path = tmp_path + sys.argv[1]+'_tmp/2.*'
folders = sorted(glob.glob(path))

# for files in each folder
for folder in folders:
    try:
        file_write=open(str(folder)+"/srun_H_wordnet.dat",'w')
        file_write.close()
        sentence1=open(str(folder)+"/hindi_leftover_words.dat",'r').readline()
        sentence=sentence1.split(" ")
        #print(sentence)
        element=obtaining_mapped_words(str(folder))
        #print(str(folder))
        #print(sentence)
        for i in element:
            hin=i[1]
            eng=i[0]
            process(eng,hin,sentence,str(folder))
    except:
        pass
