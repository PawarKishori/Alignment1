#Programme to check and replace P1 layer. If layer founds it replaces or else it appends.
#Written by Roja(04-12-19)
#python3 $HOME_alignment/csv_creation/add_p1_layer.py  srun_All_Resources.csv srun_All_Resources_id_word.csv
#######################################################################
import sys

f = open('p1_layer.csv', 'r').readlines()
p1_with_id = f[0]
f1 = open('p1_layer_with_wrd.csv', 'r').readlines()
p1_with_wrd = f1[0]

fid = open('j' ,'w')
fid1 = open('k' ,'w')

f2 = open(sys.argv[1], 'r').readlines()
f3 = open(sys.argv[2], 'r').readlines()

for i in range(0, len(f2)):
    lst = f2[i].split(',')
    if lst[0] == 'P1':
        fid.write(p1_with_id)
    elif lst[0] == 'P' and i == len(f2)-1:
        fid.write(f2[i])
        fid.write(p1_with_id)
    else:
        fid.write(f2[i])


for i in range(0, len(f3)):
    lst = f3[i].split(',')
    if lst[0]== 'P1':
        fid1.write(p1_with_wrd)
    elif lst[0] == 'P' and i == len(f3)-1:
        fid1.write(f3[i])
        fid1.write(p1_with_wrd)
    else:    
        fid1.write(f3[i])

