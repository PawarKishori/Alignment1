#Programme to convert newly generated layer(or any layer) to csv 
#Written by Roja(03-12-19)
#python3 $HOME_alignment/csv_creation/convert_new_layer_fact_to_csv.py new_p_layer.dat  > p1_layer.csv
#####################################################################################
import sys, re

label = str(sys.argv[2])

for line in open(sys.argv[1]):
    lst = line[1:-2].split()
    new_lst = []
    if lst[0] != label:
        lst[0] = label
    for each in lst:
        if ',' in each:
            each = re.sub(r',', ' ', each)
            new_lst.append(each)
        else:    
            new_lst.append(each)
    print(','.join(new_lst))       
       

