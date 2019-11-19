#Programme to align verb info in K exact and K partial layers
#python3 ~/Alignment1/csv_creation/verb_alignment.py  verb_root_tam_info.dat anu_root.dat 
##########################################################################################
import sys
import csv

from functions import unique_val
from functions import add_data_in_dic
from functions import return_key

############################################
#Declarations:
v_rt_dic = {}
tam_dic = {}
anu_rt_dic = {}
anu_tam_dic = {}
k_v_rt_dic = {}
k_v_rt_par_dic = {}
############################################
#storing verb rt and tam info in dics:
for line in open(sys.argv[1]):
    lst = line.strip().split()
    if 'verb_root-id' in lst[0]:
        add_data_in_dic(v_rt_dic, lst[1], ' '.join(lst[2:-1])) #vApasa_A    8 9
    if 'tam-id' in lst[0]:
        add_data_in_dic(tam_dic, lst[1], ' '.join(lst[2:-1]))


##############################################

#storing K layer root info in dic:
for line in open(sys.argv[2]):
    lst = line.strip().split()
    if 'id-anu_root' in lst[0]:
        anu_rt_dic[int(lst[1])] = lst[2]     

##############################################
#aligning verb root
for key in sorted(anu_rt_dic):
    anu_rt = anu_rt_dic[key]
    print('**',anu_rt)
    if anu_rt in v_rt_dic.keys():
        print(v_rt_dic.values())
        k_v_rt_dic[key] = v_rt_dic[anu_rt]  #Ex:vApasa_A
    else:
        a_rt_lst = anu_rt.split('_')
        for each in a_rt_lst:
            if each in v_rt_dic.keys():
                k_v_rt_par_dic[key] = v_rt_dic[each]

##############################################

for key in sorted(k_v_rt_dic):
    print(key, k_v_rt_dic[key])

#for key in sorted(k_v_rt_par_dic):
#    print(key, k_v_rt_par_dic[key])

##############################################
new_list = []
with open('H_alignment_parserid.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] == 'K_exact_without_vib' or row[0] =='K_Root' or row[0] == 'K_Dic':
            for i in range(len(row)):
                if i in k_v_rt_dic.keys():
                    row[i] = k_v_rt_dic[key]
        elif row[0] == 'K_par':
            for i in range(len(row)):
                if i in k_v_rt_par_dic.keys():
                   row[i] = k_v_rt_par_dic[key]
        new_list.append(row)
#        print(row)

with open('H_alignment_parserid-new.csv','w') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerows(new_list)




