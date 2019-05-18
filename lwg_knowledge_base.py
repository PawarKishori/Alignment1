#AUTHOR: Kishori
#DATE: 25/03/2019
#Code to do lwg of hindi postpositions using vibhakti list

import writeFact
import sys
import re
#python lwg_knowledge_base.py /home/kishori/forked/tmp_anu_dir/tmp/cl_english_100_detok_new_tmp/2.17/H_sentence_bkup /home/kishori/forked/tmp_anu_dir/tmp/cl_english_100_detok_new_tmp/2.17 vibhakti
tmpSentPath=sys.argv[2]

def main():
    hindiRaw=sys.argv[1]
    out=writeFact.createH_wid_word_and_PunctFact(hindiRaw)
    wid_word=out[0]
    
    with open(sys.argv[3],"r") as f:
        vibhaktis = f.read().splitlines() 
    item2WriteInFacts,item, all_vib_ids = writeFact.lwg_of_postprocessors(wid_word,vibhaktis)
    print(item2WriteInFacts)
    print(item)
    #print("Short:",item)
    writeFact.add(item2WriteInFacts,"H_def_lwg-wid-word-postpositions" ,tmpSentPath+"/H_def_lwg-wid-word-postpositions")

if __name__=='__main__':
    main()
