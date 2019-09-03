tmp_path=$HOME_anu_tmp/tmp/$1_tmp
cd  $tmp_path/
ls $tmp_path/org_hindi
$HOME_anu_test/Anu_data/canonical_form_dictionary/canonical_form.out   < org_hindi  >  tmp1_canonical_tmp
$HOME_anu_test/Anu_data/canonical_form_dictionary/canonical_form_correction.out  < tmp1_canonical_tmp  > tmp1_canonical_tmp1
$HOME_anu_test/Anu_data/canonical_form_dictionary/canonical_to_conventional.out  < tmp1_canonical_tmp1  >  hindi_canonical
ls $tmp_path/hindi_canonical
rm tmp1_canonical_tmp1 tmp1_canonical_tmp

