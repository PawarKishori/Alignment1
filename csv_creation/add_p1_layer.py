#Programme to check and replace P1 layer. If layer founds it replaces or else it appends.
#Written by Roja(04-12-19)
#python3 $HOME_alignment/csv_creation/add_p1_layer.py  srun_All_Resources.csv srun_All_Resources_id_word.csv
#######################################################################
import sys

f = open('p1_layer.csv', 'r').readlines()
p1_with_id = f[0]
f1 = open('p1_layer_with_wrd.csv', 'r').readlines()
p1_with_wrd = f[0]

fid = open('j' ,'w')
fid1 = open('k' ,'w')

for line in open(sys.argv[1]):
    if line[0] == 'P1':
        fid.write(p1_with_id+'\n')
    else:
        fid.write(line)


for line in open(sys.argv[2]):
    if line[0] == 'P1':
        fid1.write(p1_with_wrd+'\n')
    else:    
        fid1.write(line)

