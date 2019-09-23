#Prepocessing for canonical form
sh tech_dict/create_canonical.sh $2
echo "$2_canonical created"
sh tech_dict/create_canonical.sh $3
echo "$3_canonical created"
#Calling the code for Technical_Dictionary_Integration
python $HOME_alignment/tech_dict/Technical_Dictionary_Integration.py $1 $2_canonical $3_canonical
echo "Created Dictionary"

