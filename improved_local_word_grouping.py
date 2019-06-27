from operator import itemgetter
from itertools import groupby
import re 
import string
import sys
path =""

ignore_path = ['/home/akanksha/Alignment/tam_local/cl_english_100_detok_tmp/2.49/','/home/akanksha/Alignment/tam_local/cl_english_100_detok_tmp/2.24/','/home/akanksha/Alignment/tam_local/cl_english_100_detok_tmp/2.64/','/home/akanksha/Alignment/tam_local/cl_english_100_detok_tmp/2.74/','/home/akanksha/Alignment/tam_local/cl_english_100_detok_tmp/2.78/'
,'/home/akanksha/Alignment/tam_local/cl_english_100_detok_tmp/2.83/','/home/akanksha/Alignment/tam_local/cl_english_100_detok_tmp/2.85/']
#if path[-1]!="/":
#    path+="/"
# path_kriya_mul = sys.argv[1]
# path = '/home/akanksha/Alignment/tam_local/ss/home/user/forked/tmp_anu_dir/tmp/eng_cl_random_25_3_detok_tmp/2.2/'
# path="/home/akanksha/Alignment/tam_local/eng_cl_random_25_1_detok_tmp/2.16/"
path_kriya_mul = "/home/kishori/a/Alignment1/"
if path_kriya_mul[-1]!="/":
    path_kriya_mul+="/"
# path_all_tam = sys.argv[2]  
path_all_tam = "/home/kishori/a/anusaaraka/Anu_data/"
if path_all_tam[-1]!="/":
    path_all_tam+="/"


with open(path_kriya_mul+"kriyA_mUla_combined.txt","r") as g:
    kriya_mul = g.read()    
with open(path+"manual_hin.morph.dat","r") as g:
    data = g.read()
with open(path+"H_wid-word.dat","r") as g:
    fact_ = g.read()
with open(path+"H_sentence","r") as g:
    sentence = g.read().strip()
with open(path+"manual_hin.tam.dat","r") as g:
    tam_ = g.read()
with open(path_all_tam+"AllTam.txt","r") as g:
    all_tam_ = g.read()
    
punct = string.punctuation
with open(path+"pos.dat","r") as g:
    pos = g.read().strip()    
pos_ = [each_pos.strip(")").split("\t")[1:] for each_pos in pos.splitlines()]
pos_ = list(filter(lambda x:x[-1]!="SYM",pos_))
pos_grp=[]
for i in range(len(pos_)-1,-1,-1):
    if pos_[i][1] not in punct:
        pos_grp.append((pos_[i][1],pos_[i][2]))


kriya_mul_word = [each_kriya.split("\t")[0] for each_kriya in kriya_mul.splitlines()]
word_list = sentence.split()
sentence_dictionary = [(k,l.strip(string.punctuation)) for k,l in enumerate(word_list)]


new_data = [i.split("\t")[1:] for i in re.sub(' +', '\t', data.strip()).split("\n")]
fact_split = [['(Hid-lwg-lwg_ids']+i.strip(")").split()[1:]+["0)"] for i in fact_.strip().splitlines()]
hyphen = [(i[2], ind) for ind,i in enumerate(fact_split) if "-" in i[2]]
abbrevation = [(i[2], ind) for ind,i in enumerate(fact_split) if "." in i[2]]
morph_ = list(map(itemgetter(0), groupby(new_data)))
c=1
wrd_grps_id = []
lwg = ""
lwg_ = ""
wrd_id = ""
tam_root_grp={}
tam_i=""
tam_root = ""
prev_verb = 0
old_morph_dict = []
fk=0

group=groupby(morph_, key=lambda each: each[0])
for i in group:
    cat = []
    root = []
    for j in i[1]:
        cat.append(j[2].strip(")"))
        root.append(j[1].strip(")"))
    old_morph_dict.append((i[0],list(set(cat)),list(set(root)),str(c)))
    c+=1

from functools import reduce
if hyphen:
    for i in hyphen:
        hyphented = i[0].split("-")
        if len(set(hyphented))==1 or all([True if x.isdigit() else False for x in hyphented]):
            old_morph_dict[i[1]] =  (i[0],list(reduce(lambda x,y: x+y, [old_morph_dict[j][1] for j in range(i[1],i[1]+len(hyphented))])),list(reduce(lambda x,y: x+y, [old_morph_dict[j][2] for j in range(i[1],i[1]+len(hyphented))])),i[1])
            continue
        old_morph_dict[i[1]] =  (i[0],list(reduce(lambda x,y: x+y, [old_morph_dict[j][1] for j in range(i[1],i[1]+len(hyphented))])),list(reduce(lambda x,y: x+y, [old_morph_dict[j][2] for j in range(i[1],i[1]+len(hyphented))])),i[1])
        for j in range(len(hyphented)+i[1]-1,i[1],-1):
            old_morph_dict.pop(j)


