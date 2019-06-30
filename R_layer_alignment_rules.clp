;Defining templates
;(deftemplate score (slot anu_id (default 0))(slot man_id (default 0))(slot weightage_sum (default 0))(multislot heuristics (default 0))(multislot rule_names (default 0)))

(deftemplate alignment (slot anu_id (default 0))(slot man_id (default 0))(multislot anu_meaning (default 0))(multislot man_meaning(default 0)))

;(deftemplate pada_info (slot group_head_id (default 0))(slot group_cat (default 0))(multislot group_ids (default 0))(slot vibakthi (default 0))(slot gender (default 0))(slot number (default 0))(slot case (default 0))(slot person (default 0))(slot H_tam (default 0))(slot tam_source (default 0))(slot preceeding_part_of_verb (default 0)) (multislot preposition (default 0))(slot Hin_position (default 0))(slot pada_head (default 0)))

;(deftemplate manual_word_info (slot head_id (default 0))(multislot word (default 0))(multislot word_components (default 0))(multislot root (default 0))(multislot root_components (default 0))(multislot vibakthi (default 0))(multislot vibakthi_components (default 0))(slot tam (default 0))(multislot tam_components (default 0))(multislot group_ids (default 0)))

(deftemplate  database_info (slot root (default 0))(slot meaning (default 0))(multislot components (default 0))(slot database_name (default 0))( slot database_type (default 0))(multislot group_ids (default 0)))

(deftemplate tam_database_info (multislot e_tam (default 0)) (slot database_name (default 0)) (multislot meaning (default 0))(multislot components (default 0)))
(deftemplate Eid-Eword-Hid-Hword (multislot E_id (default 0))(multislot E_word (default 0))(multislot H_id (default 0))(multislot H_word (default 0)))

(deftemplate words_aligned_using_clauses (multislot Eids (default 0)) (multislot Ewords (default 0)) (multislot Hids (default 0)) (multislot Hwords (default 0)) (multislot EHClauseId (default 0)))
;------------------------------------------------------------------

;------------------------------Rule for fixed consructs---------------------------
(defrule so_that_construct
(id-original_word ?eid so)
(id-original_word =(+ ?eid 1) that) 
(H_wid-word ?hid ?hword)     
(alignment (anu_id ?eid) (man_id ?hid) (anu_meaning $?) (man_meaning ?hword))
=>
(assert (Eid-Eword-Hid-Hword (E_id ?eid (+ ?eid 1)) (E_word so_that) (H_id ?hid) (H_word ?hword)))
)

;------------------------------Rules for R Layers-----------------------
;------------------------------Rules for dictionary alignment-----------------------
(defrule align_dic_matches
	(Edict-Hdict (E_id $?eid) (E_word $?eword) (H_id $?mid) (H_word $?mword))
	=>
	(assert (Eid-Eword-Hid-Hword (E_id $?eid) (E_word $?eword) (H_id $?mid) (H_word $?mword)))
)
;-----------------------------------------------------

