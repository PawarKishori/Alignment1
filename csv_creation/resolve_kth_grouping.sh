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
  python3 $HOME_alignment/csv_creation/making_group_using_id_Apertium_word_dat.py $tmp/word.dat $tmp/id_Apertium_output_with_grp.dat $tmp/K_grouping_info.dat
  #python3 $HOME_alignment/csv_creation/making_list_using_grouping_information.py $tmp/srun_All_Resources_id_word.csv $tmp/id_Apertium_output_with_grp.dat $tmp/K_grouping_info.dat
  python3 $HOME_alignment/csv_creation/meaning_of_every_word_shreya.py $tmp/K_grouping_info.dat $HOME_anu_test/Anu_data/domain/computer_science_dic.txt $tmp/resolved_kth_groups.dat
  conda deactivate

                i=`expr $i + 1`
        done

echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


