import string,csv,sys
def remove_punct(sentence) :
    sentence=sentence.translate(sentence.maketrans('', '', string.punctuation))
    return sentence
def sentence_to_words(sentence):
    
    sent=remove_punct(sentence)
    #print(sent)
    words=sent.split(" ")
    return words
def WSD_modulo_e_words_h_words():
    try :
        e_words=[]
        h_words=[]
        WSD_dict=open(wsd_exact_match_file).read().split("\n")[:-1]
        for i in WSD_dict :
            e=i.split("\t")[1]
            h=i.rstrip(")").split("\t")[2]
            e_words.append(e)
            h_words.append(h)
        #     print(e_words)
        #     print(h_words)
        return e_words,h_words
    except FileNotFoundError :
        with open(logfile,"a") as log :
            print(logfile)
            log.write("Tranliterated_words_first_run.dat "+sent_no+"doesn't exist "+"\n")
            sys.exit()
def return_eids(e_words) :
    e_total=len(e_words)
    eids=[]
    for i in range(1,e_total+1) :
            eids.append(i)
    return eids
def compare_existence(E_sentence,H_sentence):
    print(E_sentence)
    E_sent=open(E_sentence).read().rstrip("\n")
    H_sent=open(H_sentence).read().rstrip("\n")
    e_wsd_words,h_wsd_words=WSD_modulo_e_words_h_words()
    e_words=sentence_to_words(E_sent)
    h_words=sentence_to_words(H_sent)
    final_list=[0 for x in range(len(e_words))]
#     print(final_list)
    for eid,eword in enumerate(e_words) :
        for ewsd,hwsd in zip(e_wsd_words,h_wsd_words):
            if eword == ewsd :
                if final_list[eid]== 0 :
                    final_list[eid]=hwsd
                elif hwsd not in final_list[eid] :
                    
                    temp=final_list[eid]
                    temp=temp+"#"+hwsd
                    final_list[eid]=temp
                
    print(final_list)
    creation_of_csv(e_words,final_list)
def creation_of_csv(e_words,final_list):
    eids=return_eids(e_words)
    with open(csvfile, 'w') as csvfi: 
    # creating a csv writer object 
        csvwriter = csv.writer(csvfi) 
        csvwriter.writerow(eids) 
        csvwriter.writerow(e_words)
        csvwriter.writerow(final_list)

#Full path
E_sentence=sys.argv[1]


H_sentence=sys.argv[2]


wsd_exact_match_file=sys.argv[3]


temp=E_sentence.split("/")[:-1]
tmp_path="/".join(temp)
sent_no=temp[-1]
logpath="/".join(tmp_path.split("/")[:-1])
logfile=logpath+"/Transliterate_csv_log"
# print(tmp_path)
csvfile=tmp_path+"/Transliterate1.csv"
compare_existence(E_sentence,H_sentence)

