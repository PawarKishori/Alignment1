#Create facst from Soumya grouping
#Written by Roja(02-12-19)
#For Eng:::
#python3 $HOME_Alignment/csv_creation/create_facts_from_grouping.py E_Word_Group_Sanity.dat Eng > E_grouping.dat
#For Hnd:::
#python3 $HOME_Alignment/csv_creation/create_facts_from_grouping.py H_Word_Group.dat Hnd >  H_grouping.dat 
#################################################################
import sys
count = 0
fact_name = str(sys.argv[2])

for line in open(sys.argv[1]):
    lst = line.split('(grp_elements_ids')
    ids = lst[1].split(')')
    count += 1
    print('('+ fact_name + '_label-group_elements', count, ids[0], ')')

