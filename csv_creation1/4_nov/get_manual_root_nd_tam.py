#Program to get id info of verb . If a verb is kriya mula then getting kriya mula id or else getting normal verb id
#Written by Roja(01-11-19)
#python3 ~/Alignment1/csv_creation/get_manual_root_nd_tam.py H_wordid-word_mapping.dat verb_root_tam_info kriyA_mUla.txt_wx > verb_root_tam_info.dat 
#python3 ~/Alignment1/csv_creation/get_manual_root_nd_tam.py H_wordid-word_mapping.dat verb_root_tam_info ~/create-hindi-parser/dics/kriyA_mUla.txt_wx > verb_root_tam_info.dat 
################################################################################
import sys
from functions import return_key

f= open(sys.argv[1], 'r').readlines()

h_wrd_dict = {}
v_rt_dic = {}
tam_dic = {}

for line in open(sys.argv[1]):
    lst = line[:-2].split('\t')
    h_wrd_dict[int(lst[1])] = lst[2]


def return_id(word):
    lst = word.split()
    length = len(lst)
    if lst[0] in h_wrd_dict.values():
        w = []
        out = return_key(lst[0], h_wrd_dict)
        if out != None:
            w.append(lst[0])
            for i in range(1,length):
                w.append(h_wrd_dict[out+i])
        wrd = ' '.join(w)
        if wrd == word:
            return(out)

for line in open(sys.argv[2]):
    if 'root:' not in line.strip() and 'tam:' not in line.strip():
        wrd = line.strip()
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
    wrd = h_wrd_dict[k]
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

for key in sorted(v_rt_dic):
    val = v_rt_dic[key]
    print('(verb_root-id', key, val, ')')
    print('(tam-id', tam_dic[val], val, ')')
        

