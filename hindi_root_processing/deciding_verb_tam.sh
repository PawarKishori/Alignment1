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
        #python3 $HOME_alignment/hindi_root_processing/module1.py $tmp_path > $tmp_path/VP_expr_by_hindi_parser
        python3 $HOME_alignment/hindi_root_processing/verb_3_16.py  $tmp_path tmp 
        #Nupur's code for hindi root
        python $HOME_alignment/hindi_root_processing/generate_root.py  $tmp_path/hindi.morph.dat $tmp_path/hindi_parser_canonial.dat #c    hange the path acc. to the location of generate_root.py 

        #english root: revised root.dat
done

