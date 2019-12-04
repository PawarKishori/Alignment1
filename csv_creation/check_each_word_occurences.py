#Programme to get english words and hindi words occurences(count) in a sentence.
#Written By Roja(03-12-19)
#python3 $HOME_alignment/csv_creation/check_each_word_occurences.py eng_wrd_occurence.dat hnd_wrd_occurence.dat 
################################################################################################################
import sys

fw = open("word.dat", "r").readlines()
fh = open("H_wordid-word_mapping.dat", "r").readlines()

fe = open(sys.argv[1], 'w')
fhin =  open(sys.argv[2], 'w')

wrd_dic = {}
hwrd_dic = {}

for line in fw:
    lst = line[:-2].split()
    if 'id-word' in lst[0]:
        if lst[2] not in wrd_dic.keys():
            wrd_dic[lst[2]] = 1
        else:
            wrd_dic[lst[2]] = wrd_dic[lst[2]] + 1

for line in fh:
    lst = line[:-2].split('\t')
    if lst[2] not in hwrd_dic.keys():
        hwrd_dic[lst[2]] = 1
    else:
        hwrd_dic[lst[2]] = hwrd_dic[lst[2]] + 1


for key in sorted(wrd_dic):
    fe.write('(eng_wrd-occurrences ' + key + ' ' + str(wrd_dic[key]) + ')\n')
    

for key in sorted(hwrd_dic):
    fhin.write('(hin_wrd-occurrences ' + key + ' ' + str(hwrd_dic[key]) +  ')\n')
