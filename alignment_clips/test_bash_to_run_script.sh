file_dir=$1'_tmp'
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`
python3 e_idgenerator.py $file_dir
python3 h_idgenerator.py $file_dir
python3 anchors_csv_final.py $file_dir
for i in $(seq 1 $END)
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME/Downloads/BUgol_27_aug/$1_tmp/$sentence_dir

        cd $tmp_path
echo "(defglobal ?*hpath* = $HOME_alignment)" > $tmp_path/new_alignment.clp

     myclips -f  /home/hackhard/prgrams/anchor_clp_run.bat >  $tmp_path/clips_error_allingnment
        echo "EXXX"
        python3 /home/hackhard/prgrams/tocsv_converter.py  $tmp_path
        echo "dafad"


done

