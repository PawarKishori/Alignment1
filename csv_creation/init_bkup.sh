a=1
current=`pwd`
while [ $a -lt $1 ]
do
    cp sent_details.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    cp csv_format.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    cp csv_parserid_to_wordid.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    cp sentence_details_word.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    cp csv_word.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    echo "HELLO"
    cd $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    python3 sent_details.py
    python3 csv_format.py
    python3 csv_parserid_to_wordid.py
    python3 sentence_details_word.py
    python3 csv_word.py

    rm sent_details.py
    rm csv_format.py
    rm csv_parserid_to_wordid.py
    rm sentence_details_word.py
    rm csv_word.py
    #cd ../../shell
    cd $current
	# Print the values
    echo $a
    a=`expr $a + 1`
done
