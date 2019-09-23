tmp_path_old=$HOME_anu_tmp/tmp/$1_tmp

i=1
END=102
#END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 2`
while [ "$i" -lt $END ]
	do
	tmp_path=$tmp_path_old'/2.'$i
	echo $tmp_path
	apertium-destxt  $tmp_path/$2 | lt-proc -ac $HOME_anu_test/bin/hi.morf.bin | apertium-retxt >  $tmp_path/hindi.morph
	./$HOME_alignment/morph/morph.out $tmp_path/$2'_hindi.morph.txt' $tmp_path/$2'_hindi.verb_morph.txt' < $tmp_path/hindi.morph > /dev/null
	i=`expr $i + 1`
	done
