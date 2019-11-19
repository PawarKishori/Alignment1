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

                echo "2."$i
                #source activate py3.6
                python3 $HOME_alignment/working_debug/Final_CSV_Generator.py $filename "2."$i
                #python3 $HOME_alignment/working_debug/All_Resources_id_word.py $filename "2."$i
                #python3 $HOME_alignment/working_debug/CSV_to_HTML.py $filename "2."$i
                #conda deactivate

                i=`expr $i + 1`
        done

echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
