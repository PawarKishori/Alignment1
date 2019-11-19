sh $HOME_alignment/csv_creation/create_html_csv.sh $1

cd $HOME_anu_tmp/tmp/$1_tmp
while read line 
do
   cd $line
        bash $HOME_alignment/csv_creation/run_K_layer_alignment.sh
   cd ..
done < dir_names.txt
