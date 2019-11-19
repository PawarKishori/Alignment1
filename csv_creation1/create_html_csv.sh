END=`wc -l $HOME_alignment/$1 | awk '{print $1}'`

sh $HOME_alignment/csv_creation1/init.sh $END $1
#sh $HOME_alignment/csv_creation/deciding_verb_tam.sh $1

#sh $HOME_alignment/csv_creation/mul.sh $END  $1
