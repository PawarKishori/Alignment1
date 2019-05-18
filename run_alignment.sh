tmp_path=$HOME_anu_tmp/tmp/
python split_into_tmp.py $1 E_sentence $1
python split_into_tmp.py $2 H_sentence $1

#sh $HOME_alignment/generate_basic_facts.sh $1


file_dir=$1'_tmp'
n=  cat $1 | wc -l
echo "For loop will execute for "
echo $n
END=100
#for i in $(seq 1 $n)
for i in $(seq 1 $END)
do
        sentence_dir='2.'$i
        echo $sentence_dir
        tmp_path=$HOME_anu_tmp/tmp/$file_dir/$sentence_dir

        cd $tmp_path
        cat E_sentence
        cat H_sentence
        #++++++++++++++++++++++++++++++++++++++++ GENERATION OF GENERALISED BASIC FACTS ++++++++++++++++++++++++++++++++++++++++++
        python $HOME_alignment/generate_facts.py $tmp_path/H_sentence $tmp_path
        python $HOME_alignment/generate_facts.py $tmp_path/E_sentence $tmp_path

        #++++++++++++++++++++++++++++++++++++++++ GENERATION OF DEFINITE FACTS ++++++++++++++++++++++++++++++++++++++++++
        # python lwg_knowledge_base.py /home/kishori/forked/tmp_anu_dir/tmp/cl_english_100_detok_tmp/2.1/H_sentence /home/kishori/forked/tmp_anu_dir/tmp/cl_english_100_detok_tmp/2.1
        python $HOME_alignment/lwg_knowledge_base.py $tmp_path/H_sentence $tmp_path $HOME_alignment/vibhakti

        #++++++++++++++++++++++++++++++++++++++++ ENGLISH PARSER OUTPUT GENERATION MODULE ++++++++++++++++++++++++++++++++++++++++++
        #Run Stanford parser for english sentence parse 
        sh $HOME_alignment/run_new_stanford-parser.sh $tmp_path/E_sentence $tmp_path >> temp
        #Generating English parser facts from E_conll_parse and E_sentence


done



