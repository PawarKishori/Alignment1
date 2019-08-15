#!/bin/bash
#sh run_package.sh Eng Hnd_wx
#==========================================================================
echo "Input files:" $1 $2
cd $HOME_alignment_manju
source activate python2.7               #irshad's parser needs 2.7
echo "Time taken by alignment_manju module:"
#time sh run_alignment.sh $1 $2 general nsdp
echo "End of manju mam's module: "$1 $2
conda deactivate

#==========================================================================
cp $HOME_alignment_manju/$1 $HOME_alignment/$1
cp $HOME_alignment_manju/$2  $HOME_alignment/$2

echo "copied $1 and $2 from alignment_manju to $HOME_alignment"
#==========================================================================

cd $HOME_alignment
sh $HOME_alignment/run_alignment.sh $1 $2 
#==========================================================================

#Roja Transliteration Module
source activate python2.7               #irshad's parser needs 2.7
cd $HOME_alignment
sh $HOME_alignment/Transliteration/chk_transliterate_result.sh $1
conda deactivate

#==========================================================================
#Parser's new module by interns
source activate py3.6
#python $HOME_alignment/Createdata.py $1
python $HOME_alignment/H_Createdata.py $1
python $HOME_alignment/E_Createdata.py $1
conda deactivate 

#==========================================================================
# Ayushi's Module
source activate python2.7
sh $HOME_alignment/run_all.sh $1 $2 &> tam_lwg_errors.txt
#cc resolve module
#sh cc_resolve.sh $1 $2 
conda deactivate
#=========================================================================
sh $HOME_alignment/run_only_my_clips_module.sh $1
#==========================================================================
sh $HOME_alignment/run_only_csv_generate.sh $1
#==========================================================================
sh $HOME_alignment/csv_creation/create_html_csv.sh $1
#==========================================================================
#Align_debug Module
cp $HOME_alignment/working_debug/alignment_debug_org.sh $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug
sh $HOME_alignment/working_debug/test.sh $1
cp -r styles $HOME_anu_tmp/$1_tmp/
#==========================================================================
#source activate py3.6
#python $HOME_alignment/csvtohtml/csvtohtml.py $1
#conda deactivate
#==========================================================================
