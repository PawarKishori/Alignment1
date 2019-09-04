#Prepocessing for canonical form
sh create_canonical.sh $2
echo "$2_canonical created"
sh create_canonical.sh $3
echo "$2_canonical created"
#Calling the code for Technical_Dictionary_Integration
python $HOME_alignment/tech_dict/Technical_Dictionary_Integration.py $1 $2_canonical $3_canonical
echo "Created Dictionary"

