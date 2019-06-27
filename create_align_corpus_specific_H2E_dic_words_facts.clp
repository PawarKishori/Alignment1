(deftemplate mwe_fact (multislot H_id (default 0))(multislot H_word (default 0))(multislot E_word (default 0))(slot mng_no (default 0))(slot mng_type(default 0)))
(deftemplate Edict-Hdict (multislot E_id (default 0))(multislot E_word (default 0))(multislot H_id (default 0))(multislot H_word (default 0)))
(deftemplate clause (slot cl_id (default 0)) (multislot cl_words (default 0)) (multislot cl_member_ids (default 0)) (slot finite_verb_grp (default 0)) (multislot finite_verb_grp_ids (default 0)) (slot finite_verb_root (default 0)) (slot finite_verb_root_id (default 0)) (slot finite_verb_tam (default 0)))
(deftemplate eng_clause (slot cl_id (default 0)) (multislot cl_words (default 0)) (multislot cl_member_ids (default 0)))
(deftemplate EClause-HClause (multislot EClauseIds (default 0)) (multislot EClauseMemberIds (default 0)) (multislot EClauseMemberWords (default 0)) (multislot HClauseIds (default 0)) (multislot HClauseMemberIds (default 0)) (multislot HClauseMemberWords (default 0)))
;Function to replace "-" and "_" with " " in a word
;Axi_guru        adi_guru
;Axi_maXya_aMwa  adi-madhya-anta
(deffunction remove_character(?char ?str ?replace_char)
                        (bind ?new_str "")
                        (bind ?index (str-index ?char ?str))
                        (if (neq ?index FALSE) then
                        (while (neq ?index FALSE)
                        (bind ?new_str (str-cat ?new_str (sub-string 1  (- ?index 1) ?str) ?replace_char))
                        (bind ?str (sub-string (+ ?index 1) (length ?str) ?str))
                        (bind ?index (str-index ?char ?str))
                        )
                        )
                (bind ?new_str (explode$ (str-cat ?new_str (sub-string 1 (length ?str) ?str))))
)


;Function to pick the meanings of the word present in the dictionary(gdbm) one by one and create facts for them
;ASraya  aashraya/ashraya/refuge
(deffunction pick_meanings_one_by_one_from_gdbm_and_create_facts(?word ?new_mng ?dic_type $?mid)
        (bind ?count 0)
        (bind ?word (string-to-field ?word))
        (if (eq (numberp ?word) FALSE) then
                (bind ?word (remove_character "_" ?word " "))
        )
        (bind ?new_mng1 (create$))
        (bind ?slh_index (str-index "/" ?new_mng))
        (if (and (neq (length ?new_mng) 0)(neq ?slh_index FALSE)) then
                (while (neq ?slh_index FALSE)
                        (bind ?count (+ ?count 1))
                        (bind ?new_mng1 (sub-string 1 (- ?slh_index 1) ?new_mng))
                        (bind ?org_mng (string-to-field (sub-string 1 (- ?slh_index 1) ?new_mng)))
                        (bind ?new_mng1 (remove_character "_" ?new_mng1 " "))
                        (bind ?new_mng1 (remove_character "-" (implode$ (create$  ?new_mng1)) " "))
			(if (eq ?dic_type multi) then
			 	(assert (mwe_fact (H_id $?mid)(H_word ?word)(E_word ?new_mng1)(mng_no ?count)(mng_type ?dic_type)))
			 else
				(assert (H_id-H_word-E_word-mng_no-mng_type $?mid ?word ?new_mng1 ?count ?dic_type))
			)
			;(assert (database_info (meaning ?org_mng)(components ?new_mng1)(group_ids $?word_ids)))
                        (bind ?new_mng (sub-string (+ ?slh_index 1) (length ?new_mng) ?new_mng))
                        (bind ?slh_index (str-index "/" ?new_mng))
                )
        )
	(bind ?new_mng1 (str-cat (sub-string 1 (length ?new_mng) ?new_mng)))
        (bind ?org_mng (string-to-field (str-cat (sub-string 1 (length ?new_mng) ?new_mng))))
        (bind ?new_mng1 (remove_character "_" ?new_mng1 " "))
        (bind ?new_mng1 (remove_character "-" (implode$ (create$ ?new_mng1)) " "))
        (if (neq ?new_mng "") then
                (bind ?count (+ ?count 1))
		(if (eq ?dic_type multi) then
		(assert (mwe_fact (H_id $?mid)(H_word ?word)(E_word ?new_mng1)(mng_no ?count)(mng_type ?dic_type)))
		else
			(assert (H_id-H_word-E_word-mng_no-mng_type $?mid ?word ?new_mng1 ?count ?dic_type))
		)
        	;(assert (database_info (meaning ?org_mng)(components ?new_mng1)(group_ids $?word_ids)))
        )
)

(deffunction create_H2E_facts_after_gdbm_lookup(?gdbm ?hword ?dic_type $?mid)
        (bind ?list_of_mngs (gdbm_lookup ?gdbm ?hword))
	(if (neq ?list_of_mngs "FALSE") then
        	(pick_meanings_one_by_one_from_gdbm_and_create_facts ?hword ?list_of_mngs ?dic_type $?mid))
)

