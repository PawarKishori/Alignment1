END=`wc -l $1 | awk '{print $1}'`
i=1
while [ $i -le $END ]
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$1_tmp/$sentence_dir
        python3 $HOME_alignment/Transliteration/Transliteration_Second_Run.py  $tmp_path/english_leftover_words.dat $tmp_path/hindi_leftover_words.dat #path to be changed acc to your file location
        i=`expr $i + 1`
done
