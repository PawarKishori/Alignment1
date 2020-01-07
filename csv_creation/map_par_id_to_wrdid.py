#Programme to map manual word id with word id 
#As manual_word.dat contains punctuations info..so treating it as parser ids. Hence mapping to word id is required.
#RUN:: python3 $HOME_alignment/csv_creation/map_par_id_to_wrdid.py manual_word.dat  manual_id_mapped.dat manual_id_wrdid.dat
##########################################################
import sys

hin_dic = {}
p_id_w_id_dic = {}
p_count = 0
f = open(sys.argv[2], 'w')
f1 = open(sys.argv[3], 'w')
flog = open("mapping_log_info", 'w')
flag = 0

#To check any difference between mapping files. This is not neccessary
try:
    fw = open('H_wordid-word_mapping.dat', 'r').readlines()
except:
    flog.write('H_wordid-word_mapping.dat is missing')
    flag = 1
    

for line in open(sys.argv[1]):
    lst = line[:-2].split()
    if '@PUNCT' in lst[2]:
        p_count += 1
    elif '.' in lst[2]:
        p_count += 1
    else:
        hin_dic[int(lst[1])-p_count] = lst[2]
        p_id_w_id_dic[int(lst[1])] = int(lst[1])-p_count

#To get mapped id and wrd info:
for key in sorted(hin_dic):
    f.write('(manual_mapped_id-word ' +  str(key) + ' ' + hin_dic[key] + ')\n')

#To get original id and mapped id:
for key in sorted(p_id_w_id_dic):
    f1.write('(manual_parserid-wordid ' +  str(key) + ' ' + str(p_id_w_id_dic[key]) + ')\n')

#To check any difference between mapping files. This is not neccessary
if(flag == 0):
    for line in fw:
        lst = line[:-2].split('\t')
        if lst[2] != hin_dic[int(lst[1])]:
            flog.write('Mismatch in line: ' + line)
