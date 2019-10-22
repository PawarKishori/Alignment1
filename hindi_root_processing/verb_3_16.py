#!/usr/bin/env python
# coding: utf-8

# In[43]:


#!/usr/bin/env python
# coding: utf-8

# In[50]:

#print("abc")
mydict={}
import sys
import os
path=sys.argv[1]
#path ="/home/user/tmp_anu_dir/tmp/ai1E_tmp/2.96"
#f= open("/home/user/tmp_anu_dir/tmp/ai1E_tmp/2.9/H_sentence","r")

f= open(path+"/VP_expr_by_hindi_parser","r")
contents=f.readlines()
def info_required():
    text_file = open("/home/kishori/a/Alignment1/hindi_root_processing/dict_tam_req.txt", "r")
    word=[]
    required=[]
    info=[]
    for i in text_file:
        word.append(i.split("                    "))
    for i in word:
        required.append(i[1])
#print(required)
#print(word)
    
    for i in word:
    #for j in range(len(i)):
        info.append(word[word.index(i)][0][len(i[0])-5:len(i[0])])
    return(word)
required=[]
info=[]
def previous_word(sentence,t):
    p=''
    for i in reversed(range(0,t-1)):
        if sentence[i]==" ":
            break
        else:
            p=sentence[i]+p
    #print(p)
    return(p)
