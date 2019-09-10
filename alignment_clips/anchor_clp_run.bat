(load "new_alignment.clp")
(bind ?*hpath* (str-cat ?*hpath* "/alignment_clips/check.clp"))
(load ?*hpath*)
(load-facts "E_clip_deffact.dat")
(load-facts "H_clip_deffact.dat")
(load-facts "deffact_anchors.dat")
(load ?*hpath*)
(run)
(facts)
;(save-facts "save_facts1" local final_english_id-final_hindi_id)                             ;final_set-eid-hid
;(save-facts "save_facts2" local final_Egroup_ids-final_Hgroup_ids)                           ;proposed_groups
(save-facts "save_facts1" local final_set-eid-hid)
(save-facts "save_facts2" local proposed_groups)
(save-facts "save_facts_unknown" local anchor_type-english_id-hindi_id)
(exit)

