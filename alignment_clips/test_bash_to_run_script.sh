file_dir=$1'_tmp'
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`

python3 $HOME_alignment/alignment_clips/e_idgenerator.py $1
python3 $HOME_alignment/alignment_clips/h_idgenerator.py $1
python3 $HOME_alignment/alignment_clips/anchors_csv_final.py $1
for i in $(seq 1 $END)
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$1_tmp/$sentence_dir

        cd $tmp_path
echo "(defglobal ?*hpath* = $HOME_alignment)" > $tmp_path/new_alignment.clp

     myclips -f  $HOME_alignment/alignment_clips/anchor_clp_run.bat >  $tmp_path/clips_error_alignment
        python3 $HOME_alignment/alignment_clips/tocsv_converter.py  $tmp_path


done