(defrule H2E_gdbm_lookup_single_word
        (H_wid-word $?mid ?hword)
	=>
	;(create_H2E_facts_after_gdbm_lookup "gita_ratnakar_dic.gdbm" ?hword ?mid))	
	;(create_H2E_facts_after_gdbm_lookup "ilci_H2E_single_dic.gdbm" ?hword single $?mid))
	;(create_H2E_facts_after_gdbm_lookup "Geo_single_H2E_dic.gdbm" ?hword single $?mid))
	(create_H2E_facts_after_gdbm_lookup "Geo_single_merge_dict_H2E_dic.gdbm" ?hword single $?mid))


(defrule H2E_gdbm_lookup_multi_word
        (manual_id-mwe $?mid ?hword)
        =>
        ;(create_H2E_facts_after_gdbm_lookup "ilci_H2E_multi_dic.gdbm" ?hword multi $?mid))	
        ;(create_H2E_facts_after_gdbm_lookup "Geo_multi_H2E_dic.gdbm" ?hword multi $?mid))	
        (create_H2E_facts_after_gdbm_lookup "Geo_multi_merge_dict_H2E_dic.gdbm" ?hword multi $?mid))	
     

(defrule retract_single_word_facts_for_which_mwe_fact_already_exists
	(mwe_fact (H_id $?pre ?hid $?post))
	?f1<-(H_id-H_word-E_word-mng_no-mng_type ?hid ? ? ? single)
	=>
	(retract ?f1)
)

;(mwe_fact (H_id 3) (H_word pORtika AhAra) (E_word nutritious diet) (mng_no 1) (mng_type multi))
;Disambiguate for same mwe in a single sentence.
(defrule assert_corpus_specific_H2E_dict_multi_facts
        (mwe_fact (H_id $?mids)(H_word $?mwords)(E_word $?pr ?x $?pst))
        (id-original_word ?id ?x)
        (id-original_word =(+ ?id 1) $?pst)
	;(EClause-HClause (EClauseMemberIds $?pre1 ?id $?post1) (HClauseMemberIds $?pre2 $?mids $?post2))
	(not (Edict-Hdict (H_id $?mids)))
       =>
        (if (= (length$ $?pr) 2) then
                (assert (Edict-Hdict (E_id (- ?id 2) (- ?id 1) ?id (+ 1 ?id)) (E_word $?pr ?x $?pst)(H_id $?mids)(H_word $?mwords)))
        else
                (if (= (length$ $?pr) 1) then
                        (assert (Edict-Hdict (E_id (- ?id 1) ?id (+ 1 ?id)) (E_word $?pr ?x $?pst)(H_id $?mids)(H_word $?mwords)))
                else
                        (assert (Edict-Hdict (E_id ?id (+ 1 ?id)) (E_word $?pr ?x $?pst) (H_id $?mids)(H_word $?mwords))))
        )
)


(defrule add_vibhakti_to_corpus_specific_H2E_dict_multi_fact
	?f1<-(Edict-Hdict (E_id $?eids)(E_word $?ewords)(H_id $?preid ?mid)(H_word $?preword ?mword))
	(H_def_lwg-wid-word-postpositions ?mword_with_vib ?mid ?mword ?)
	=>
	(retract ?f1)
	(assert (Edict-Hdict (E_id $?eids)(E_word $?ewords)(H_id $?preid ?mid)(H_word $?preword ?mword_with_vib)))
)

; (clause (cl_id 1) (cl_words wo jAzca karavAnA Ora BI AvaSyaka hE.) (cl_member_ids 12 13 14 15 16 17 18) (finite_verb_grp AvaSyaka_hE) (finite_verb_grp_ids 17 18) (finite_verb_root AvaSyaka_hE) (finite_verb_root_id 17) (finite_verb_tam hE))
(defrule assert_corpus_specific_H2E_dict_single_facts
	(id-original_word ?eid ?eword)
	(H_id-H_word-E_word-mng_no-mng_type ?hid ?hword ?eword ? single)
	;(clause (cl_words $?pre1 ?hword $?post1) (cl_member_ids $?pre2 ?hid $?post2))
	;(eng_clause (cl_words $?pre3 ?eword $?post3) (cl_member_ids $?pre4 ?eid $?post4))
	;(EClause-HClause (EClauseMemberIds $?pre1 ?eid $?post1) (HClauseMemberIds $?pre2 ?hid $?post2))
	(not (Edict-Hdict (E_id ?) (E_word ?) (H_id ?hid) (H_word ?hword)))
	(not (Edict-Hdict (E_id ?eid) (E_word ?eword) (H_id ?) (H_word ?)))
	=>
	(assert (Edict-Hdict (E_id ?eid) (E_word ?eword) (H_id ?hid) (H_word ?hword)))
)

;(defrule assert_corpus_specific_H2E_dict_single_facts_without_clause_boundary_check
;	(declare (salience -1))
;	(id-original_word ?eid ?eword)
;	(H_id-H_word-E_word-mng_no-mng_type ?hid ?hword ?eword ? single)
;	(not(EClause-HClause (EClauseMemberIds $?pre1 ?eid $?post1) (HClauseMemberIds $?pre2 ?hid $?post2)))
;	(not (Edict-Hdict (E_id ?) (E_word ?) (H_id ?hid) (H_word ?hword)))
;	(not (Edict-Hdict (E_id ?eid) (E_word ?eword) (H_id ?) (H_word ?)))
;	=>
;	(assert (Edict-Hdict (E_id ?eid) (E_word ?eword) (H_id ?hid) (H_word ?hword)))
;)
