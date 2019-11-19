##==========================================================================
cp $HOME_alignment/$2  $HOME_anu_tmp/tmp/$1_tmp/org_hindi
echo "copied $1 and $2 from alignment_manju to $HOME_alignment"
#==========================================================================
##Adding 1.1 hindi text in hindi file
sed -i  '1iparIkRaNa.' $HOME_anu_tmp/tmp/$1_tmp/org_hindi
##==========================================================================
##Converting hindi org_hindi to hindi_canonical
cd $HOME_alignment
sh $HOME_alignment/canonical/create_canonical.sh $1

##==========================================================================
##Running morph on org_hindi and splitting it into all directories.
sh $HOME_alignment/morph/generate_morph_facts.sh $1
##==========================================================================
##Remove nukta from org_hindi, hence this module will create org_hindi_without_nukta in tmp
sh $HOME_alignment/canonical/remove_nukta.sh $1


#sh $HOME_alignment/run_alignment.sh $1 $2    #DON'T Foregt to remove comment

####################################################################################################################
## Given a Lookup_dict for a corpus, this module generates Tech_dict_lookup.dat for each 2.1, 2.2 etc. directories
## File generated by this module will be input of working_debug/All_Resources.py

sh $HOME_alignment/tech_dict/run_tech-dict.sh $1 $2 $HOME_alignment/dictionary/Lookup_dict_ai


#####################################################################################################################
# Given a Lookup_transliterated_dict for a corpus, this module generates Tranliterated_words_first_run.dat for each 2.1, 2.2 etc. directories.

filename=$1
i=1
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`
while [ "$i" -lt $END ]
    do
    python3 $HOME_alignment/Transliteration/generate_transliterated_file_for_every_sentences.py $1 Lookup_transliteration_AI_all_eng.txt  "2."$i
    #python3 $HOME_alignment/Transliteration/generate_transliterated_file_for_every_sentences.py $1 Lookup_transliteration_final_histE.txt  "2."$i
    i=`expr $i + 1` 
    done


#####################################################################################################################

sh $HOME_alignment/run_only_my_clips_module.sh $1
#####################################################################################################################


##Parser's Module
source activate py3.6
#python $HOME_alignment/H_Createdata.py $1
#python $HOME_alignment/E_Createdata.py $1     #DON'T Foregt to remove comment
conda deactivate
#sh $HOME_alignment/hindi_wordid_sanity.sh $1

##=========================================================================
#python $HOME_alignment/Definite_LWG/E_Grouping_Word_Dependency.py $1
#python $HOME_alignment/Definite_LWG/H_Grouping_Word.py $1
##source activate py3.6
sh $HOME_alignment/Definite_LWG/Run_Grouping_Files.sh $1

##conda deactivate
#####################################################################################################################

#sh $HOME_alignment/hindi_root_processing/deciding_verb_tam.sh $1    #DON'T Foregt to remove comment


#####################################################################################################################

#Calling Shreya's module to get K_enhanced.dat
sh $HOME_alignment/csv_creation/resolve_kth_grouping.sh $1

#####################################################################################################################

#For P layer 
sh $HOME_alignment/csv_creation1/create_html_csv.sh $1

#####################################################################################################################


#''''''''''''''''''''''''''''''''''''''''''''''''''''
sh $HOME_alignment/csv_creation/run_K_layer.sh $1

sh $HOME_alignment/csv_creation/create_html_csv.sh $1        #No more needed for roja mam's module

cd $HOME_anu_tmp/tmp/$1_tmp
while read line 
do
   cd $line	
  	 bash $HOME_alignment/csv_creation/run_K_layer_alignment.sh
   cd ..
done < dir_names.txt	
#####################################################################################################################

sh $HOME_alignment/Domain_Specific_Align_Dict/Domain_Specific_Align_Dict_shell.sh $1

#####################################################################################################################


cd $HOME_alignment

sh $HOME_alignment/working_debug/test3.sh $1
sh $HOME_alignment/alignment_clips/test_bash_to_run_script.sh $1
cp -r $HOME_alignment/styles $HOME_anu_tmp/tmp/$1_tmp/
sh $HOME_alignment/working_debug/test4.sh $1


#####################################################################################################################
sh $HOME_alignment/working_debug/statistic-shell.sh $1
sh $HOME_alignment/working_debug/generate_1st_iter_leftover.sh $1

#####################################################################################################################
# 2 Run programs (H_wordnet and Bahri)
sh $HOME_alignment/dict_suggest_srun/bahri_dict_suggestion/bahri_UTF_WX.sh $1
python3 $HOME_alignment/dict_suggest_srun/h_wordnet_suggest/Srun_H_wordnet_suggested_words.py $1
sh $HOME_alignment/Transliteration/Transliteration_Second_Run-shell.sh $1


sh $HOME_alignment/working_debug/test5.sh $1
#####################################################################################################################
#sh $HOME_alignment/working_debug/statistic-shell.sh $1

##################################################################################################################
