filename=$1
folder_no=$2
i=87


while [ "$i" -lt 90]
	do
		
		cd $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug	
		sh alignment_debug_org.sh $filename "2."$i
	
		#python sanity_check.py "2."$i 
		
		#sent_id_path=$HOME_anu_tmp/tmp/$1_tmp/2.$i		
		#echo $sent_id_path
		#cd $sent_id_path
		#python $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug/change.py $filename "2."$i
		python $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug/html_to_csv.py  $filename "2."$i
		python3 $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug/parser_csv.py $filename "2."$i
	   	
		i=`expr $i + 1`
	done
	
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

