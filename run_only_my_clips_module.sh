file_dir=$1'_tmp'
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`
for i in $(seq 1 $END)
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$file_dir/$sentence_dir

        cd $tmp_path
	echo "(defglobal ?*hpath* = $HOME_alignment)" > $tmp_path/new_alignment.clp

        myclips -f  $HOME_alignment/tmp_run_Qth.bat  >  $tmp_path/clips_error_kishori
        myclips -f  $HOME_alignment/final_Pth.bat  >>  $tmp_path/clips_error_kishori



done



