str1="sent_no\th_al_%\te_al_%\te_leftover"
str2="sent_no\th_leftover_ids\te_leftover_ids"
str3="sent_no\th_aligned\te_aligned"
echo -e $str1 > $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info.txt
echo -e $str2 > $HOME_anu_tmp/tmp/$1_tmp/alignment_leftover_info.txt
echo -e $str3 > $HOME_anu_tmp/tmp/$1_tmp/alignment_aligned_info.txt
#n=`wc -l $1 | awk '{print $1}'`
i=1
#n=125 #`ls -d */ | wc -l`
#n=86
END=`wc -l $1 | awk '{print $1}'`
#END=67
#echo $END
END=`expr $END + 1`


current=`pwd`
#echo "$current"
while [ $i -le $END ]
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$1_tmp
        #python working_debug/eng_lwg.py ai2E 2.1

        python $HOME_alignment/working_debug/statistic.py $tmp_path "2."$i
        i=`expr $i + 1`
done
(head -1 $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info.txt && tail -n+2 $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info.txt | sort -k 2gr) > $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info_sorted.txt 
rm $HOME_anu_tmp/tmp/$1_tmp/alignment_percent_info.txt
#sed "1i\ $str" $HOME_anu_tmp/tmp/$1/alignment_percent_info_sorted.txt 


