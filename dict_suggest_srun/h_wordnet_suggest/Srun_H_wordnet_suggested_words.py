import re
import os
import sys
import glob

def obtaining_mapped_words(folder):
    try:
        input_file=open(folder+"/anu_root.dat",'r')
        eng_word_mapping=open(folder+'/E_wordid-word_mapping.dat','r')
        per_line_input=input_file.readlines()
        file_list=[]
        file_list_2=[]
        split_list=[]
        element=[]
        element1=[]
        required={}

        for i in per_line_input:
            file_list.append(i.split(" "))

        for i in file_list:
            element1=[]
            element1.append(i[1])
            element1.append(i[2])
            element.append(element1)

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
    except:
        print(folder," missing files")
def process(eng,hin,sentence,folder):
    
    
    hnd_wordnet_adj=open(os.getenv("HOME_anu_test")+"/miscellaneous/SMT/MINION/dictionaries/hnd-wrdnet-adj.txt",'r')
    hnd_wordnet_adv=open(os.getenv("HOME_anu_test")+"/miscellaneous/SMT/MINION/dictionaries/hnd-wrdnet-adv.txt",'r')
    hnd_wordnet_noun=open(os.getenv("HOME_anu_test")+"/miscellaneous/SMT/MINION/dictionaries/hnd-wrdnet-noun.txt",'r')
    hnd_wordnet_verb=open(os.getenv("HOME_anu_test")+"/miscellaneous/SMT/MINION/dictionaries/hnd-wrdnet-verb.txt",'r')
    adj=hnd_wordnet_adj.readlines()
    adv=hnd_wordnet_adv.readlines()
    noun=hnd_wordnet_noun.readlines()
    verb=hnd_wordnet_verb.readlines()
    adj_dict={}
    adv_dict={}
    noun_dict={}
    verb_dict={}
    outcome=[]
    list_split_1=[]
    list_split_2=[]
    list_split_3=[]
    list_split_4=[]
    for i in adj: 
        list_split_1.append(i[:-1].split('\t'))
    for i in list_split_1:
        adj_dict[i[0]]=i[1]
    #print(adj_dict)
    for i in adv: 
        list_split_2.append(i[:-1].split('\t'))
    for i in list_split_2:
        adv_dict[i[0]]=i[1]
    for i in noun: 
        list_split_3.append(i[:-1].split('\t'))
    for i in list_split_3:
        noun_dict[i[0]]=i[1]
    for i in verb: 
        list_split_4.append(i[:-1].split('\t'))
    for i in list_split_4:
        verb_dict[i[0]]=i[1]

    try:
        for key,value in adj_dict.items():
            if hin == key:
                outcome.append(value)

        for key,value in adv_dict.items():
            if hin == key:
                outcome.append(value)

        for key,value in noun_dict.items():
            if hin == key:
                outcome.append(value)

        for key,value in verb_dict.items():
            if hin == key:
                outcome.append(value)

        words=outcome[0].split('/')
        for i in words:
            if i in sentence:
                print(eng +" <> "+i)
                file_write.write(eng +" <> "+i+'\n')
        file_write.close()
    except:
        pass
            
tmp_path = os.getenv('HOME_anu_tmp')+'/tmp/'
path = tmp_path + sys.argv[1]+'_tmp/2.*'
folders = sorted(glob.glob(path))

for folder in folders:
    try:
        print(folder)

        file_write=open(str(folder)+"/srun_H_wordnet.dat",'w')
        file_write.close()
        sentence1=open(str(folder)+"/hindi_leftover_words.dat",'r').readline()
        sentence=sentence1.split(" ")
        element=obtaining_mapped_words(str(folder))
        for i in element:
            hin=i[1]
            eng=i[0]
            process(eng,hin,sentence,str(folder))
    except:
        pass