tmp_path=$HOME_anu_tmp/tmp/$1_tmp

echo $tmp_path
#Get morph info for each word
apertium-destxt  $tmp_path/hindi_canonical | lt-proc -ac $HOME_anu_test/bin/hi.morf.bin | apertium-retxt >  $tmp_path/hindi.morph

#Get morph info in facts format
$HOME_alignment/morph/morph.out $tmp_path/hindi.morph.facts $tmp_path/hindi.verb_morph.txt < $tmp_path/hindi.morph > /dev/null

cd $tmp_path
$HOME_anu_test/Anu_src/split_file.out  hindi.morph.facts dir_names.txt hindi.morph.dat



