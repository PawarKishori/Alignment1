#sh run_all.sh Geo_chap2_E1_detok Geo_chap2_H1_detok_charu_wx



#sh create_corpus_specific_gdbm.sh ilci_E2H_single_nandani.txt ilci_H2E_single ilci_E2H_multi_nandani.txt ilci_H2E_multi
#sh create_corpus_specific_gdbm.sh corpus_single_E2H_dict corpus_single_H2E corpus_multi_E2H_dict corpus_multi_H2E
sh preprocess.sh $1 $2	/home/kishori/a/alignment_manju
echo "preprocessing done"
sh Rth.sh $1 #/home/user/WORK/Alignment/ > tam_lwg_errors.txt
