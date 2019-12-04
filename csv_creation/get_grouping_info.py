#Programme to get each layer info with head id and group id format
#Ex: If suppose Col6 has values 7 8 then O/p will be 7 as head id and group ids as 7 8 
#Written by Roja (04-12-19)
#python3 $HOME_alignment/csv_creation/get_grouping_info.py  > get_all_layer_group_info.dat
#O/p: get_all_layer_group_info.dat
#########################################################################################
import sys, csv


def create_grouping_info(layer):
    for i in range(1, len(layer)):
        print(('(' + layer[0] + '-head_id-grp_ids ' + layer[i].split()[0] + ' ' + layer[i] + ')'))


with open('srun_All_Resources.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        create_grouping_info(row)

