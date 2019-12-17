import sys
from functions import unique_val
from functions import add_data_in_dic
from functions import return_key


hrt_dic = {}
hid_dic = {}
kriyA_mUla = []
for line in open(sys.argv[1]):
    lst = line[:-2].split('\t')
    add_data_in_dic(hrt_dic, lst[2], lst[1])
    add_data_in_dic(hid_dic, int(lst[1]), lst[2])


for line in open(sys.argv[2]):
    lst = line.strip().split('\t')
    mngs = lst[1].split('/')
    for each in mngs:
        if each not in kriyA_mUla:
            kriyA_mUla.append(each)
            

#print(kriyA_mUla)

def check_substring(lst, sub):
  sub_lst = []  
  for each in lst:
    if sub in each:
       sub_lst.append(each)
  return sub_lst     


def check_for_kriyA_mUla(lst, dic, v):
    new_wrd = lst[0]
    for i in range(1, len(lst)):
        key = int(v)+i
        if key in hid_dic.keys():
            val = hid_dic[key]
            if val in dic.keys():
                new_wrd = new_wrd + '_' + hid_dic[int(v)+i]
            else:
                return None
        else:
            return None
    return new_wrd   


def check_for_consecutive(wrd, dic): 
#    print(wrd)
    new_lst = []
    lst = each.split('_')
    v = dic[lst[0]]
    new_wrd = lst[0]
    if '/' not in v:
        o = check_for_kriyA_mUla(lst, dic, v)
        if o in kriyA_mUla:
            new_lst.append(o+':'+v)
    else:
        val = v.split('/')
        for j in val: 
            o = check_for_kriyA_mUla(lst, dic, j)
            if o in kriyA_mUla:
                new_lst.append(o+':'+j)
    return new_lst            

def return_ids(wrd, start_id):
    lst = wrd.split('_')
    ids = []
    ids.append(str(start_id))
    for i in range(1, len(lst)):
        ids.append(str(start_id+i))
    return ids    


for key in sorted(hrt_dic):
    new_k_m_l= []
    if key in kriyA_mUla:
        ids = return_ids(key, int(hrt_dic[key]))
        val = key + ' ' + ' '.join(ids)
        if val not in new_k_m_l:
           new_k_m_l.append(val)
    else:
        out = check_substring(kriyA_mUla, key)
        if out != None:
            for each in out:
                lst = each.split('_')
                if lst[0] == key: #Assuming first wrd as key wrd ex: pawA_lagA , key = pawA
                    o1 = check_for_consecutive(each, hrt_dic)
                    if o1 != []:
                        for item in o1:
                            kri_m_lst = item.split(':')
                            ids = return_ids(kri_m_lst[0], int(kri_m_lst[1]))
                            val = kri_m_lst[0] + ' ' + ' '.join(ids) 
                            if val not in new_k_m_l:
                                new_k_m_l.append(val)
    if new_k_m_l != []:
        print('(kriyA_mUla_wrd-ids ', ' '.join(new_k_m_l), ')')
