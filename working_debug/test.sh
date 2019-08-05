filename=$1
#folder_no=$2
i=1
echo $i
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`
#for i in $(seq 1 $END)
while [ "$i" -lt $END ]
	do
		
		
		cd $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug	
		sh alignment_debug_org.sh $filename "2."$i
		source activate py3.6
		python $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug/csv_generate.py $filename "2."$i
		conda deactivate

		#python $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug/html_to_csv.py  $filename "2."$i
		#python $HOME_alignment/working_debug/check_prerequisite.py $filename "2."$i
		#python3 $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug/Parser_facts_in_csv.py $filename "2."$i
		i=`expr $i + 1`
	done
	
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

