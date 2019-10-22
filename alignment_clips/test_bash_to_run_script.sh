file_dir=$1'_tmp'
echo >$HOME_anu_tmp/tmp/$1_tmp/Group_Facts_Parser_POS_log
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`
#END=102

#python3 $HOME_alignment/alignment_clips/e_idgenerator.py $1
#python3 $HOME_alignment/alignment_clips/h_idgenerator.py $1
#python3 $HOME_alignment/alignment_clips/pandas_generalised.py $1    #Old code Apratim
for i in $(seq 1 $END)
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
        python3 $HOME_alignment/alignment_clips/tocsv_converter.py  $tmp_path

done

