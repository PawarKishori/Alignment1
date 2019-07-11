a=1

while [ $a -lt $1 ]
do
    cp invert_csv.py ../BUgol2.1E_tmp/2.$a
    cp allfacts_csv.py ../BUgol2.1E_tmp/2.$a
    cp invert_stage1.py ../BUgol2.1E_tmp/2.$a
    cp conversion.py ../BUgol2.1E_tmp/2.$a
    cp invert_stage2.py ../BUgol2.1E_tmp/2.$a
    cp alldebugfacts.py ../BUgol2.1E_tmp/2.$a

    cd ../BUgol2.1E_tmp/2.$a

    python3 invert_csv.py
    python3 allfacts_csv.py


    python3 invert_stage1.py
    python3 conversion.py
    python3 invert_stage2.py
    python3 alldebugfacts.py
    rm invert_csv.py
    rm allfacts_csv.py
    rm invert_stage1.py
    rm conversion.py
    rm invert_stage2.py
    rm alldebugfacts.py

    cd ../../csv_creation
    # Print the values
    echo $a

    a=`expr $a + 1`
done
