#Progarmme to get left over words in the required label
#RUN: python3 $HOME_alignment/csv_creation/get_left_over_wrds.py srun_All_Resources.csv  P1 > p1_left_over_wrds.dat
#Where P1 is the label. P1 left over words are stored in p1_left_over_wrds.dat
#O/p: p1_left_over_wrds.dat
#Written by Roja(18-12-19)
#####################################################################################
import sys

lab = str(sys.argv[2])

f = open("H_wordid-word_mapping.dat", 'r').readlines()
count = len(f) #To get file count (no: of words in a sentence)

lab_lst = ''

for line in open(sys.argv[1]):
    lst = line.strip().split(',')
    if lst[0] == lab:
        lab_lst = lst 

#print(lab_lst)
left_over_lst = []
new_lst = []

for each in lab_lst:
    lst = each.split()
    for each in lst:
        new_lst.append(each)

for i in range(1, count+1):
    if str(i) not in new_lst:
        left_over_lst.append(str(i))


print('(' + lab + '_left_over_ids'+ '\t' + ' '.join(left_over_lst) + ')')
