#source activate python2.7
python3 $HOME_alignment/Transliteration/Transliterate_Dict.py $1 $2  
#conda deactivate

python3 $HOME_alignment/Transliteration/Acronym_Dict.py $1 $2
