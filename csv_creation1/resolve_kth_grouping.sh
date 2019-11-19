filename=$1
i=1
echo $i
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`
while [ "$i" -lt $END ]
  do
  echo "2."$i
  source activate py3.6
  tmp=$HOME_anu_tmp/tmp/$1_tmp/"2."$i
  python3 $HOME_alignment/csv_creation/all_words_using_apertium.py $tmp/word.dat $tmp/id_Apertium_output_with_grp.dat $tmp/K_grouping_info.dat $tmp/K_grouping_info1.dat
 
# python  $HOME_alignment/csv_creation/merge_dictionaries.py $HOME_anu_test/Anu_data/canonical_form_dictionary/dictionaries/computer_science_dic_in_canonical_form.txt $HOME_anu_test/Anu_data/canonical_form_dictionary/dictionaries/default-iit-bombay-shabdanjali-dic_smt.txt $HOME_anu_test/Anu_data/canonical_form_dictionary/dictionaries/cs_default_dictionary.txt
 
 python3 $HOME_alignment/csv_creation/meaning_of_every_word_shreya.py $tmp/K_grouping_info1.dat $HOME_anu_test/Anu_data/canonical_form_dictionary/dictionaries/default-iit-bombay-shabdanjali-dic_smt.txt $tmp/resolved_kth_groups.dat

 cut -f1 $tmp/K_grouping_info.dat > $tmp/first_column
 cut -f2 $tmp/resolved_kth_groups.dat > $tmp/second_column
 
 paste $tmp/first_column $tmp/second_column > $tmp/input_to_K_enhanced_layer

 python3 $HOME_alignment/csv_creation/csv_conversion_id_final.py $tmp/input_to_K_enhanced_layer  $tmp/K_enhanced.dat

 python3 $HOME_alignment/csv_creation/K_enhanced_correction.py $tmp/K_enhanced.dat $tmp/E_Group_Facts_Parser_POS.dat $tmp/H_Group_Facts_Parser_POS.dat

  conda deactivate

                i=`expr $i + 1`
        done

echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
