filename=$1
i=1
echo $i
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`
while [ "$i" -lt $END ]
        do
                tmp_path=$HOME_anu_tmp/tmp/$1_tmp/"2."$i
                echo "(defglobal ?*hpath* = $HOME_alignment)" > $tmp_path/new_alignment.clp
                echo "2."$i

                python3  $HOME_alignment/working_debug/prepare_facts.py $1 "2."$i

                cd $tmp_path
                myclips -f $HOME_alignment/working_debug/phrase.bat 
                i=`expr $i + 1`
                echo "++++++++++++++++++++++++++++++++++++++++++++++++++"
        done

echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
