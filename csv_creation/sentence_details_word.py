import re
log=open('file_missing_log','w')
flagf1=0
flagf2=0
flagf3=0
try:
    f1=open('E_conll_parse','r').readlines()
    n1=len(f1)-1
except:
    flagf1=1
    log.write("E_conll_parse is missing\n")

try:
    f2=open('hindi_dep_parser_original.dat','r').readlines()
    n2=len(f2)
except:
    flagf2=1
    log.write("hindi_dep_parser_original is missing\n")

try:
    f3=open('anu_id_word_dictionary.dat','r').readlines()
    n3=len(f3)
except:
    flagf3=1
    log.write('anu_id_word_dictionary.dat is missing\n')


s=open("sentence_details_word.dat","w")



list1=[]
#ENGLISH SENTENCE
if(flagf1==0):
    for i in range(n1):
        flaglist=0
        try:
            res=re.split(r'\t',f1[i].rstrip())
            list1.append(res[1])
        except:
            log.write('MULTIPLE TRESS PRESENT\n')
            flaglist=1
            break
    len1=len(list1)
    s.write('English Sentence: ')
    if(flaglist==0):
        for i in range(len1):  #Writing the words
            s.write(list1[i]+' ')

#HINIDI_MANUAL SENTENCE

list2=[]
if(flagf2==0):
    for i in range(n2):
        res=re.split(r'\t',f2[i].rstrip())
        list2.append(res[1])
    len2=len(list2)
    s.write('\nManual Sentence: ')
    for i in range(len2):  #Writing the words
        s.write(list2[i]+' ')

#ANUSAARAKA SENTENCE
list3=[]
if(flagf3==0):
    for i in range(n3):
        f3[i]=f3[i].rstrip("\n")#Removes only the newline characters(Spaces are present in few of the elements that have to be preserved)
        res=re.split(r'\t',f3[i])
        list3.append(res[1])
    len3=len(list3)
    print(len3)
    list4=[]
    for i in range(len3):
        list4.append(" ")
        if('@PUNCT-OpenParen' in list3[i]):
            list4[i]=list3[i].replace("@PUNCT-OpenParen","(")
        elif('@PUNCT-ClosedParen' in list3[i]):
            list4[i]=list3[i].replace("@PUNCT-ClosedParen",")")
        else:
            list4[i]=list3[i]
    print(list4)
    len4=len(list4)
    s.write("\nAnusaaraka Sentence: ")
    for i in range(len4):
        s.write(list4[i]+' ')

s.close()
log.close()
