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


#python3 $HOME_alignment/csv_creation/get_manual_root_nd_tam.py H_wordid-word_mapping.dat verb_root_tam_info $HOME_alignment/csv_creation/kriyA_mUla_default_dic.txt  $HOME_alignment/csv_creation/kriyA_mUla.txt_wx > verb_root_tam_info.dat

cd $tmp_path
python3 $HOME_alignment/csv_creation/get_manual_root_nd_tam.py $tmp_path/H_wordid-word_mapping.dat $tmp_path/verb_root_tam_info $HOME_alignment/csv_creation/kriyA_mUla_default_dic.txt  $HOME_alignment/csv_creation/kriyA_mUla.txt_wx > $tmp_path/verb_root_tam_info.dat

python3 $HOME_alignment/csv_creation/verb_alignment.py  $tmp_path/verb_root_tam_info.dat $tmp_path/anu_root.dat

done

