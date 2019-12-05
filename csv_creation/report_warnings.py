#Programme to report warnings like :
#   -> N2 and P layer mismatch
#   -> P layer left over words
#   -> Repeatition english words
#Written by Roja (04-12-19)
#python3 $HOME_alignment/csv_creation/report_warnings.py > wrong_grouping_id.dat
########################################################################################
import sys, csv
from all_indices import return_index

n2_dic = {}
p_dic = {}

#To get N2 and P layer mismatch::
with open('srun_All_Resources.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] == 'N2_layer':
            for i in range(1, len(row)):
                n2_dic[i] = row[i]
        if row[0] == 'P':
            for i in range(1, len(row)):
                p_dic[i] = row[i]


for key in sorted(n2_dic):
    if n2_dic[key] != p_dic[key]:
        print('(N2_P_mismatch ', key, ')')

####################
#To get Repeated english words index
with open('word.dat', 'r') as wd:
    new_lst = []
    w_lst = []
    for line in wd:
        if 'id-word' in line:
            lst = line[:-2].split()
            w_lst.append(lst[2])
    for each in w_lst:
        out = return_index(w_lst, each)
        if len(out) > 1:
            for each in out:
                if each+1 not in new_lst:
                   new_lst.append(each+1)

    for each in new_lst:
        print('(Repeated_id ' , each, ')')
