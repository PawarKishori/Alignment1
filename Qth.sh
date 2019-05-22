#Author: Kishori
#sh Qth.sh rGitaE_Up_012

file_dir=$1'_tmp'
n=  cat $1 | wc -l
echo "For loop will execute for "
END=101
#for i in $(seq 1 $n)
for i in $(seq 1 $END)
do
	sentence_dir='2.'$i
	#echo $sentence_dir
        echo $tmp_path	
	tmp_path=$HOME_anu_tmp/tmp/$file_dir/$sentence_dir 
	echo "(defglobal ?*hpath* = $HOME_alignment)" > $tmp_path/new_alignment.clp
	cd $tmp_path

	touch $tmp_path/clips_output
	myclips -f  $HOME_alignment/tmp_run_Qth.bat  >  $tmp_path/clips_output.txt 

done
#
python $HOME_alignment/EchunkId-Echunkword.py $HOME_anu_tmp/tmp  $1 
