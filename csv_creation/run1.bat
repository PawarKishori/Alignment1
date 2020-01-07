(load "alignment_path.clp")
(bind ?*path* (str-cat ?*path* "/csv_creation/heuristics1.clp"))
(load ?*path*)
;(load-facts "H_wordid-word_mapping.dat")
(load-facts "manual_id_mapped.dat")
(load-facts "cat_consistency_check.dat")
(load-facts "word.dat")
(load-facts "relations.dat")
(watch rules)
(watch facts)
(agenda)
(run)
(save-facts "new_p_layer_tmp.dat" local P1_tmp eng_id_decided hid_id_decided)
(clear)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(load "alignment_path.clp")
(bind ?*path* (str-cat ?*path* "/csv_creation/group_kriyA_mUla1.clp"))
(load ?*path*)
(load-facts "hindi_meanings_with_grp_ids.dat")
(load-facts "cat_consistency_check.dat")
(load-facts "revised_root.dat")
(load-facts "E_grouping.dat")
(load-facts "H_grouping.dat")
;(load-facts "H_wordid-word_mapping.dat")
(load-facts "manual_id_mapped.dat")
(load-facts "kriyA_mUla_info.dat")
(load-facts "new_p_layer_tmp.dat")
(watch rules)
(watch facts)
(agenda)
(run)
(save-facts "E_grouping1.dat" local Eng_label-group_elements)
(save-facts "H_grouping1.dat" local Hnd_label-group_elements)
(save-facts "new_p_layer_tmp1.dat" local P1_tmp eng_id_decided hid_id_decided)
(clear)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(load "alignment_path.clp")
(bind ?*path* (str-cat ?*path* "/csv_creation/get_anchor.clp"))
(load ?*path*)
(load-facts "new_p_layer_tmp1.dat")
(load-facts "anchor.dat")
(load-facts "E_grouping1.dat")
(load-facts "H_grouping1.dat")
(watch rules)
(watch facts)
(agenda)
(run)
(save-facts "anchor1.dat" local iter-type-eng_g_id-h_g_id hindi_head_id-grp_ids iter-h_g_id)
(clear)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(load "alignment_path.clp")
(bind ?*path* (str-cat ?*path* "/csv_creation/align_using_dic.clp"))
(load ?*path*)
(load-facts "anchor1.dat")
(load-facts "database_mng.dat")
;(load-facts "H_wordid-word_mapping.dat")
(load-facts "manual_id_mapped.dat")
(load-facts "revised_root.dat")
(watch rules)
(watch facts)
(agenda)
(run)
(save-facts "anchor2.dat" local iter-type-eng_g_id-h_g_id hindi_head_id-grp_ids iter-h_g_id)
(clear)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(load "alignment_path.clp")
(bind ?*path* (str-cat ?*path* "/csv_creation/generate_new_layer.clp"))
(load ?*path*)
(load-facts "anchor2.dat")
(assert (label P2))
(watch rules)
(watch facts)
(agenda)
(run)
(save-facts "new_layer_p2.dat" local dummy )
(clear)
(exit)

