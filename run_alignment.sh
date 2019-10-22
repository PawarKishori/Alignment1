#sh $HOME_alignment/generate_basic_facts.sh $1

tmp=$HOME_anu_tmp/tmp
file_dir=$1'_tmp'
END=`wc -l $1 | awk '{print $1}'`
END=`expr $END + 1`

echo "No. of eng sentences: " $END


#source activate python2.7
#Running hindi parser on hindi_canonical(1.parIkSaNa + 100 canonical sentences) 
#sh $hindi_parser/run_hindi_parser.sh $tmp/$file_dir/hindi_canonical $tmp/$file_dir/hindi_dep_parser_out_canonical.txt
#sed 's/^$/;~~~~~~~~~~/g' $tmp/$file_dir/hindi_dep_parser_out_canonical.txt > $tmp/$file_dir/hindi_dep_parser_original_canonical.txt
#$HOME_anu_test/Anu_src/split_file.out hindi_dep_parser_original_canonical.txt dir_names.txt hindi_dep_parser_original_canonical.dat
#conda deactivate


python split_into_tmp.py $1 E_sentence $1  #$1 i.e. BUgol2.1E is without test. sentence
python split_into_tmp.py $2 H_sentence_org $1  #$2 i.e. BUgol2.1H is without parIkshan. sentence

#The following 2 lines and python code is patch up work, most correct way to do this task is to generate <p> </p> tags hindi files, then calling split_file.out to split all these files in 2.1, 2.2 etc.
python split_into_tmp_1_test.py $tmp/$file_dir/hindi_canonical H_sentence $1    #hindi_canonical is with parIkshan. sentence, H_sentence is canonical
python split_into_tmp_1_test.py $tmp/$file_dir/org_hindi_without_nukta H_sentence_without_nukta $1    #hindi_canonical is with parIkshan. sentence, H_sentence is canonical


#################################

#Creation Canonical version of hindi parse output.

cut -f1 $tmp/$file_dir/hindi_dep_parser_original.txt > $tmp/$file_dir/temp_id_column
cut -f2 $tmp/$file_dir/hindi_dep_parser_original.txt > $tmp/$file_dir/temp_word_column
cut -f3-10 $tmp/$file_dir/hindi_dep_parser_original.txt > $tmp/$file_dir/temp_remaining_column

$HOME_anu_test/Anu_data/canonical_form_dictionary/canonical_form.out   < $tmp/$file_dir/temp_word_column  >  $tmp/$file_dir/tmp1_canonical_tmp
$HOME_anu_test/Anu_data/canonical_form_dictionary/canonical_form_correction.out  < $tmp/$file_dir/tmp1_canonical_tmp  > $tmp/$file_dir/tmp1_canonical_tmp1
$HOME_anu_test/Anu_data/canonical_form_dictionary/canonical_to_conventional.out  < $tmp/$file_dir/tmp1_canonical_tmp1  > $tmp/$file_dir/temp_word_canonical_column


paste $tmp/$file_dir/temp_id_column $tmp/$file_dir/temp_word_canonical_column  $tmp/$file_dir/temp_remaining_column >  $tmp/$file_dir/tmp1_canonical_tmp2

sed 's/;~~~~~~~~~~\t;~~~~~~~~~~\t;~~~~~~~~~~/;~~~~~~~~~~/g' $tmp/$file_dir/tmp1_canonical_tmp2 > $tmp/$file_dir/hindi_parser_out_canonical.txt

rm $tmp/$file_dir/tmp1_canonical_tmp $tmp/$file_dir/tmp1_canonical_tmp1 $tmp/$file_dir/tmp1_canonical_tmp2 

cd $tmp/$file_dir

$HOME_anu_test/Anu_src/split_file.out hindi_parser_out_canonical.txt dir_names.txt hindi_parser_canonial.dat

cd $HOME_alignment

##################################
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
 sh $HOME_alignment/run_new_stanford-parser.sh $tmp_path/E_sentence $tmp_path 
        #Generating English parser facts from E_conll_parse and E_sentence
	

	#++++++++++++++++++++++++++++++++++++++++  Clips to generate constituency parse +++++++++++++++++++++++++++++++++++++++++++++++
        #echo "(defglobal ?*hpath* = $HOME_alignment)" > $tmp_path/new_alignment.clp

        #touch $tmp_path/clips_error_kishori
        #myclips -f  $HOME_alignment/tmp_run_Qth.bat  >  $tmp_path/clips_error_kishori
        #myclips -f  $HOME_alignment/final_Pth.bat  >>  $tmp_path/clips_error_kishori

done



