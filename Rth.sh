#Author: Ayushi
#To run this shell see the following example:
#The arguement "rGitaE_Up_000" is the name of the tmp folder for which you want to create respective files. 
#sh Rth.sh rGitaE_Up_000
#The arguement "rGitaE_Up_000" is the name of the eng file which is been used as parallel inputs to run alignment. 

tmp_dir_name=$1'_tmp'
tmp_path=$HOME_anu_tmp/tmp/$tmp_dir_name

for i in {1..100}
do
	sent_dir_name='2.'$i
	echo "----------"
	echo $sent_dir_name
	sent_dir_path=$HOME_anu_tmp/tmp/$tmp_dir_name/$sent_dir_name
	
#Rth_clips_debug file saves the clip rule prompt output which can be referred in case of debugging of corresponding clip facts.
	if [ -d $sent_dir_path ]; then
		touch $sent_dir_path/Rth_clips_debug
		cd $sent_dir_path

#Removing "corpus_specific_dic_facts_for_one_sent.dat" and "Hindi_word_with_possible_corpus_specific_dict_eng_mngs_facts.dat" in case they already exist.  This is to ensure that these files are created each time this script is run.
		#rm Hindi_word_with_possible_corpus_specific_dict_eng_mngs_facts.dat 	
		#rm corpus_specific_dic_facts_for_one_sent.dat
		#rm R_layer_final_facts.dat

#Preprocessing steps
		#echo "creating manual_mwe_facts.dat"
		python $HOME_alignment/create_manual_mwe_facts.py 
		#python3 $HOME_alignment/revised_local_word_grouping.py $HOME_alignment $HOME_anu_test/Anu_data
		#echo "creating revised_manual_local_word_group.dat"
		python3 $HOME_alignment/improved_local_word_grouping.py $HOME_alignment $HOME_anu_test/Anu_data
		#echo "creating finite_clauses.dat"
		#python3 $HOME_alignment/clause_facts.py

#The "run_Rth.bat" batch file which loads, processes and saves the facts required for creating the Rth layer (taking alignment decisions)
#It loads "/home/user/WORK/Alignment/align_corpus_specific_H2E_dic_words.clp", "manual_word.dat" and "word.dat"
#and creates "Hindi_word_with_possible_eng_mngs_facts.dat" and "gita_ras_ratnakar_dic_facts_for_one_sent.dat" files.
		#echo "Running run_Rth.bat for "$sent_dir_name
		#myclips -f  $HOME_alignment/run_Rth.bat  >  $sent_dir_path/Rth_clips_debug 
#This python program creates the csv files for the alignment module. The file "clip_facts_to_csv_format.csv" is created in the respective sentence directory for all the sentences in a folder.
#Eg: $HOME_anu_test/collaborator/tmp_anu_dir/tmp/rGitaE_Up_000_tmp/2.10 will have the corresponding "clip_facts_to_csv_format.csv" file at the specified path.
		#echo "creating clip_facts_to_csv_format.csv"
		#python $HOME_alignment/create_csv_from_clip_facts.py 
	fi
done


