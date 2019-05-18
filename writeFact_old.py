# -*- coding: utf-8 -*-
import os
import writeFact
import sys
import re
import operator
hindi_punct=['_','_',"'","!",'"',"#","$","%","&","'","(",")",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","|","}","~","'"]

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

def addLists(factlist,factname,filename):
    #print("Inside writeFactLists Function")
    if os.path.isfile(filename):
        os.remove(filename)
    with open(filename,"a") as f:
        for i in range(0,len(factlist[0])):  #i= number of rows
            fact="("+factname
            for j in range(0,len(factlist)): #j=number of column
                fact=fact+"\t"+str(factlist[j][i])
            fact=fact+")\n"
            #print(fact)
            f.write(fact)
    #print("END: Inside writeFactLists Function")

def createH_wid_word_and_PunctFact(sent):
    with open(sent,"r") as f:
        i=1;wid_word_list=[];punctlist=[]; pattern=re.compile("\w+")
        x=f.read()
        #print(x) #original sentence
        x=" ".join(x.split()) #removing more than one white spaces in line
        for word in x.strip().split(" "):
            #print(i,word)
            #if pattern.match(word):   # if word contains only punctuation eg.'=' exclude it
            #print(word[0],word)
            #print('('in string.punctuation)
            #print(word)
            #if (word[0] in string.punctuation or word[0] in hindi_punct) and len(word)>1: #left punct  
            if word[0] in hindi_punct and len(word)>1: #left punct  
                #print("left punct")
                punct=word[0]
                punctlist.append((punct,"L",i))
                word=word.lstrip(punct)
            #if word[-1] in string.punctuation and len(word)>1:
            if word[-1] in hindi_punct and len(word)>1:
                punct=word[-1]
                punctlist.append((punct,"R",i))
                if len(word)>=2:
                    #if word[-2] in string.punctuation:
                    if word[-2] in hindi_punct:
                        punct1=word[-2]
                        punctlist.append((punct1,"R",i))
                        word=word.rstrip(word[-1])
                word=word.rstrip(word[-1])
                #print(word) 
            wid_word_list.append((i,word))
            i+=1
        wid_word_dict={}
        for pair  in wid_word_list:
            #print(pair[0], pair[1])
            wid_word_dict[0]='root'
            wid_word_dict[pair[0]]=pair[1]
        
        return([wid_word_list,punctlist, wid_word_dict])

p_w={}
def createWID_PID(wid_word, PID, PWORD, POS):
    #print("wid-word******************",wid_word)       
    #print("))))))))))))))))))))")      
    #print((i,j) for i,j in zip(PID,PWORD))
    #for i in range(0, len(PID)):
    #    print(PID[i],PWORD[i])
    print("******************** START createWID_PID ******************")
    print(PID)
    print(PWORD)
    print(POS)
    wid_pid=[];pid_wid=[];wid_pos_list=[]
    index=0
    p_w['P0']=0;new_punct_check=[]
    
    #print(PWORD)
    for item in wid_word:
        #print(item)
        for i in range(index,len(PWORD)):
            if item[1]==PWORD[i]:
                p_w[PID[i]]=item[0]
                wid_pid.append((item[0],PID[i]))
                pid_wid.append((PID[i],item[0]))
                wid_pos_list.append((item[0],POS[i]))
                index=i
                new_punct_check.append(item[0])
                break
    print(type(wid_pos_list))
    print(wid_pos_list)
    print( len(wid_word),len(new_punct_check))
    if len(wid_word)!=len(new_punct_check):
        print("WARNING: NEW PUNCTUATION OCCURED IN SENTENCE: CHECK H_wid-word.dat AND ADD THE NEW PUNCTUATION FROM WORD TO hindi_punct list(line 5) ")
    #writeFact.add(wid_pid,"H_wid-pid",tmpSentPath+"/H_wid-pid.dat")
    #writeFact.add(pid_wid,"H_pid-wid",tmpSentPath+"/H_pid-wid.dat")
    #for itrm in (pid_wid):
        #print("*")
        #print(itrm)
    print(p_w)
    print(wid_pid)
    print("******************** END createWID_PID ******************")
    return([wid_pid, p_w, wid_pos_list])



