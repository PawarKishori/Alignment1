#sh $HOME_alignment/generate_basic_facts.sh $1

tmp=$HOME_anu_tmp/tmp
file_dir=$1'_tmp'
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`

echo "No. of eng sentences: " $END

python split_into_tmp.py $1 E_sentence $1  #$1 i.e. BUgol2.1E is without test. sentence
python split_into_tmp.py $2 H_sentence_org $1  #$2 i.e. BUgol2.1H is without parIkshan. sentence
python split_into_tmp_1_test.py $tmp/$file_dir/hindi_canonical H_sentence $1    #hindi_canonical is with parIkshan. sentence, H_sentence is canonical
python split_into_tmp_1_test.py $tmp/$file_dir/org_hindi_without_nukta H_sentence_without_nukta $1    #hindi_canonical is with parIkshan. sentence, H_sentence is canonical


for i in $(seq 1 $END)
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$file_dir/$sentence_dir

        cd $tmp_path
        cat E_sentence
        cat H_sentence
        #++++++++++++++++++++++++++++++++++++++++ GENERATION OF GENERALISED BASIC FACTS ++++++++++++++++++++++++++++++++++++++++++
        #python $HOME_alignment/generate_facts.py $tmp_path/H_sentence $tmp_path
        #python $HOME_alignment/generate_facts.py $tmp_path/E_sentence $tmp_path

        #++++++++++++++++++++++++++++++++++++++++ GENERATION OF DEFINITE FACTS ++++++++++++++++++++++++++++++++++++++++++
        # python lwg_knowledge_base.py /home/kishori/forked/tmp_anu_dir/tmp/cl_english_100_detok_tmp/2.1/H_sentence /home/kishori/forked/tmp_anu_dir/tmp/cl_english_100_detok_tmp/2.1
        #python $HOME_alignment/lwg_knowledge_base.py $tmp_path/H_sentence $tmp_path $HOME_alignment/vibhakti

        #++++++++++++++++++++++++++++++++++++++++ ENGLISH PARSER OUTPUT GENERATION MODULE ++++++++++++++++++++++++++++++++++++++++++
        #Run Stanford parser for english sentence parse 
 #sh $HOME_alignment/run_new_stanford-parser.sh $tmp_path/E_sentence $tmp_path 
        #Generating English parser facts from E_conll_parse and E_sentence
	

	#++++++++++++++++++++++++++++++++++++++++  Clips to generate constituency parse +++++++++++++++++++++++++++++++++++++++++++++++
        #echo "(defglobal ?*hpath* = $HOME_alignment)" > $tmp_path/new_alignment.clp

        #touch $tmp_path/clips_error_kishori
        #myclips -f  $HOME_alignment/tmp_run_Qth.bat  >  $tmp_path/clips_error_kishori
        #myclips -f  $HOME_alignment/final_Pth.bat  >>  $tmp_path/clips_error_kishori

done



