#!/bin/bash
##sh run_package.sh Eng Hnd_wx
#==========================================================================
echo "Input files:" $1 $2
cp $1 $HOME_alignment_manju/$1
cp $2 $HOME_alignment_manju/$2


cd $HOME_alignment_manju
source activate python2.7               #irshad's parser needs 2.7
echo "Time taken by alignment_manju module:"
time sh run_alignment.sh $1 $2 general nsdp
echo "End of manju mam's module: "$1 $2
conda deactivate
##==========================================================================
cp $HOME_alignment/$2  $HOME_anu_tmp/tmp/$1_tmp/org_hindi
echo "copied $1 and $2 from alignment_manju to $HOME_alignment"
#==========================================================================
##Adding 1.1 hindi text in hindi file
sed -i  '1iparIkRaNa.' $HOME_anu_tmp/tmp/$1_tmp/org_hindi
##==========================================================================
##Converting hindi original text to canonical text
cd $HOME_alignment
sh $HOME_alignment/canonical/create_canonical.sh $1

##==========================================================================
##Running morph on org_hindi and splitting it into all directories.
sh $HOME_alignment/morph/generate_morph_facts.sh $1
##==========================================================================

##Remove nukta from org_hindi
sh $HOME_alignment/canonical/remove_nukta.sh $1
##==========================================================================
##Integration of technical dictionary


##==========================================================================


#cd $HOME_alignment
sh $HOME_alignment/run_alignment.sh $1 $2 
##==========================================================================
##Roja Transliteration Module
source activate python2.7               #irshad's parser needs 2.7
##Output : Creates Roja_chk_transliterated_words.dat file in respective folder either with 0 or more transliteration etries
sh $HOME_alignment/Transliteration/chk_transliterate_result.sh $1
conda deactivate
##==========================================================================
##Parser's Module
source activate py3.6
python $HOME_alignment/H_Createdata.py $1
python $HOME_alignment/E_Createdata.py $1
##=========================================================================
python $HOME_alignment/Definite_LWG/E_Grouping_Word.py $1
python $HOME_alignment/Definite_LWG/H_Grouping_Word.py $1
conda deactivate 
##==========================================================================
##Need to be replaced by new dictionary lookup using python dictionary
##Ayushi's Module #Prerequisite: create_corpus_specific_gdbm.sh
source activate python2.7
sh $HOME_alignment/run_all.sh $1 $2 &> tam_lwg_errors.txt
##cc resolve module
##sh cc_resolve.sh $1 $2 
conda deactivate
##=========================================================================
sh $HOME_alignment/run_only_my_clips_module.sh $1
##=========================================================================
sh $HOME_alignment/csv_creation/create_html_csv.sh $1
##=========================================================================
## Apratim and Prashant's module to run alignment clips rule
source activate py3.6
sh alignment_clips/test_bash_to_run_script.sh $1
conda deactivate
##=========================================================================
##Align_debug Module
cp -r $HOME_alignment/styles $HOME_anu_tmp/tmp/$1_tmp/
cp -r $HOME_alignment/ihss102.pdf $HOME_anu_tmp/tmp/$1_tmp/
cp -r $HOME_alignment/iess102.pdf $HOME_anu_tmp/tmp/$1_tmp/
cp $HOME_alignment/working_debug/index.html $HOME_anu_tmp/tmp/$1_tmp/

#One time task. alignment_debug_org.sh needed to be placed in following folder as per it's dependency
cp $HOME_alignment/working_debug/alignment_debug_org.sh $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug
sh $HOME_alignment/working_debug/test.sh $1
##=========================================================================
#Ayushi csv geberate module and pratishtha csv to html module.
sh $HOME_alignment/run_only_csv_generate.sh $1
#source activate py3.6
#python $HOME_alignment/csvtohtml/csvtohtml.py $1
#conda deactivate
##=========================================================================
