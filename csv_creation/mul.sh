a=1
current=`pwd`
while [ $a -lt $1 ]
do
    echo "+++++++++++++++++++++++++++++++++++++++++"
    echo 2.$a
    cp $HOME_alignment/csv_creation/invert_csv.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    cp $HOME_alignment/csv_creation/allfacts_csv.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    #cp invert_stage1.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    #cp conversion.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    #cp invert_stage2.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a
    #cp alldebugfacts.py $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a

    cd $HOME_anu_tmp/tmp/BUgol2.1E_tmp/2.$a

    python3 invert_csv.py
    python3 allfacts_csv.py


    #python3 invert_stage1.py
    #python3 conversion.py
    #python3 invert_stage2.py
    #python3 alldebugfacts.py
    rm invert_csv.py
    rm allfacts_csv.py
    #rm invert_stage1.py
    #rm conversion.py
    #rm invert_stage2.py
    #rm alldebugfacts.py
    echo $current
    cd $current
    # Print the values
    echo $a

    a=`expr $a + 1`
done
