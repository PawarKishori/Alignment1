#Written by Roja(0

#Extracting K layer root and tam info , O/p: anu_root.dat
echo "Extracting K layer root and Tam info..."
python3 $HOME_alignment/csv_creation/extract_anu_root_nd_tam.py id_Apertium_input.dat > anu_root.dat

echo "Extracting root info for manual..."
python3 $HOME_alignment/csv_creation/extract_hindi_id_root.py

echo "Creating csv..."
#Extracting K layer info to get K, K_exact_without_vib, K_par, K_Root, K_Dic layers , O/p: H_alignment_parserid.csv
#python3 $HOME_alignment/csv_creation/csv_format.py
python3 $HOME_alignment/csv_creation/K_layer_alignment.py $HOME_alignment/vibhakti

echo "Creating csv for 1st word capital..."
#Extracting Proper noun info : O/p: K_1st_letter_capital_word.csv
python3 $HOME_alignment/csv_creation/check_proper_noun_mng.py $HOME_anu_test/Anu_data/canonical_form_dictionary/dictionaries/computer_science_dic_in_canonical_form.txt  $HOME_anu_test/Anu_data/canonical_form_dictionary/dictionaries/default-iit-bombay-shabdanjali-dic_smt.txt

echo "Aligning MWE..."
#Aligning MWE words : O/p: K_exact_mwe_word_align.csv
python3 $HOME_alignment/csv_creation/align_mwe.py  hindi_meanings_with_grp_ids.dat  $HOME_alignment/csv_creation/mwe_tech_dic.txt

echo "Extract kriyA_mUla Root and ids info..."
#Get ids for verb root , extracting verb root for kriyA mUla O/p: verb_root_tam_info.dat
python3 $HOME_alignment/csv_creation/get_manual_root_nd_tam.py  $HOME_alignment/csv_creation/kriyA_mUla_default_dic.txt  $HOME_alignment/csv_creation/kriyA_mUla.txt_wx $HOME_alignment/csv_creation/verb_default_dic.txt > verb_root_tam_info.dat

echo "Alignining Verb using tam..."
python3 $HOME_alignment/csv_creation/get_K_layer_align_using_tam_info.py

echo "Aligning Verb..."
#Verb Alignment, O/p: H_alignment_parserid-new.csv
python3 $HOME_alignment/csv_creation/verb_alignment.py  verb_root_tam_info.dat anu_root.dat