if abbrevation:
    for i in abbrevation:
        abbrevationated = i[0].split(".")
        abbr = list(i for i, x in groupby(abbrevationated)) 
        old_morph_dict[i[1]] =  (i[0],list(reduce(lambda x,y: x+y, [old_morph_dict[j][1] for j in range(i[1],i[1]+len(abbrevationated))])),list(reduce(lambda x,y: x+y, [old_morph_dict[j][2] for j in range(i[1],i[1]+len(abbrevationated))])),i[1])
        for j in range(len(abbr)+i[1]-1,i[1],-1):
            old_morph_dict.pop(j)


morph_dict = []
lm=0
for k in sentence_dictionary:
    if k[1].isdigit() and old_morph_dict[lm][0].isdigit():
        l=list(old_morph_dict[lm])
        lm+=1
        l[3] = str(k[0]+1)
    elif k[1].isdigit():
        continue
    else:
        l=list(old_morph_dict[lm])
        lm+=1
        l[3] = str(k[0]+1)
    morph_dict.append(tuple(l))

tam__ = [i.split("\t")[1:] for i in re.sub(' +', '\t', tam_.strip()).split("\n")]
tam_1= list(map(itemgetter(0), groupby(tam__)))
tam_group=groupby(tam_1, key=lambda each: each[0])
tam_final_grp = {}
for i in tam_group:
    cat = []
    root=[]
    for j in i[1]:
        root.append(j[1])
        cat.append(j[2].strip(")"))
    cat=list(set(cat))
    if list(set(root))[0]!="v":
        continue
    if cat==["subj"]:
        tam_final_grp[i[0]]="subj"
        continue
    elif cat==["subj","imper"] or cat==["imper","subj"]:
        print("choosing subj over imper")
        tam_final_grp[i[0]]="subj"
        continue
    tam_entry = [i for i in cat if i != "subj" and i!= "imper"]
    if tam_entry!=[]:
        tam_final_grp[i[0]]=tam_entry[0]

