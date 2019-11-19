#Programme to get alignment of capital words in a sentence
#using 'original_word.dat' for eng and 'H_wordid-word_mapping.dat' for manual.
#Written by Roja(24-10-19)
#RUN:   python ~/Alignment1/csv_creation/check_proper_noun_mng.py  $HOME_anu_test/Anu_data/canonical_form_dictionary/dictionaries/computer_science_dic_in_canonical_form.txt  $HOME_anu_test/Anu_data/canonical_form_dictionary/dictionaries/default-iit-bombay-shabdanjali-dic_smt.txt
#O/p: K_alignment_for_prop.csv
############################################################
import sys
import csv

from functions import unique_val
from functions import add_data_in_dic
from functions import return_key


fr = open("H_wordid-word_mapping.dat", "r").readlines()
fo = open("original_word.dat", "r").readlines()

weak_choice = ['from','with', 'on', 'to', 'of','in','at', 'through', 'by', 'at', 'into', 'over']
###############################
#Declarations:
cap_dic = {}
domain_dic = {}
default_dic = {}
cap_dom_dic = {}
cap_def_dic = {}
man_mng_dic = {}
k_align_dic = {}

list_K_alignment=['K_1st_letter_capital_word']
#################################
#Collecting first word Capital from original_word.dat
for line in fo:
    lst = line[:-2].split()
    if (lst[2].lower() not in weak_choice):#ai1E/2.67:  Condition added by Kishori 9 nov to remove 1_In = 3_meM/10_meM in K_1st_letter_capital_word
        if(lst[2][0].isupper()): #and lst[1] != '1'):
            #print(lst[2])
            add_data_in_dic(cap_dic, int(lst[1]), lst[2].lower())
    
    
    
    
#for key in sorted(cap_dic):
#    print(str(key) + '\t' + cap_dic[key])

#################################
#Creating domain dic:
for line in open(sys.argv[1]):
    if(line[0]!= '#'):
        lst = line.strip().split('\t')
        wrd = lst[0].split('_')
        add_data_in_dic(domain_dic, wrd[0], lst[1])

#for key in sorted(domain_dic):
#    print(str(key) + '\t' + domain_dic[key])
        
#Checking collected capital words in domain dic:
for key in sorted(domain_dic):
    if(key in cap_dic.values()):
        key_id = return_key(key, cap_dic)
   #    if(key_id not in cap_dom_dic.keys()):  #If neccessary uncomment this loop
        cap_dom_dic[key_id] = domain_dic[key]
   #    print(str(key_id) + '\t' + domain_dic[key])


#################################
#Creating default dic:
for line in open(sys.argv[2]):
    if(line[0]!= '#' and line[0] != '\t'):
        lst = line.strip().split('\t')
        add_data_in_dic(default_dic, lst[0], lst[1])

#Checking collected capital words in domain dic:
for key in sorted(default_dic):
    if(key in cap_dic.values()):
        key_id = return_key(key, cap_dic)
        cap_def_dic[key_id] = default_dic[key]
#        print(str(key_id) + '%%\t' + default_dic[key])

#################################
#Creating manual mng dic (NMT sentence or Manual sentence)
for line in fr:
    lst = line[:-2].split('\t')
    add_data_in_dic(man_mng_dic, lst[2], lst[1])

#for key in sorted(man_mng_dic):
#    print(key + '\t' + man_mng_dic[key])

#################################
#Manual mng first checking in domain dic if not found checking in default dic
for key in sorted(cap_dom_dic):
    if(cap_dom_dic[key] in man_mng_dic.keys()):
        k_align_dic[key] = man_mng_dic[cap_dom_dic[key]]
#        print(str(key)+ '\t' + man_mng_dic[cap_dom_dic[key]])

for key in sorted(cap_def_dic):
    if(key not in k_align_dic.keys()):
      for each in cap_def_dic[key].split('/'):
          if(each in man_mng_dic.keys()):
             k_align_dic[key] = man_mng_dic[each]
#             print(str(key)+ '\t' + man_mng_dic[each])
             break
#################################
#for key in sorted(k_align_dic):
#    print(str(key) + '\t' + k_align_dic[key])

for i in range(len(fo)):
    list_K_alignment.append('-')

#Store data in list_K_alignment
for i in range(1, len(fo)+1):
    if i in k_align_dic.keys():
        list_K_alignment[i] = k_align_dic[i]

#print('K Alignment layer info::\n', list_K_alignment)
#################################
#Writing in csv
with open("K_1st_letter_capital_word.csv", 'w') as csvfile:
   csvwriter = csv.writer(csvfile)
   csvwriter.writerow(list_K_alignment)
#################################
