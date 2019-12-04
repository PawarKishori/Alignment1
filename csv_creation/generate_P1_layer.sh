#To generate P1 layer

#Convert srun_All_Resources.csv to facts
python3 $HOME_alignment/csv_creation/convert_csv_to_facts.py srun_All_Resources.csv > all_layer_facts.dat

#Create Eng and Hindi Soumya grouping facts
python3 $HOME_alignment/csv_creation/create_facts_from_grouping.py E_Word_Group_Sanity.dat Eng > E_grouping.dat
python3 $HOME_alignment/csv_creation/create_facts_from_grouping.py H_Word_Group.dat Hnd > H_grouping.dat

#Reporting warnings where ids are reported, where N2 and P mismatches
python3 $HOME_alignment/csv_creation/report_warnings.py  > wrong_grouping_id.dat 

#Get each word with count of occurences
python3 $HOME_alignment/csv_creation/check_each_word_occurences.py eng_wrd_occurence.dat hnd_wrd_occurence.dat

#Get each row grouping info. For ex: In P col 5 val is 7 8 then we get that info
python3 $HOME_alignment/csv_creation/get_grouping_info.py  > get_all_layer_group_info.dat

#Generating P1 layer
echo "(defglobal ?*path* = $HOME_alignment)" > alignment_path.clp
myclips -f $HOME_alignment/csv_creation/run.bat > new_layer.error

#Converting P1 layer fact to csv 
python3 $HOME_alignment/csv_creation/convert_new_layer_fact_to_csv.py new_p_layer.dat  > p1_layer.csv

#Replacing new layer id with id_wrd format
python3 $HOME_alignment/csv_creation/replace_id_with_wrd.py   H_wordid-word_mapping.dat p1_layer.csv > p1_layer_with_wrd.csv


python3 $HOME_alignment/csv_creation/add_p1_layer.py  srun_All_Resources.csv srun_All_Resources_id_word.csv

cp j srun_All_Resources.csv
cp k srun_All_Resources_id_word.csv

#Appending new layer P1 in new-final.html
cd $HOME_anu_tmp/tmp/$1_tmp
python3 $HOME_alignment/working_debug/CSV_to_HTML.py $1 $2

