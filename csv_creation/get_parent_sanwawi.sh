rm -f parent_sanwawi.dat
count=`wc -l original_word.dat| awk '{print $1}'`
for ((i = 1 ; i <= $count ; i++)); do
	python3 $HOME_alignment/csv_creation/print_ancester.py E_conll_parse_enhanced_without_punc.tsv $i $1  >> parent_sanwawi.dat 
	python3 $HOME_alignment/csv_creation/print_ancester.py hindi_dep_parser_original_without_punc.tsv $i $2 >> parent_sanwawi.dat
done;

