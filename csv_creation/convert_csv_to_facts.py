#Programme to convert final csv to facts
#Written by Roja(26-11-19)
#python3 $HOME_Alignment/csv_creation/convert_csv_to_facts.py srun_All_Resources.csv > all_layer_facts.dat
##################################################################################
import sys, csv, re

new_list = []

def pre_proccess(value):
    if '/' in value:
        value = re.sub(r'/', '_', value)
    if ' ' in value:
        value = re.sub(r' ', ',', value)

    return(value)    


pick_facts = [  'English_word_ids',
		'K_exact_match',
		'K_exact_word_align',
		'K_exact_without_vib',
		'K_1st_letter_capital_word',
		'K_dict',
		'K_root',
		'N2_layer',
                'P'
             ] 

with open(sys.argv[1], 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        for i in range(len(row)):
            if row[0] in pick_facts:
                out = pre_proccess(row[i])
                new_list.append(out)
        if new_list != []:
            print('(' + ' '.join(new_list) + ')')
            new_list = []
