(load "new_alignment.clp")
(bind ?*hpath* (str-cat ?*hpath* "/bc.clp"))
(load ?*hpath*)
(load-facts "deffact_anchors.dat")
(load-facts "E_clip_deffact.dat")
(load-facts "H_clip_deffact.dat")
(run)
(facts)
(save-facts "save_facts1" local final_english_id-final_hindi_id)
(save-facts "save_facts2" local final_Egroup_ids-final_Hgroup_ids)
(save-facts "save_facts_unknown" local anchor_type-english_id-hindi_id)
(exit)