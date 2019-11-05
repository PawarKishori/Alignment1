#Program to get id info of verb . If a verb is kriya mula then getting kriya mula id or else getting normal verb id
#Written by Roja(01-11-19)
#python3 ~/Alignment1/csv_creation/get_manual_root_nd_tam.py H_wordid-word_mapping.dat verb_root_tam_info kriyA_mUla.txt_wx > verb_root_tam_info.dat 
#python3 ~/Alignment1/csv_creation/get_manual_root_nd_tam.py H_wordid-word_mapping.dat verb_root_tam_info ~/create-hindi-parser/dics/kriyA_mUla.txt_wx > verb_root_tam_info.dat 
################################################################################
import sys
from functions import unique_val
from functions import add_data_in_dic
from functions import return_key

f= open(sys.argv[1], 'r').readlines()

h_wrd_dict = {}
v_rt_dic = {}
tam_dic = {}

for line in open(sys.argv[1]):
    lst = line[:-2].split('\t')
    add_data_in_dic(h_wrd_dict, lst[2], lst[1])

def check_wrd(index, length, word, f_wrd):
    lst = []
    lst.append(f_wrd)
    for i in range(1, length):
        k = return_key(str(index+i), h_wrd_dict)
        lst.append(k)
    w = ' '.join(lst)
    if w == word:
        return index

        

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
    #    print('&&', ind)

for line in open(sys.argv[2]):
    if 'root:' not in line.strip() and 'tam:' not in line.strip():
        wrd = line.strip()
#        print(wrd)
        out = return_id(wrd)
#       if out != None:
#            print(out, wrd)
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
#Get kriyA_mUla info:

f3 = open(sys.argv[3], 'r').readlines()
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
        

