#Programme to get Hindi sentence with ids
#Written by Roja(05-12-19)
#python3 $HOME_alignment/csv_creation/get_hindi_sentence_with_id_wrd.py  manual_id_mapped.dat > H_sentence_with_ids.dat
#####################################################
import sys

hin_lst = []

for line in open(sys.argv[1]):
    lst = line[:-2].split(' ')
    hin_lst.append(lst[1] + '_' + lst[2])

print('@Hindi_@sentence'+ '\t'+'\t'.join(hin_lst))

