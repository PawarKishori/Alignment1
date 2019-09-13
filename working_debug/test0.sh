filename=$1
#folder_no=$2
i=1
echo $i
END=`wc -l $1 | awk '{print $1}'`
#END=67
echo $END
END=`expr $END + 1`
#for i in $(seq 1 $END)
while [ "$i" -lt $END ]
	do
		
		
		cd $HOME_anu_test/miscellaneous/SMT/phrasal_alignment/align_debug	
		sh $HOME_alignment/working_debug/alignment_debug_org.sh $filename "2."$i
		i=`expr $i + 1`
	done
	
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

