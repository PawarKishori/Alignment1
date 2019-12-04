(load "alignment_path.clp")
(bind ?*path* (str-cat ?*path* "/csv_creation/correct_grouping.clp"))
(load ?*path*)
(load-facts "E_grouping.dat")
(load-facts "H_grouping.dat")
(load-facts "all_layer_facts.dat")
(load-facts "hindi_meanings_with_grp_ids.dat")
(load-facts "word.dat")
(load-facts "H_wordid-word_mapping.dat")
(watch rules)
(watch facts)
(agenda)
(run)
(clear)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(load "alignment_path.clp")
(bind ?*path* (str-cat ?*path* "/csv_creation/correct_hindi_grouping.clp"))
(load ?*path*)
(load-facts "wrong_grouping_id.dat")
(load-facts "E_grouping.dat")
(load-facts "H_grouping.dat")
(load-facts "all_layer_facts.dat")
(load-facts "word.dat")
(load-facts "H_wordid-word_mapping.dat")
(load-facts "eng_wrd_occurence.dat")
(load-facts "hnd_wrd_occurence.dat")
(load-facts "get_all_layer_group_info.dat")
(watch rules)
(watch facts)
(agenda)
(run)
(save-facts "new_p_layer.dat" local P1)
(exit)


