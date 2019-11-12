i=1
END=`wc -l $1 | awk '{print $1}'`
while [ "$i" -le $END ]
 do
 echo "--------2."$i
 python $HOME_alignment/E_Createdata_one.py $1 "2."$i
 #python $HOME_alignment/H_Createdata_one.py $1 "2."$i
 i=`expr $i + 1`
done
