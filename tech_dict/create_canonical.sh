cd  $HOME_alignment/tech_dict
$HOME_anu_test/Anu_data/canonical_form_dictionary/canonical_form.out   < $1  >  tmp1_canonical_tmp
$HOME_anu_test/Anu_data/canonical_form_dictionary/canonical_form_correction.out  < tmp1_canonical_tmp  > tmp1_canonical_tmp1
$HOME_anu_test/Anu_data/canonical_form_dictionary/canonical_to_conventional.out  < tmp1_canonical_tmp1  >  $1_canonical
rm tmp1_canonical_tmp1 tmp1_canonical_tmp