for sentence in contents:
    print(sentence)
    list2=[] 
    word=info_required()
    for i in word:
            required.append(i[1])

    for i in word:

            info.append(word[word.index(i)][0][len(i[0])-5:len(i[0])])
    #text_file = open("/home/user/kishori/tam_dict.txt", "r")
    #text_file = open("/home/user/Desktop/tam_dict.txt", "r")

    #lines = text_file.readlines()

    symbol=['?','.','!',',']
    for i in sentence:
        #if i in symbol:
            sentence=sentence.translate({ord('.'): None})
            sentence=sentence.translate({ord('\n'): None})
            sentence=sentence.translate({ord('?'): None})
    #print(sentence)

    split_sentence=sentence.split()

    finallist=[]
    reversedlist=[]
    remove=('0','nA','wA','yA')
    totallist=[]
    for i in range(len(required)):
        wordlist=[]
        wordlist=[required[i][:-1]]
        totallist.append(wordlist)
    for i in range(len(required)):
        mydict[required[i]]=info[i]
    #print(totallist)
    for i in (totallist):
        for j in range(len(i)):
             z=totallist[totallist.index(i)][j].split('_')


             finallist.append(z)

    finallist.sort(key=len)
    
    reversedlist=finallist[::-1]
    finallist=[]   
    newdict={}
    for k in sorted(mydict,key=lambda k: len(k),reverse=True):
    #print("%s: %s" % (k, mydict[k]))
        newdict[k]=mydict[k]
    for i in reversedlist:
                 t=[" ".join(reversedlist[reversedlist.index(i)])]
                 finallist.append(t)
    #print("abc")
    z=[]
    t=[]
    anu_path=os.getenv('HOME_anu_test')
    morph_command=" | lt-proc "+  anu_path  +"/bin/hi.morf.bin | apertium-retxt"
    for  i in finallist:

          for j in range(len(i)):

                if 'nA' in finallist[finallist.index(i)][j][0:2] or 'wA' in finallist[finallist.index(i)][j][0:2] or 'yA' in finallist[finallist.index(i)][j][0:2]:
                    if " " in finallist[finallist.index(i)][j][3:]:
                        if finallist[finallist.index(i)][j][3:] in sentence:
                             #print(finallist[finallist.index(i)][j])
                             z=previous_word(sentence,sentence.index(finallist[finallist.index(i)][j][3:]))
                             command="echo "+z+ morph_command
                             #command="echo "+z+" | lt-proc /home/user/anusaaraka/apertium/en.morf.bin | apertium-retxt"
                             #str22=os.popen(command).readlines()
                             #print(str22)
                             root="root:"+z
                             tam ="tam:"+finallist[finallist.index(i)][j][3:]
                             t.append(root+" "+tam)
                        



                else:
                    if " " in finallist[finallist.index(i)][j][2:]:
                        if finallist[finallist.index(i)][j][2:] in sentence:
                             #print(finallist[finallist.index(i)][j])
                             z=previous_word(sentence,sentence.index(finallist[finallist.index(i)][j][2:]))
                             command="echo "+z+ morph_command
                             #command="echo "+z+" | lt-proc /home/user/anusaaraka/apertium/en.morf.bin | apertium-retxt"
                             #str22=os.popen(command).readlines()
                             #print(str22)
                             root="root:"+z
                             tam ="tam:"+finallist[finallist.index(i)][j][2:]
                             t.append(root+" "+tam)
                    else:
                            if finallist[finallist.index(i)][j][2:] in split_sentence:
                                #print(finallist[finallist.index(i)][j])
                                z=previous_word(sentence,sentence.index(finallist[finallist.index(i)][j][2:]))
                                #command="echo "+z+" | lt-proc /home/user/anusaaraka/apertium/en.morf.bin | apertium-retxt"
                                command="echo "+z+ morph_command
                                #str22=os.popen(command).readlines()
                                #print(str22)
                                root="root:"+z

                                tam ="tam:"+finallist[finallist.index(i)][j][2:]
                                t.append(root+" "+tam)
                         


    t1=[]
    #print(t)
    for i in range(len(t)):
        #for j in range(len(i)):
            if t[i][5]==" ":
                #print(t[i])
                pass
            else:
                t1.append(t[i])
    #print(t1[0])
                
    if t1==[]:
        print("root:")
        print("tam:")
    else:
        tam=""
        for i in range(t1[0].index("tam")+4,len(t1[0])):
            tam=tam+t1[0][i]
            
        #print(tam)
        string=""               
        for ii in range(5,len(t[0])):
            if t1[0][ii]!=" ":
                string=string+str(t1[0][ii])
            else:
                break
        list1=[]  
        #print(string)
        command="echo "+string+morph_command
        #command="echo "+string+" | lt-proc /home/user/anusaaraka/bin/hi.morf.bin | apertium-retxt"
        str22=os.popen(command).readlines()
        str1=str22[0].split("/")
        #print(str1)

        for i in str1:
             
             if "<cat:v>" in i:
                     list1.append(i)
                    

        #print(list1)
        tam1=""

        try: 
            root=""
            #print(list1)
            #if(list1)
            for i in list1[0]:
                if i=="<":
                    break
                else:
                    root=root+i
            for i in range(list1[0].index("tam")+4,len(list1[0])-1):
                tam1=tam1+list1[0][i]
            zz=tam.replace(" ","_")
            print("root:"+root)
            if len(tam)!=0:
            
                tam=tam1+"_"+zz
                for i in newdict.keys():
                    if zz in i:
                        req=(newdict[i])
                        break
                #print("root:"+root)
                print("tam:"+tam1+"_"+zz+"("+req+")")
            else:
                print("tam:"+tam1)
        except:
            root=tam
            #print(root)
            if " " in root[0]:
                root=root=root[1:]
            finroot=root.split(" ")
            #print("finroot")
            #print(finroot)
            command="echo "+finroot[0]+morph_command
            #command="echo "+finroot[0]+" | lt-proc /home/user/anusaaraka/bin/hi.morf.bin | apertium-retxt"
            finroot.pop(0)
            tam2=" ".join(finroot)
            #print(len(tam2))
            #print("tam2"+tam2)
            
            str22=os.popen(command).readlines()
            #print(str22)
            str1=str22[0].split("/")
            #print("str1:"+str1)
            for i in str1:
                if "<cat:v>" in i:
                     list2.append(i)

            root=""
            
            for z in list2[0]:
                if z=="<":
                    break
                else:
                    root=root+z
            for i in range(list2[0].index("tam")+4,len(list2[0])-1):
                tam1=tam1+list2[0][i] 
            zz=tam2.replace(" ","_")
            print("root:"+root)
            if len(zz)!=0:
                for i in newdict.keys():
                    if zz in i:
                        req=(newdict[i])
                    #print(req)
                        break
            
                #print("root:"+root)
                print("tam: "+tam1+"_"+zz+"("+req+")")
            else:
                print("tam: "+tam1)





