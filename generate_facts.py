# -*- coding: utf-8 -*-
#remove above line when u switch to python3. It is added to avoid an error: SyntaxError: Non-ASCII character '\xe2' in file lwg_knowdge_base.py in hindi_punct

# RUN COMMAND:
# python generate_H_facts.py H_sentence /home/kishori/forked/tmp_anu_dir/tmp/cl_english_100_detok_tmp/2.1

'''This python script is used to do lwg using knowledge base.
Inputs: 
1. H_sentence (hindi wx sentence)  
2. sent_dir path i.e. path of dir where out files to be created.

Outputs:
1. H_punct-position-wid.dat
2. H_wid-word.dat

Pending:
1. Add 2nd argument dynamically

'''

import writeFact
import sys
#$HOME_anu_tmp/tmp/$file_dir/$sentence_dir
tmpSentPath=sys.argv[2]
#tmpSentPath="/home/kishori/forked/tmp_anu_dir/tmp/rGitaE_Up_011_tmp/2.3"
def main():
    rawFile=sys.argv[1]
    [wid_word_list,punctlist,wid_word_dict]=writeFact.createH_wid_word_and_PunctFact(rawFile)
    filename=rawFile.split("/")[-1]
    #print(filename[0])
    if(filename[0]=='H'):
        #print("inside 1st if")
        writeFact.add(punctlist,"H_punct-position-wid",tmpSentPath+"/H_punct-position-wid.dat")
        writeFact.add(wid_word_list,"H_wid-word",tmpSentPath+"/H_wid-word.dat")
    
    if(filename[0]=='E'):
        #print("inside 2nd if")
        writeFact.add(punctlist,"E_punct-position-wid",tmpSentPath+"/E_punct-position-wid.dat")
        writeFact.add(wid_word_list,"E_wid-word",tmpSentPath+"/E_wid-word.dat")

if __name__=='__main__':
    main()
