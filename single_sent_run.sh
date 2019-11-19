python3.6 $HOME_alignment/working_debug/All_Resources.py $1 $2

python3.6 $HOME_alignment/working_debug/Create_potential_and_current_anchors.py $1 $2

##############################################################################################################################################

file_dir=$1'_tmp'
echo >$HOME_anu_tmp/tmp/$1_tmp/Group_Facts_Parser_POS_log

END=`expr $3 + 1`

for i in $(seq $3 $END)
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$1_tmp/$sentence_dir
	python3 $HOME_alignment/alignment_clips/E_Group_Generator.py $tmp_path/E_Word_Group_MFS.dat
	python3 $HOME_alignment/alignment_clips/H_Group_Generator.py $tmp_path/H_Word_Group_MFS.dat
        python3 $HOME_alignment/alignment_clips/Generating_Anchor_Facts.py $1 "2."$i    #Few changes by Jagrati

        cd $tmp_path
        echo "(defglobal ?*hpath* = $HOME_alignment)" > $tmp_path/new_alignment.clp

        myclips -f  $HOME_alignment/alignment_clips/anchor_clp_run.bat >  $tmp_path/clips_error_alignment
        #python3 $HOME_alignment/alignment_clips/tocsv_converter_old.py  
        python3 $HOME_alignment/alignment_clips/clips_to_csv_N1.py $1 "2."$i  

done

##############################################################################################################################################

python3 $HOME_alignment/working_debug/Final_CSV_Generator.py $1 $2

##############################################################################################################################################
# sh $HOME_alignment/working_debug/statistic-shell.sh $1
str1="sent_no\th_al_%\te_al_%\te_leftover"
str2="sent_no\th_leftover_ids\te_leftover_ids"
str3="sent_no\th_aligned\te_aligned"
echo -e $str1 > $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info.txt
echo -e $str2 > $HOME_anu_tmp/tmp/$1_tmp/alignment_leftover_info.txt
echo -e $str3 > $HOME_anu_tmp/tmp/$1_tmp/alignment_aligned_info.txt

END=`expr $3 + 1`
i=$3
current=`pwd`
#echo "$current"
while [ $i -lt $END ]
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$1_tmp
        #python working_debug/eng_lwg.py ai2E 2.1

        python $HOME_alignment/working_debug/statistic.py $tmp_path "2."$i
        i=`expr $i + 1`
done
(head -1 $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info.txt && tail -n+2 $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info.txt | sort -k 2gr) > $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info_sorted.txt
rm $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info.txt
#sed "1i\ $str" $HOME_anu_tmp/tmp/$1/alignment_percent_info_sorted.txt 
##############################################################################################################################################

# sh $HOME_alignment/working_debug/generate_1st_iter_leftover.sh $1
line=$2
rm $HOME_anu_tmp/tmp/$1_tmp/$line/hindi_leftover_ids.dat
rm $HOME_anu_tmp/tmp/$1_tmp/$line/english_leftover_ids.dat
grep -P "^$line\t" $HOME_anu_tmp/tmp/$1_tmp/alignment_leftover_info.txt | cut -f2  > $HOME_anu_tmp/tmp/$1_tmp/$line/hindi_leftover_ids.dat
echo $line"----------------------------------------"
grep -P "^$line\t" $HOME_anu_tmp/tmp/$1_tmp/alignment_leftover_info.txt | cut -f3  > $HOME_anu_tmp/tmp/$1_tmp/$line/english_leftover_ids.dat

x=`cat $HOME_anu_tmp/tmp/$1_tmp/$line/english_leftover_ids.dat`
y=`cat $HOME_anu_tmp/tmp/$1_tmp/$line/hindi_leftover_ids.dat`

echo "(left_over_english " $x ")" > $HOME_anu_tmp/tmp/$1_tmp/$line/english_leftover_ids_fact.dat
echo "(left_over_hindi " $y ")" > $HOME_anu_tmp/tmp/$1_tmp/$line/hindi_leftover_ids_fact.dat

cat $HOME_anu_tmp/tmp/$1_tmp/$line/hindi_leftover_ids.dat
echo "-"
cat $HOME_anu_tmp/tmp/$1_tmp/$line/english_leftover_ids.dat

python3 $HOME_alignment/working_debug/extract_left_over_words.py $1 $line


##############################################################################################################################################

python3 $HOME_alignment/working_debug/srun_All_Resources.py $1 $2

python3 $HOME_alignment/working_debug/srun_All_Resources_id_word.py $1 $2

cat $HOME_anu_tmp/tmp/$1_tmp/$2/K_enhanced.dat
echo "\n"
cat $HOME_anu_tmp/tmp/$1_tmp/$2/K_enhanced_corrected.dat
echo "\n"

python3 $HOME_alignment/working_debug/CSV_to_HTML.py $filename $1 $2

