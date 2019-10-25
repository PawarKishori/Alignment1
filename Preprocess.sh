##Bringing out eng-hindi dictionary entries once from Bharatwani for a Domain's parallel corpora (eg. ALL PARALLEL AI CHAPTERS).
#sh $HOME_alignment/tech_dict/run_tech-dict_first_run.sh AI_all_eng AI_all_hin dictionary/Final_Computer_Science_Glossary_English-Hindi dictionary/Lookup_dict_ai
sh $HOME_alignment/tech_dict/run_tech-dict_first_run.sh $1 $2 dictionary/Final_Computer_Science_Glossary_English-Hindi dictionary/Lookup_dict_ai

## following command not working.. check why? Need to debug $HOME_alignment/tech_dict/Technical_Dictionary_Integration_first_run.py
##sh $HOME_alignment/tech_dict/run_tech-dict_first_run.sh GeoE GeoH dictionary/technical_geography_dictionary dictionary/Lookup_dict_geography


###############################################################################################################
##Bringing out eng-hindi transliterated words once from a given parallel corpora (eg. ALL PARALLEL AI CHAPTERS).

sh $HOME_alignment/Transliteration/Transliterate_Dict-shell.sh $1 $2 

###############################################################################################################
