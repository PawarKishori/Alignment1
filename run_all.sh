#sh run_all.sh cl_english_100_detok cl_hindi_100_detok
#sh create_corpus_specific_gdbm.sh ilci_E2H_single_nandani.txt ilci_H2E_single ilci_E2H_multi_nandani.txt ilci_H2E_multi
sh preprocess.sh $1 $2	/home/kishori/a/alignment_manju
echo "preprocessing done"
sh Rth.sh $1 #/home/user/WORK/Alignment/ > tam_lwg_errors.txt
