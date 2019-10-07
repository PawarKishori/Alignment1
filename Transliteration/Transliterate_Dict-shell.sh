tmp_path=$HOME_anu_tmp/tmp/$1
read -p "Enter English Corpus name : " e
read -p "Enter Hindi Corpus name : " h
echo $tmp_path
python3 $HOME_alignment/Transliteration/Transliterate_Dict.py "${tmp_path}/${e}" "${tmp_path}/${h}"   
