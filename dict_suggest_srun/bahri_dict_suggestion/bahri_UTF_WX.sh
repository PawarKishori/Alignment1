#!/bin/bash
#written by Raj Rajeshwari Kayan. For queries mail at:rajrajeshwarikayan@gmail.com
cd $HOME_anu_tmp/tmp/
corpus=$1
cd $corpus'_tmp/'
for i in 2.*
do
cd $i
cp hindi_leftover_words.dat $HOME/Convert_utf_wx/
cd $HOME/Convert_utf_wx/
sh wx_to_utf8.sh hindi_leftover_words.dat hindi_leftover_words_utf.dat
cp hindi_leftover_words_utf.dat $HOME_anu_tmp/tmp/$corpus'_tmp/'$i
cd $HOME_anu_tmp/tmp/$corpus'_tmp/'$i
cd ..
done
cd $HOME_alignment/dict_suggest_srun/bahri_dict_suggestion
# now calling the python program to lookup in the dictionary
python3 bahri_lookup.py $corpus
# now removing the extra file hindi_leftover_words_utf.dat which was created in the process
cd $HOME_anu_tmp/tmp/
cd $corpus'_tmp/'
for i in 2.*
do
cd $i
if test -f hindi_leftover_words_utf.dat; then
	rm hindi_leftover_words_utf.dat
fi
cd ..
done
# 
cd $HOME_anu_tmp/tmp/
cd $corpus'_tmp/'
for i in 2.*
do
cd $i
cp srun_bahri_dict_suggestion.dat $HOME/Convert_utf_wx/
cd $HOME/Convert_utf_wx/
sh utf8_to_wx.sh srun_bahri_dict_suggestion.dat srun_bahri_dict_suggestion1.dat
mv srun_bahri_dict_suggestion1.dat $HOME_anu_tmp/tmp/$corpus'_tmp/'$i/srun_bahri_dict_suggestion.dat
cd $HOME_anu_tmp/tmp/$corpus'_tmp/'$i
cd ..
done
