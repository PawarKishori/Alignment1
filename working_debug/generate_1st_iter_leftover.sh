while read line 
do
rm $HOME_anu_tmp/tmp/$1_tmp/$line/hindi_leftover_ids.dat
rm $HOME_anu_tmp/tmp/$1_tmp/$line/english_leftover_ids.dat
grep -P "^$line\t" $HOME_anu_tmp/tmp/$1_tmp/alignment_leftover_info.txt | cut -f2  > $HOME_anu_tmp/tmp/$1_tmp/$line/hindi_leftover_ids.dat
echo $line"----------------------------------------"
grep -P "^$line\t" $HOME_anu_tmp/tmp/$1_tmp/alignment_leftover_info.txt | cut -f3  > $HOME_anu_tmp/tmp/$1_tmp/$line/english_leftover_ids.dat
cat $HOME_anu_tmp/tmp/$1_tmp/$line/hindi_leftover_ids.dat
echo "-"
cat $HOME_anu_tmp/tmp/$1_tmp/$line/english_leftover_ids.dat

python3 $HOME_alignment/working_debug/extract_left_over_words.py $1 $line

done < $HOME_anu_tmp/tmp/$1_tmp/dir_names.txt 

