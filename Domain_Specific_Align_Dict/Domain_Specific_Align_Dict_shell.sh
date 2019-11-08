echo > $HOME_anu_tmp/tmp/$1_tmp/Domain_Specific_Align_Dict.log
i=1
n=`wc -l $HOME_alignment/$1 | awk '{print $1}'`
#n=86
current=`pwd`

while [ $i -le $n ]
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$1_tmp/$sentence_dir
        python $HOME_alignment/Domain_Specific_Align_Dict/Domain_Specific_Align_Dict.py $1 $sentence_dir
        #python $current/run3.py 
        i=`expr $i + 1`
done