all_tam__ = set(i.split("\t")[-1] for i in re.sub(' +', '\t', all_tam_.strip()).split("\n"))
all_tam__1 = set(i.split(",")[0] for i in re.sub(' +', '\t', all_tam_.strip()).split("\n"))
all_tam__1.remove("")
all_tam__.remove("")
flag_1=0
flag_2=0
for each_ele in range((len(morph_dict)-1),-1,-1):
    if morph_dict[each_ele][0] == "lie" or morph_dict[each_ele][0] == "liye":
        if morph_dict[each_ele-1][0] == "ke":
            continue
    elif morph_dict[each_ele][0] == "se" or  morph_dict[each_ele][0] == "kI":
        continue
    elif len(morph_dict[each_ele][1]) == 1 and pos_[each_ele][2][0].lower()=="v": 
        if morph_dict[each_ele][0] in tam_final_grp:  
            tam_i3 = tam_final_grp[morph_dict[each_ele][0]]+"_"+lwg.strip("_")
            tam_i13 = morph_dict[each_ele][0]+"_"+lwg.strip("_")
            if tam_i3.strip("_") in all_tam__ or tam_i3.strip("_") in all_tam__1:
                tam_i=tam_i3.strip("_")
                tam_root =  morph_dict[each_ele][2][0]
                tam_root=tam_root.strip("_")
        lwg = morph_dict[each_ele][0]+"_"+lwg
        wrd_id  = morph_dict[each_ele][3]+" "+wrd_id
        lwg_= ["_"+k for k in morph_dict[each_ele][2]]
        prev_verb = 1
    elif morph_dict[each_ele][0] in tam_final_grp and pos_[each_ele][2][0].lower()=="v":
        tam_i12 = tam_final_grp[morph_dict[each_ele][0]]+"_"+lwg.strip("_")
        tam_i112 = morph_dict[each_ele][0]+"_"+lwg.strip("_")
        if tam_i12.strip("_") in all_tam__ or tam_i12.strip("_") in all_tam__1:
            tam_i=tam_i12.strip("_")
            lwg = morph_dict[each_ele][0]+"_"+lwg
            if "n" in morph_dict[each_ele][1] or "adj" in morph_dict[each_ele][1]:
                for each_root in morph_dict[each_ele][2]:
                    for k in lwg_:
                        if each_root+k in kriya_mul_word:
                            if tam_i!="":
                                prev_tam_root=morph_dict[each_ele+1][2][0]
                                tam_root = morph_dict[each_ele][0]+"_"+prev_tam_root
                            break
            if tam_root == "":
                tam_root =  morph_dict[each_ele][2][0]
            tam_root=tam_root.strip("_")
            #tam_root =  morph_dict[each_ele][2][0]
            #tam_root=tam_root.strip("_")
            wrd_id  = morph_dict[each_ele][3]+" "+wrd_id
            lwg_= ["_"+k for k in morph_dict[each_ele][2]]
            prev_verb = 1
        else:
            for each_root in morph_dict[each_ele][2]:
                flag=0
                for k in lwg_:
                    if each_root+k in kriya_mul_word:
                        lwg = morph_dict[each_ele][0]+"_"+lwg
                        wrd_id  = morph_dict[each_ele][3]+" "+wrd_id
                        if tam_i!="":
                            prev_tam_root=morph_dict[each_ele+1][2][0]
                            tam_root = morph_dict[each_ele][0]+"_"+prev_tam_root
                        prev_verb = 0
                        flag=1
                        break
                if flag == 1: 
                    print(str(each_root)+str(k)+" not found in tam but found in kriyamul \n")
                if flag==0:
                    print(str(each_root)+str(k)+" not found for "+str(each_root)+" in kriyA_mUla dictionary and tam \n")
                    if lwg!="":
                        wrd_grps_id.append((lwg.strip("_"),wrd_id.strip()))
                        if tam_root == '':
                            tam_root ="0"
                            tam_i = "#"
                        tam_root_grp[wrd_id.strip().split()[0]]=[wrd_id.strip().split()[0],tam_root.strip("_"),tam_i.strip("_"),lwg.strip("_"),  wrd_id.strip()]
                        tam_root=""
                        tam_i=""
                        lwg = ""
                        wrd_id = ""
                        prev_verb = 0
                        fk=1
    elif prev_verb == 1 :
        for each_root in morph_dict[each_ele][2]:
                flag=0
                for k in lwg_:
                    if each_root+k in kriya_mul_word:
                        lwg = morph_dict[each_ele][0]+"_"+lwg
                        wrd_id  = morph_dict[each_ele][3]+" "+wrd_id
                        if tam_i!="":
                            prev_tam_root=morph_dict[each_ele+1][2][0]
                            tam_root = morph_dict[each_ele][0]+"_"+prev_tam_root
                        prev_verb = 0
                        flag=1
                        break
                if flag==0:
                    print(str(each_root)+str(k)+" not found for "+str(each_root)+" in kriyA_mUla dictionary \n")
                    if lwg!="":
                        wrd_grps_id.append((lwg.strip("_"),wrd_id.strip()))
                        if tam_root == '':
                            tam_root ="0"
                            tam_i = "#"
                        tam_root_grp[wrd_id.strip().split()[0]]=[wrd_id.strip().split()[0],tam_root.strip("_"),tam_i.strip("_"),lwg.strip("_"),  wrd_id.strip()]
                        tam_root=""
                        tam_i=""
                        lwg = ""
                        wrd_id = ""
                        prev_verb = 0
                        fk=1
    else:
        if lwg!="":
            wrd_grps_id.append((lwg.strip("_"),wrd_id.strip()))
            if tam_root=="":
                tam_root ="0"
                tam_i = "#"
            tam_root_grp[wrd_id.strip().split()[0]]=[wrd_id.strip().split()[0],tam_root.strip("_"),tam_i.strip("_"),lwg.strip("_"),  wrd_id.strip()]
            tam_root=""
            tam_i=""
            lwg = ""
            wrd_id = ""
            prev_verb = 0
            fk=1

if fk==0:
    print("no single verb found. Category need to be disabmbiguated through future resources like parser")



prev = 1
new_fact = []
final_fact_ = []
for i in wrd_grps_id[::-1]:
    index = i[1].split()[0]
    for j in range(len(fact_split)):
        if index == fact_split[j][1]:
            new_fact += fact_split[prev-1:int(index)-1]
            new_fact.append(['(Hid-lwg-lwg_ids',index,i[0],i[1]+")"])
            final_fact_ += [["(id-root-tam-lwg-lwg_ids", fin[1], "0","#",fin[2],fin[3]] for fin in fact_split[prev-1:int(index)-1]]
            final_fact_.append(["(id-root-tam-lwg-lwg_ids"]+tam_root_grp[index][:-1]+[tam_root_grp[index][-1]+")"])
            prev=int(i[1].split()[-1])+1
            break
new_fact+=fact_split[prev-1:]

with open(path+"manual_local_word_group.dat","w") as g:
    for i in new_fact:
        k="\t".join(i)
        g.write(k)
        g.write("\n")

        
with open(path+"revised_manual_local_word_group.dat","w") as g:
    for i in final_fact_:
        k="\t".join(i)
        g.write(k)
        g.write("\n")
