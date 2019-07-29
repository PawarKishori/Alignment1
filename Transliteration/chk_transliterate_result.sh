#touch /home/kishori/a/tmp_anu_dir/tmp/BUgol2.2E_tmp/transliterate_log.dat
echo > /home/kishori/a/tmp_anu_dir/tmp/$1_tmp/transliterate_log.dat
i=1
n=`wc -l $HOME_alignment/$1 | awk '{print $1}'`
current=`pwd`

while [ $i -le $n ]
do
	sentence_dir='2.'$i
	echo $sentence_dir
	tmp_path=$HOME_anu_tmp/tmp/$1_tmp/$sentence_dir

	python $HOME_alignment/Transliteration/Check_Transliterate_generalised.py -f $tmp_path/E_sentence $tmp_path/H_sentence
	#python $current/run3.py 
	i=`expr $i + 1`
done
