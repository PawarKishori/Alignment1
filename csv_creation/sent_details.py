import re
log=open('file_missing_log','w')
flagf=0
try:
    f = open("E_conll_parse","r").readlines()
    n=len(f)
except:
    flagf=1
    log.write('E_conll_parse missing xD \n')

f1=open("E_id_word_dictionary.dat",'w')
f2=open("sentence_details.dat",'w')
id_list=[]
word_list=[]
flag3=0
flag5=0
if(flagf==0):
    for i in range(n-1):
        id = re.split(r'\t',f[i])
        id_list.append(id[0])
        try:
            word= id[1]
        except:
            print("MULTIPLE TREES PRESENT \n")
            log.write("MULTIPLE TREES PRESENT\n")
            break
        word_list.append(word)
        f1.write(str(id_list[i])+'\t'+word_list[i]+'\n')
    print(id_list)
    print(word_list)

    parse_id_mapping = dict(zip(id_list,word_list))
    print(parse_id_mapping)


try:
    f3=open("manual_word.dat",'r').readlines()
except:
    log.write('manual_word.dat Not Found\n')
    flag3=1
f4=open("manual_id_word_dictionary.dat",'w')


manual_id=[]
manual_word=[]
if(flag3==0):
    n=len(f3)
    for i in range(n):
        id = re.split(r'\s+',f3[i])
        manual_id.append(id[1])
        word= id[2]
        word=word[:-1]
        manual_word.append(word)
        f4.write(str(manual_id[i])+'\t'+manual_word[i]+'\n')

    print(manual_id)
    print(manual_word)

try:
    f5=open("id_Apertium_output_with_grp.dat",'r').readlines()
except:
    flag5=1
    log.write("id_Apertium_output_with_grp.dat\n")

f6=open("anu_id_word_dictionary.dat",'w')


anu_id=[]
anu_word=[]
if(flag5==0):
    n=len(f5)
    for i in range(n):
        id=re.split('\s+',f5[i].rstrip())
        if len(id)==3:
            id[2]="  "+id[2]
        if len(id)>2:
            for j in range(3,len(id)):
                id[2]=id[2]+' '+id[j]
            anu_word.append(id[2][:-2])
        anu_id.append(id[1])

        f6.write(str(anu_id[i])+'\t'+anu_word[i]+'\n')
    print(anu_id)
    print(anu_word)



f2.write("English sentence: ")
for i in id_list:
    f2.write(i+' ')
f2.write("\nManual sentence: ")
for i in manual_id:
    f2.write(i+' ')
f2.write("\nanusaaraka sentence: ")
for i in anu_id:
    f2.write(i+' ')




f1.close()
f6.close()
f2.close()
f4.close()
log.close()
