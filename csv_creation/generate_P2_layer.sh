#To generate P1 layer

#map manual_word.dat
python3 $HOME_alignment/csv_creation/map_par_id_to_wrdid.py manual_word.dat  manual_id_mapped.dat manual_id_wrdid.dat

echo "Extracting root info for manual..."
python3 $HOME_alignment/csv_creation/get_manual_root.py  manual_id_wrdid.dat manual_lwg_new.dat > manual_mapped_id_root_info.dat

#Create Eng and Hindi Soumya grouping facts
python3 $HOME_alignment/csv_creation/create_facts_from_grouping.py E_Word_Group_Sanity.dat Eng > E_grouping.dat
python3 $HOME_alignment/csv_creation/create_facts_from_grouping.py H_Word_Group.dat Hnd > H_grouping.dat

#Get each word with count of occurences
python3 $HOME_alignment/csv_creation/check_each_word_occurences.py eng_wrd_occurence.dat hnd_wrd_occurence.dat

python3 $HOME_alignment/csv_creation/map_punctuations_in_conll.py E_conll_parse_enhanced > E_conll_parse_enhanced_without_punc.tsv
python3 $HOME_alignment/csv_creation/map_punctuations_in_conll.py hindi_dep_parser_original.dat > hindi_dep_parser_original_without_punc.tsv

#Get parent sanwawi info 
#bash $HOME_alignment/csv_creation/get_parent_sanwawi.sh Eng Hnd   

#Get kriyA_mUla info from Hindi sentence:
python3 $HOME_alignment/csv_creation/check_for_kriyA_mUla.py manual_mapped_id_root_info.dat $HOME_alignment/csv_creation/kriyA_mUla_default_dic.txt > kriyA_mUla_info.dat

#Get anchors:
python3 $HOME_alignment/csv_creation/map_slot_debug_info.py manual_id_wrdid.dat slot_debug_input.txt  > slot_debug_input_mapped.txt
#python3 $HOME_alignment/csv_creation/get_anch_and_pot_info.py slot_debug_input_mapped.txt word.dat  H_wordid-word_mapping.dat  > anchor.dat
python3 $HOME_alignment/csv_creation/get_anch_and_pot_info.py slot_debug_input_mapped.txt word.dat  manual_id_mapped.dat  > anchor.dat

#Create conll facts 
python3 $HOME_alignment/csv_creation/create_facts_from_coll.py E_conll_parse_enhanced_without_punc.tsv eng > eng_conll_facts.dat
python3 $HOME_alignment/csv_creation/create_facts_from_coll.py hindi_dep_parser_original_without_punc.tsv hnd > hnd_conll_facts.dat


#Generating P1 layer
echo "(defglobal ?*path* = $HOME_alignment)" > alignment_path.clp
#myclips -f $HOME_alignment/csv_creation/run.bat > new_layer.error
myclips -f $HOME_alignment/csv_creation/run1.bat > new_layer.error


#Converting P1 layer fact to csv 
#python3 $HOME_alignment/csv_creation/convert_new_layer_fact_to_csv.py new_p_layer_tmp3.dat P1 > p1_layer.csv

sed -i 's/dummy //g' new_layer_p2.dat
#Converting P2 layer fact to csv 
python3 $HOME_alignment/csv_creation/convert_new_layer_fact_to_csv.py new_layer_p2.dat P2 > p2_layer.csv

#python3 $HOME_alignment/csv_creation/get_left_over_wrds.py srun_All_Resources.csv  P1 > p1_left_over_wrds.dat
#python3 $HOME_alignment/csv_creation/get_left_over_wrds.py p1_layer.csv  P1 > p1_left_over_wrds.dat
python3 $HOME_alignment/csv_creation/get_left_over_wrds.py p2_layer.csv  P2 > p2_left_over_wrds.dat
myclips -f $HOME_alignment/csv_creation/run_left_over_wrds.bat >> new_layer.error

#Replacing new layer id with id_wrd format
python3 $HOME_alignment/csv_creation/replace_id_with_wrd.py   manual_id_mapped.dat p2_layer.csv P2 > p2_layer_with_wrd.csv

#python3 $HOME_alignment/csv_creation/add_p1_layer.py  srun_All_Resources.csv srun_All_Resources_id_word.csv P1 p1_layer.csv p1_layer_with_wrd.csv 
#cp j srun_All_Resources.csv
#cp k srun_All_Resources_id_word.csv


#python3 $HOME_alignment/csv_creation/add_p1_layer.py srun_All_Resources.csv  srun_All_Resources_id_word.csv   P2 p2_layer.csv p2_layer_with_wrd.csv  
#cp j srun_All_Resources.csv
#cp k srun_All_Resources_id_word.csv

#python3 $HOME_alignment/csv_creation/check_P_nd_P1_mismatch.py > P_P1_mismatch.dat



#For debugging purpose 
#python3 $HOME_alignment/csv_creation/get_hindi_sentence_with_id_wrd.py  H_wordid-word_mapping.dat > H_sentence_with_ids.dat
python3 $HOME_alignment/csv_creation/get_hindi_sentence_with_id_wrd.py  manual_id_mapped.dat > H_sentence_with_ids.dat
wx_utf8 < H_sentence_with_ids.dat > H_sentence_with_ids_utf8.dat

python3 $HOME_alignment/csv_creation/group.py E_grouping.dat English_grouping > E_grouping.tsv
python3 $HOME_alignment/csv_creation/group.py H_grouping.dat Hindi_grouping > H_grouping.tsv

#sed 's/,/\t/g' srun_All_Resources_id_word.csv > srun_All_Resources_id_word.tsv

#head -1 srun_All_Resources_id_word.tsv > e_sent
#tail -n +2 srun_All_Resources_id_word.tsv > rest 
#
#cut -f1  rest > f1
#cut -f2-1000  rest > f2
#wx_utf8 < f2 > f2_utf8
#paste f1 f2_utf8 > rest.utf8
#cat e_sent rest.utf8 > srun_All_Resources_id_word_utf8.tsv
#
#sed 's/(//g' p1_left_over_wrds.dat | sed 's/)//g' | sed 's/ /,/g'> p1_left_over_wrds.txt
sed 's/(//g' p2_left_over_wrds.dat | sed 's/)//g' | sed 's/ /,/g'> p2_left_over_wrds.txt
sed 's/,/\t/g' p2_layer_with_wrd.csv > p2_layer_with_wrd.tsv
wx_utf8 < p2_layer_with_wrd.tsv > p2_layer_with_wrd_utf8.tsv

python3 $HOME_alignment/csv_creation/prepare_e_sent_and_k_layer_info.py original_word.dat  id_Apertium_output.dat > info.tsv

cat H_sentence_with_ids.dat  H_grouping.tsv E_grouping.tsv info.tsv p2_layer_with_wrd.tsv p2_left_over_wrds.txt > Complete_alignment.csv
cat H_sentence_with_ids_utf8.dat  H_grouping.tsv E_grouping.tsv info.tsv p2_layer_with_wrd_utf8.tsv p2_left_over_wrds.txt > Complete_alignment_utf8.csv

####################
