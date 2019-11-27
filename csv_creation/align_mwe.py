#Programme to get alignment of mwe words in a sentence
#using 'word.dat' for eng and 'H_wordid-word_mapping.dat' for manual.
#Written by Roja(30-10-19)
#RUN: python ~/Alignment1/csv_creation/align_mwe.py  multi_word_expressions.dat  <technical_mwe_dic>
#Ex:  python ~/Alignment1/csv_creation/align_mwe.py  multi_word_expressions.dat  mwe_tech_dic.txt 
#O/p: K_exact_mwe_word_align.csv
#NOTE: << >> This notation is used for guessing . If any mng or word is guessed then in O/p it is stored in this format
############################################################
import sys
import csv

from functions import unique_val
from functions import add_data_in_dic
from functions import return_key

fw = open("word.dat", "r").readlines()
fr = open("H_wordid-word_mapping.dat", "r").readlines()

############################################################
#Declarations:
wrd_dic = {}
mwe_dic = {}
h_wrd_dic = {}
k_mwe_dic = {}

list_K_exact_word_align=['K_exact_word_align']

############################################################
#Creating wrd_dic, nwe_dic, h_wrd_dic
for line in fw:
    lst = line[:-2].split()
    wrd_dic[lst[1]] = lst[2]

for line in open(sys.argv[2]):
    lst = line.strip().split('\t')
    mwe_dic[lst[0]] = lst[1]

for line in fr:
    lst = line[:-2].split('\t')
    add_data_in_dic(h_wrd_dic, lst[2], lst[1])
############################################################
#Checking multi_word_expressions.dat
mwe_list = []
for line in open(sys.argv[1]):
    mwe_mng = ''
    lst = line[:-2].split()
    if 'compound' in lst[3]:
        mwe_mng = lst[2]
    ids = lst[4:]
    print(ids, mwe_mng)
    mwe_lst = []
    for each in ids:
        mwe_lst.append(wrd_dic[each])
        #print each, wrd_dic[each], h_wrd_dic.keys()
    mwe = '_'.join(mwe_lst) #finite_state_machine
#    print(mwe)#, mwe_dic.keys())
    if mwe in mwe_dic.keys():
            print(mwe), 
            expr = mwe_dic[mwe]
            #print expr
            expr_lst = expr.split()
            h_ids = []
            for i in range(0, len(expr_lst)):
                item = expr_lst[i]
                if item.split(':')[1] in h_wrd_dic.keys():
                    val = item.split(':')[1]
                    h_ids.append(h_wrd_dic[val])       # Ex: item.split(':')[1] = 'parimiwa' , h_wrd_dic['item.split(':')[1]] = 4 (Ex: 2.98, ai2E)
                    k_mwe_dic[ids[i]] = h_wrd_dic[val]
                    #print h_wrd_dic[val]
                else:
                    last_id = h_ids[-1]
                    cur_id = int(last_id)+1
                    o = return_key(str(cur_id), h_wrd_dic)
                    if o != None:
                        #print item.split(':')[1] + '<>' + o
                        k_mwe_dic[ids[i]] = '<< ' + str(cur_id) + ' >>'

#################################
for key in sorted(k_mwe_dic):
    print(str(key) + '\t' + k_mwe_dic[key])


for i in range(len(fw)-1):
    list_K_exact_word_align.append('-')

#Store data in list_K_alignment
for i in range(1, len(fw)):
    if str(i) in k_mwe_dic.keys():
        list_K_exact_word_align[i] = k_mwe_dic[str(i)]

print('K exact word align layer info::\n', list_K_exact_word_align)
#################################
#Writing in csv
with open("K_exact_mwe_word_align.csv", 'w') as csvfile:
   csvwriter = csv.writer(csvfile)
   csvwriter.writerow(list_K_exact_word_align)

