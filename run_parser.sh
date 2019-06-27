# $1 => GeoE01
python3 Halignment_parser_tree_in_one_line-for-all-sentences.py $1 > $1H_grouping_error
python3 Ealignment_parser_tree_in_one_line-for-all-sentences.py $1 > $1E_grouping_error
