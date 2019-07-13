PRES_PATH=`pwd`
MYPATH=$HOME_anu_tmp/tmp/$1_tmp

#------------- For Parser tree purpose -----------------------
$HOME_anu_test/Anu_src/comp.sh combine_apos
$HOME_anu_test/Anu_src/comp.sh get_wordid
sed '1d' $MYPATH/one_sentence_per_line.txt.std.penn > $MYPATH/one_sentence_per_line.txt.std.penn.tmp1
./combine_apos.out  < $MYPATH/one_sentence_per_line.txt.std.penn.tmp1 > $MYPATH/one_sentence_per_line.txt.std.penn.tmp2
#./get_wordid.out < $MYPATH/one_sentence_per_line.txt.std.penn.tmp2  > $MYPATH/one_sentence_per_line.txt.std.penn.tmp3

cd $MYPATH

#$HOME_anu_test/Anu_src/split_file.out one_sentence_per_line.txt.std.penn.tmp3  dir_names.txt  std.penn.tmp
$HOME_anu_test/Anu_src/split_file.out one_sentence_per_line.txt.std.penn.tmp2  dir_names.txt  std.penn.tmp
while read line
do
 cd $line
 myclips -f  $PRES_PATH/run_parser_mapping.bat >  $1_map.error
 sed 's/(parserid-wordid   /sed "s\//' parserid_wordid_mapping_with_punct.dat | sed "s/P\([0-9's]\+\)[ ]\+/P\1\//" | sed 's/)$/\/"/' | sed -n -e "H;\${g;s/\n/ | /g;p}"  | sed 's/^/sed "s\/dummy_sed\/\/" \$1/g' > map.sh
 sh map.sh  $MYPATH/$line/std.penn.tmp  > std.penn.tmp1
 cd ..
done < $MYPATH/dir_names.txt

cd $MYPATH/$2
#sed 's/\([0-9]\)\()\+\)[ ]/\1\2_/g' std.penn.tmp1 > std.penn.tmp2
#sed 's/[A-Z,\$]\+//g' std.penn.tmp2 > std.penn.txt

sed 's/) (\([A-Z$]\)/)_(\1/g' std.penn.tmp1 | sed 's/([A-Z$-\:\.]\+ /(/g' > std.penn.tmp2
 sed 's/\([A-Za-z]\+\)\([)]\+\)[ ](\([,.: ]\+\))_/\1\3\2_/g' std.penn.tmp2 | sed 's/\([A-Za-z]\+\)\([)]\+\)[ ](\([,.: ]\+\))\(.*\)$/\1\3\2\4/g' > std.penn.txt
 #sed 's/\([A-Za-z]\+\)\([)]\+\)[ ](\([,. ]\+\))_/\1\3\2_/g' std.penn.tmp2 > std.penn.txt


cat std.penn.txt >> slot_debug_input.txt
#cat std.penn.tmp2 std.penn.txt >> slot_debug_input.txt
#-------------------------------------------------------------------


sed 's/(Eng_sen / Eng sen : /g' English_sentence.dat | sed 's/)//g'  > eng_sent

cat eng_sent >> slot_debug_input.txt

sed 's/(manual_hin_sen//g' manual_hindi_sen.dat | sed 's/)//g' > man_sent

wx_utf8 < man_sent >  man_sent_wx
wx_utf8 < hindi_sentence.dat > hindi_sentence_wx.dat 

sed 's/^/ Anu : /g'  hindi_sentence_wx.dat >> slot_debug_input.txt
sed 's/^/ Manual sen : /g' man_sent_wx >>  slot_debug_input.txt 

python $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug/print_matrix.py slot_debug_input.txt  English_sentence.dat  manual_word.dat > $1_table
perl $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug/create-html-table.pl < $1_table > $1_table1.html
echo "************************************************************"
#python $PRES_PATH/change.py $1 $2
#perl $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug/create-html-table.pl < $1_table1 > $1_table2.html

#python $PRES_PATH/html_to_csv.py $1 $2 

sed -e 's/<TD>\(.*\)BGCOLOR="#CCFFFF"/<TD BGCOLOR="#CCFFFF" > \1 /g' < $HOME/$1_table1.html | sed -e 's/<TD>\(.*\)BGCOLOR="#DFA800"/<TD BGCOLOR="#DFA800"> \1 /g' > $HOME/$1_$2_table.html

#firefox $HOME/$1_$2_table.html
