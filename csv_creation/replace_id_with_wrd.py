#Programme to generate id with word if id is present to display in html
#Written by Roja (04-12-19)
#python3 $HOME_alignment/csv_creation/replace_id_with_wrd.py manual_id_mapped.dat p1_layer.csv > p1_layer_with_wrd.csv
############################################################################################
import sys, re

hwrd_dic = {}

label = str(sys.argv[3])

for line in open(sys.argv[1]):
    lst = line[:-2].split(' ')
    hwrd_dic[lst[1]] = lst[2]


for line in open(sys.argv[2]):
    lst = line.strip().split(',')
    new_lst=[]
    for each in lst:
        if ' ' not in each and each != label and each != '0':
            new_lst.append(each+'_'+hwrd_dic[each])
        elif ' ' in each:
            item = each.split()
            j = []
            for i in item:
                j.append(i+'_'+hwrd_dic[i])
            new_lst.append('+'.join(j))
        else:
            new_lst.append(each)
    p1 = ','.join(new_lst)
    p1 = re.sub(r'\+', ' ', p1)
    print(p1)
    
