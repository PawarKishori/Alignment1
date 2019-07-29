
tmp_dir_name=$1'_tmp'
tmp_path=$HOME_anu_tmp/tmp/$tmp_dir_name
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`

for i in $(seq 1 $END)
do
	sent_dir_name='2.'$i
        echo $sent_dir_name
        sent_dir_path=$HOME_anu_tmp/tmp/$tmp_dir_name/$sent_dir_name
	cd $sent_dir_path

#	python $HOME_alignment/create_csv_from_clip_facts_latest_1_with_ids.py
	#python $HOME_alignment/create_csv_new_words_and_ids.py
	python $HOME_alignment/create_csv_new_words_and_ids.py
	#cd /home/kishori/Convert_utf_wx
	#sh /home/kishori/Convert_utf_wx/wx_to_utf8.sh < $sent_dir_path/clips_to_csv_words.csv >$sent_dir_path/clips_to_csv_words_utf.csv
	sh /home/kishori/Convert_utf_wx/wx_to_utf8.sh < clips_to_csv_words.csv > clips_to_csv_utf_words.csv

done


