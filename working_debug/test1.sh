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
		
		
		source activate py3.6
		python $HOME_alignment/working_debug/add_N1_to_final.py $filename "2."$i
		conda deactivate

		i=`expr $i + 1`
	done
	
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

