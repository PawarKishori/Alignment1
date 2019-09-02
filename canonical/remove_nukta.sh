tmp_path=$HOME_anu_tmp/tmp/$1_tmp
cd  $tmp_path/
touch $HOME_anu_tmp/tmp/$1_tmp/org_hindi_without_nukta
$HOME_alignment/canonical/replace_nukta.out < org_hindi > org_hindi_without_nukta
