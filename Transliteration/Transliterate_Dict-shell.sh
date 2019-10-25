python3 $HOME_alignment/Transliteration/Acronym_Dict.py $1 $2
echo "____________"
python3 $HOME_alignment/Transliteration/Transliterate_Dict.py $1 $2  

echo "____________"
python3 $HOME_alignment/Transliteration/Remove_entries_handled_by_acronym_from_Transliterate.py




file_dir=$1'_tmp'
END=`wc -l $1 | awk '{print $1}'`

for i in $(seq 1 $END)
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$1_tmp/$sentence_dir
        python3 $HOME_alignment/Transliteration/Exact_match_dict.py $tmp_path/E_sentence $tmp_path/H_sentence $tmp_path/Tranliterated_words_first_run.dat
        cat $tmp_path/Transliterate1.csv
done

