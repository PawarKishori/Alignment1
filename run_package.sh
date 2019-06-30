#!/bin/bash
## Module 0 =>  manju mam's alignment
#Will run for 100 parallel sentences 

#sh run_all.sh Geo_chap2_E2 Geo_chap2_H2_wx_preprocessed

#==========================================================================
echo "Input files:" $1 $2
cd $HOME_alignment_manju
source activate python2.7               #irshad's parser needs 2.7
sh run_alignment.sh $1 $2 general nsdp
echo "End of manju mam's module: "$1 $2
conda deactivate

echo "==========================================================================\n"
#==========================================================================
cp $HOME_alignment_manju/$1 $HOME_alignment/$1
cp $HOME_alignment_manju/$2  $HOME_alignment/$2

echo "copied $1 and $2 from alignment_manju to $HOME_alignment"

#==========================================================================
cd $HOME_alignment
sh $HOME_alignment/run_alignment.sh $1 $2 
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
#==========================================================================
sh $HOME_alignment/run_only_my_clips_module.sh $1

#==========================================================================
sh $HOME_alignment/run_only_csv_generate.sh $1
#==========================================================================


