END=`wc -l $HOME_alignment/$1 | awk '{print $1}'`

sh $HOME_alignment/csv_creation/init.sh $END $1
#sh $HOME_alignment/csv_creation/mul.sh $END  $1
