file_dir=$1'_tmp'
#file_dir="ai1E_tmp"
END=`wc -l $1 | awk '{print $1}'`
#END=`expr $END + 1`
#END=102

for i in $(seq 1 $END)
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$1_tmp/$sentence_dir

        python3 $HOME_alignment/hindi_root_processing/module1.py $tmp_path
        python3 $HOME_alignment/hindi_root_processing/verb_3_11_19.py  $tmp_path >  $tmp_path/verb_root_tam_info

        python3 $HOME_alignment/hindi_root_processing/generate_root.py $tmp_path  #c    hange the path acc. to the location of generate_root.py 
        python $HOME_alignment/hindi_root_processing/module4.py $tmp_path
        python3 $HOME_alignment/hindi_root_processing/Exact_match_dict.py $tmp_path/E_sentence $tmp_path/H_sentence $tmp_path/A_exact_match_WSD_modulo.dat
        #english root: revised root.dat
done

