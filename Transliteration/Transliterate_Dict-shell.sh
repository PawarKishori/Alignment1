python3 $HOME_alignment/Transliteration/Acronym_Dict.py $1 $2
echo "____________"
python3 $HOME_alignment/Transliteration/Transliterate_Dict.py $1 $2  

echo "____________"
python3 $HOME_alignment/Transliteration/Remove_entries_handled_by_acronym_from_Transliterate.py
