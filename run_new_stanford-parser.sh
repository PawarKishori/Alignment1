# called in Qth.sh => sh $HOME_alignment/run_new_stanford-parser.sh $tmp_path/E_sentence $tmp_path
# This will generate in tmp folder =>E_constituency_parse,  E_constituency_one_line_parse, E_typed_dependency_parse, E_conll_parse
cd $HOME_anu_test/Parsers/stanford-parser/stanford-parser-full-2018-10-17
#java -mx150m -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat "penn,typedDependencies" -outputFormatOptions "basicDependencies, collapsedDependencies, CCPropagatedDependencies, nonCollapsedDependencies, nonCollapsedDependenciesSeparated" edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $1 
#java -mx1g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences "newline" -outputFormat oneline -outputFormatOptions "treeDependencies" -tagSeparator / -tokenizerOptions "americanize=false, escapeForwardSlashAsterisk=false"  edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz fox.txt 
#touch $2/E_constituency_parse
java -mx1g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser  edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $1 > $2/E_constituency_parse
#touch $2/E_constituency_one_line_parse
java -mx1g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser  -outputFormat oneline   edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $1  > $2/E_constituency_one_line_parse
#touch $2/E_typed_dependency_parse
java -mx1g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser  -outputFormat "typedDependencies"  edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz $1  > $2/E_typed_dependency_parse
#java -mx1g  -cp "*" edu.stanford.nlp.trees.EnglishGrammaticalStructure  -treeFile $2/E_constituency_parse  -conllx > $2/E_conll_parse
#touch $2/E_conll_parse
java -mx1g  -cp "*" edu.stanford.nlp.trees.ud.UniversalDependenciesConverter  -treeFile $2/E_constituency_parse  -conllx > $2/E_conll_parse
