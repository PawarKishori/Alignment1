a=1
current=`pwd`
while [ $a -lt $1 ]
do
    cp $HOME_alignment/csv_creation/sent_details.py $HOME_anu_tmp/tmp/$2_tmp/2.$a
    
    cp $HOME_alignment/csv_creation/csv_format.py $HOME_anu_tmp/tmp/$2_tmp/2.$a
    cp $HOME_alignment/vibhakti $HOME_anu_tmp/tmp/$2_tmp/2.$a
    cp $HOME_alignment/csv_creation/csv_parserid_to_wordid.py $HOME_anu_tmp/tmp/$2_tmp/2.$a
    cp $HOME_alignment/csv_creation/sentence_details_word.py $HOME_anu_tmp/tmp/$2_tmp/2.$a
    cp $HOME_alignment/csv_creation/csv_word.py $HOME_anu_tmp/tmp/$2_tmp/2.$a
    cp $HOME_alignment/csv_creation/extract_anu_root.py $HOME_anu_tmp/tmp/$2_tmp/2.$a
    cp $HOME_alignment/csv_creation/extract_hindi_id_root.py $HOME_anu_tmp/tmp/$2_tmp/2.$a
    
    echo "HELLO"
    cd $HOME_anu_tmp/tmp/$2_tmp/2.$a
    python3 sent_details.py
    echo 2.$a 
    python extract_anu_root.py id_Apertium_input.dat > anu_root.dat
    python3 extract_hindi_id_root.py 
    python3 csv_format.py
    python3 csv_parserid_to_wordid.py
    python3 sentence_details_word.py
    python3 csv_word.py


    rm sent_details.py
    rm csv_format.py
    rm csv_parserid_to_wordid.py
    rm sentence_details_word.py
    rm csv_word.py
    rm extract_anu_root.py
    rm extract_hindi_id_root.py
    rm vibhakti
    #cd ../../shell
    cd $current
#	# Print the values
    echo $a
    a=`expr $a + 1`
done
