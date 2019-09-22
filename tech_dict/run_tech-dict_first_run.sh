## RUN:
# Eg. sh tech_dict/run_tech-dict_first_run.sh <eng_entire_corpus> <hindi_entire_corpus> <original_bharatwani_dict_in_proper_format> <final_lookup_dictionry_list> 


#Prepocessing for canonical form
sh tech_dict/create_canonical.sh $2
echo "$2_canonical created"
sh tech_dict/create_canonical.sh $3
echo "$3_canonical created"
#Calling the code for Technical_Dictionary_Integration
#python $HOME_alignment/tech_dict/Technical_Dictionary_Integration.py $1 $2_canonical $3_canonical $4
python $HOME_alignment/tech_dict/Technical_Dictionary_Integration_first_run.py $1 $2_canonical $3_canonical $4
echo "Created Dictionary"

