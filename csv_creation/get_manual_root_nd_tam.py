#Program to get id info of verb . If a verb is kriya mula then getting kriya mula id or else getting normal verb id
#Written by Roja(01-11-19)
#python3 ~/Alignment1/csv_creation/get_manual_root_nd_tam.py ~/Alignment1/csv_creation/kriyA_mUla_default_dic.txt  ~/Alignment1/csv_creation/kriyA_mUla.txt_wx ~/Alignment1/csv_creation/verb_default_dic.txt > verb_root_tam_info.dat 
################################################################################
import sys
from functions import unique_val
from functions import add_data_in_dic
from functions import return_key

fhw = open('H_wordid-word_mapping.dat', 'r').readlines()
fv = open('verb_root_tam_info', 'r').readlines()

##############################
#Declarations:
h_wrd_dict = {}
v_rt_dic = {}
tam_dic = {}
anu_eng_rt_dic = {}
kriyA_mula_dic = {}
anu_rt_dic = {}
anu_tam_dic = {}
verb_dic = {}

##############################
for line in fhw:
    lst = line[:-2].split('\t')
    add_data_in_dic(h_wrd_dict, lst[2], lst[1])

##############################
#storing single mng verb dic
for line in open(sys.argv[3]):
    lst = line.strip().split('\t')
    add_data_in_dic(verb_dic, lst[0], lst[1])

##############################
def check_wrd(index, length, word, f_wrd):
    lst = []
    lst.append(f_wrd)
    for i in range(1, length):
        k = return_key(str(index+i), h_wrd_dict)
        lst.append(k)
    w = ' '.join(lst)
    if w == word:
        return index
##############################
def return_id(word):
    lst = word.split()
    length = len(lst)
    if lst[0] in h_wrd_dict.keys():
        w = []
        out = h_wrd_dict[lst[0]]
        if '/' not in out:
            ind = check_wrd(int(out), length, word, lst[0]) 
            if ind != None:
                return ind
        else:
            ids = out.split('/')
            for each in ids:
                ind = check_wrd(int(each), length, word, lst[0])
                if ind != None:
                    return ind
##############################
for line in fv:
    if 'root:' not in line.strip() and 'tam:' not in line.strip():
        wrd = line.strip()
#        print(wrd)
        out = return_id(wrd)
    if 'root:' in line.strip():
        rt = line.strip()[5:]
#       print(rt)
        if out != None:
           v_rt_dic[out] = rt
    if 'tam:' in line.strip():
        tam = line.strip()[4:-7]
#       print(tam)
        if out != None:
           tam_dic[out] = tam

##############################
#for key in sorted(v_rt_dic):
#    print(key, v_rt_dic[key])

##############################
#Extracting eng_wrd_rt
with open('revised_root.dat', 'r') as rt:
    for line in rt:
        lst = line.strip().split()
        add_data_in_dic(anu_eng_rt_dic, int(lst[1]), lst[2])

##############################################
#storing kriyA_mUla_default_dic info:
for line in open(sys.argv[1]):
    lst = line.strip().split('\t')
    add_data_in_dic(kriyA_mula_dic, lst[0], lst[1])

##############################################
#storing K layer root info in dic:
with open('anu_root.dat', 'r') as anu_rt:
    for line in anu_rt:
        lst = line.strip().split()
        if 'id-anu_root' in lst[0]:
            anu_rt_dic[int(lst[1])] = lst[2]     
        if 'id-anu_tam' in lst[0]:
            anu_tam_dic[int(lst[1])] = lst[2]    

##############################################
#Check for kriyA mUla word
def check_for_kriyA_mUla(start_id, length, anu_vb_word):
    k_m_wrd = []
    ids = []
    for i in range(length):
        if start_id+i not in v_rt_dic.keys():
            val = return_key(str(start_id+i), h_wrd_dict)
            if val != None:
                k_m_wrd.append(val)   #bAwa
                ids.append(str(start_id+i))
        else:
                k_m_wrd.append(v_rt_dic[start_id+i])  #kara
                ids.append(str(start_id+i))

    if anu_vb_word == '_'.join(k_m_wrd):
        return ' '.join(ids) 
##############################################

#extract kriyA_mUla if present using eng word
for key in sorted(anu_tam_dic):
    if key in anu_eng_rt_dic.keys():
        eng_rt = anu_eng_rt_dic[key]
        #print(eng_rt)
        mngs = kriyA_mula_dic[eng_rt].split('/')
        for each in mngs:
            wrd = each.split('_')
            if wrd[0] in h_wrd_dict.keys():
                out = check_for_kriyA_mUla(int(h_wrd_dict[wrd[0]]), len(wrd), each)
                if out != None:
#                    print(each, h_wrd_dict[wrd[0]])
                    print('(anu_id-manu_verb_root-ids',  key, each , out, ')' )
                else:
                    mngs = verb_dic[eng_rt].split('/') 
                    for each in mngs:
                        v_id = return_key(each, v_rt_dic)
                        if v_id != None:
                            print('(anu_id-manu_verb_root-ids',  key,  each,  v_id, ')' )  #ai1E, 2.50, pA

########################################################
#Get kriyA_mUla info from hindi side:
f3 = open(sys.argv[2], 'r').readlines()
kriyA_mUla_lst = []

for each in f3:
    lst = each.strip().split('\t')
    if lst[0] not in kriyA_mUla_lst: 
        kriyA_mUla_lst.append(lst[0])

#print(kriyA_mUla_lst, len(kriyA_mUla_lst))


for key in sorted(v_rt_dic):
    k = key-1
    wrd = return_key(str(k), h_wrd_dict)
    k_m_w = wrd + '_' + v_rt_dic[key]
#    print(wrd, k_m_w)
    if k_m_w in kriyA_mUla_lst:
#        print('&&', k , k_m_w)
        del v_rt_dic[key]
        if k_m_w not in v_rt_dic:
            v_rt_dic[k_m_w] = str(k) + ' ' + str(key)
        else:
            v_rt_dic[k_m_w] = v_rt_dic[k_m_w] + '/'+ str(k) + ' ' + str(key)
        new_key = str(k) + ' ' + str(key)    
        tam_dic[new_key] = tam_dic[key]
        del tam_dic[key]
    else:
        val = v_rt_dic[key]
        del v_rt_dic[key]
        v_rt_dic[val] = key

for key in sorted(v_rt_dic):
    val = v_rt_dic[key]
    print('(verb_root-id', key, val, ')')
    print('(tam-id', tam_dic[val], val, ')')
        
