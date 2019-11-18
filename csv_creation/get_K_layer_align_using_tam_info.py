#Written by Roja(15-11-19)
#Programme to get alignment through tam match
#If K layer tam and Manual tam are same even if root is different then aligning the same
#RUN: python3 $HOME_alignment/csv_creation/get_K_layer_align_using_tam_info.py
#O/p: K_tam_layer.csv 
##########################################################################################
import sys
import csv
from functions import return_key

###########################################
#Declarations:
anu_rt_dic = {}
anu_tam_dic = {}
man_rt_dic = {}
man_tam_dic = {}
k_tam_dic = {}
gnp_dic = {}
k_v_t_gnp_dic = {}

list_K_tam  = ['K_exact_with_tam_analysis']
list_K_tam_v = ['K_exact_with_tam_analysis']

###########################################
#Extarct anu root info
with open("anu_root.dat", 'r') as f:
    for line in f:
        if 'id-anu_root' in line:
            lst = line.strip().split()
            anu_rt_dic[int(lst[1])] = lst[2]
        if 'id-anu_tam' in line:
            lst = line.strip().split()
            anu_tam_dic[int(lst[1])] = lst[2]
###########################################
#Extarct manual root info
with open("verb_root_tam_info.dat", 'r') as f1:
    for line in f1:
        if 'tam-id' in line:
            lst = line[:-2].split()
            man_tam_dic[lst[1]] = lst[2:]
        if 'verb_root-id' in line:
            lst = line[:-2].split()
            man_rt_dic[lst[1]] = '+'.join(lst[2:])
        if 'verb_root-tam-gnp-v_id' in line:
            lst = line[:-2].split()
            key = '+'.join(lst[4:])
            gnp_dic[key] = lst[3]

#############################################            
#Aligning with tam if anu root and manual root are different: 
for key in sorted(anu_tam_dic):
#    print(anu_tam_dic[key], man_tam_dic.values())
    if anu_tam_dic[key] in man_tam_dic.keys():
        k = anu_tam_dic[key]
        val = man_tam_dic[k]
        print(val, man_rt_dic)
        man_rt = return_key('+'.join(val), man_rt_dic)
        if man_rt == None:
            man_rt =  return_key(val[0], man_rt_dic)
        if anu_rt_dic[key] != man_rt:
            k_tam_dic[key] = ' '.join(val)
            k_v_t_gnp_dic[key] = man_rt + '+' + k + gnp_dic[val[0]] 
#            print(key, man_rt, man_rt_dic, k)

#############################################            
fw = open("word.dat", "r").readlines()
word_len = len(fw)-1

for i in range(len(fw)):
   list_K_tam.append('-')
   list_K_tam_v.append('-')

for i in range(1, word_len+1):
    if i in k_tam_dic.keys():
        list_K_tam[i] = k_tam_dic[i]
        list_K_tam_v[i] = k_v_t_gnp_dic[i]

print('K tam layer' , list_K_tam)        
#################################
#Writing in csv
with open("K_tam_layer.csv", 'w') as csvfile:
   csvwriter = csv.writer(csvfile)
   csvwriter.writerow(list_K_tam)
#################################
#Writing in csv for visualisation:
with open("K_tam_layer_v.csv", 'w') as csvfile:
   csvwriter = csv.writer(csvfile)
   csvwriter.writerow(list_K_tam_v)

#################################



