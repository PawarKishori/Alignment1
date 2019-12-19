#Programme to report P and P1 mismatch
#Written by Roja (04-12-19)
#python3 $HOME_alignment/csv_creation/check_P_nd_P1_mismatch.py > P_P1_mismatch.dat
########################################################################################
import sys, csv

n2_dic = {}
p_dic = {}

#To get N2 and P layer mismatch::
with open('srun_All_Resources.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[0] == 'P':
            for i in range(1, len(row)):
                n2_dic[i] = row[i]
        if row[0] == 'P1':
            for i in range(1, len(row)):
                p_dic[i] = row[i]


for key in sorted(n2_dic):
    if n2_dic[key] != p_dic[key]:
        print('(P_P1_mismatch ', key, ')')

