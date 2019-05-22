#sh preprocess.sh cl_english_100_detok cl_hindi_100_detok /home/user/forked/alignment_manju
#$1=name of the english_file/tmp_folder;	Eg:cl_english_100_detok
#$2=hindi corpus file's name in which you want to join multiwords with an underscore;	Eg:cl_hindi_100_detok
#$HOME'/forked/alignment_manju/' is the path of alignment_manju_folder in your system
corpus_path=$3
#python replace_multiwords_in_corpus.py cl_hindi_100_detok /home/user/forked/alignment_manju > cl_hindi_100_detok.out
python replace_multiwords_in_corpus.py $2 $3 > $2.out
#python write_a_file_in_multiple_dirs.py cl_english_100_detok cl_hindi_100_detok_multiwords_underscored Hindi_sent_mwes_underscored.dat /home/user/forked/alignment_manju
python write_a_file_in_multiple_dirs.py $1 $(cat $2.out) Hindi_sent_mwes_underscored.dat $3