#===================================
def sortTuple(vib_list,order):
    if (order== 'D'):
        vib_list.sort(key = operator.itemgetter(1), reverse = True)
    if (order == 'A'):
        vib_list.sort(key = operator.itemgetter(1), reverse = False)
    return(vib_list)

def reFunction(vibPattern,sent):
    matches=len(re.findall(vibPattern,sent))
    indices=[(m.start(0), m.end(0)) for m in re.finditer(vibPattern, sent)]
    return([matches,indices])

def findWordPositionInSentence(tmpString, vibPattern):
    vibIds=[]
    vibStartId=len(re.findall(" ",tmpString))+1
    numOfWordsInVibhakti=len(re.findall(" ",vibPattern)) +1
    if numOfWordsInVibhakti == 1:
        vibIds.append(vibStartId)

    if numOfWordsInVibhakti >1 :
        #print("true")
        x=vibStartId
        for i in range(0,numOfWordsInVibhakti):
            x=x+i
            vibIds.append(x)
    return([vibStartId,numOfWordsInVibhakti,vibIds])

def lwg_of_postprocessors(wid_word,vibhaktis):
    words=[];wid=[]; sent_list=[]
    for i in wid_word:
        words.append(i[1])
        wid.append(i[0])
        #Creation of sentence without punctuation
        sent=" ".join(words)
        sent_list.append((i[1],i[0]))
    #print(sent)
    #print(sent_list)
    vib_list=[]

    for v in vibhaktis:
        n=len(v.split(" "))
        vib_list.append((v,n))
        #Sorting of vibh_list in descending order of word length
        vib_list=sortTuple(vib_list,'D')
    
    visited=[];item2WriteInFacts=[];item=[]
    all_vib_ids=[]
    
    for vib in vib_list:
        #print("======================================================================================================")
        vibPattern=vib[0]
        vibStartId=0;
        matches,indices=reFunction(vibPattern,sent)
        if (len(indices)!=0 ): #if the vib is not in sentence  but it is in vib list
            for IND in indices:                #if the same vibhakti is twice in sentence, for loop will be iterated twice
                new_vib_word=sent[IND[0]-1:IND[1]+1]
                if (" "+vibPattern+" " == new_vib_word):
                    tmpString=sent[:IND[0]]        # The whole sentence from start to vibhakti occurance starting index.
                    vibStartId, numOfWordsInVibhakti,vibIds = findWordPositionInSentence(tmpString,vibPattern)
                    #print("+++++++++++",tmpString,IND[0],vibStartId,vibIds)
                    new_vib_word_join="_".join(new_vib_word.strip(" ").split(" "))
                    vibStartId_str=str(vibStartId)
                    #print("B4 IF: ", vibStartId_str,visited)
                    if (vibStartId_str not in visited):
                        visited.append(vibStartId_str)
                        all_vib_ids.append(vibIds)
                        #print("After appending (vibStart, visited): ",vibStartId_str,visited)
                        noun_id=vibStartId-1  #8
                        noun=words[noun_id-1]   #words[8-1] = karane (since word_id = array indix +1)
                        lwg_ids=(noun_id,vibIds)
                        item.append(lwg_ids)
                        #print("noun_id, noun: ",noun_id,noun)
                        #print("item: ",item)
                        new_vib_word_strip="_".join(new_vib_word.strip(" ").split(" "))
                        #print("new_vib_word: ", new_vib_word_strip)
                        lwg="_".join([noun,new_vib_word_strip])
                        #print("lwg: ",lwg)
                        vibIds_str = [str(i) for i in vibIds] 
                        item2WriteInFacts.append((lwg,noun_id,noun," ".join(vibIds_str)))

    print("All_vibhakti_IDs====")
    print(all_vib_ids)
    print(item2WriteInFacts)
    return([item2WriteInFacts,item , all_vib_ids])


#==================================================================================================

def flatten_list(list_of_list):
    final_list = [item for sublist in list_of_list for item in sublist]
    return final_list

