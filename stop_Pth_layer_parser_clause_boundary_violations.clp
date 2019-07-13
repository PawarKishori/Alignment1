(deftemplate  database_info (slot root (default 0))(slot meaning (default 0))(multislot components (default 0))(slot database_name (default 0))( slot database_type (default 0))(multislot group_ids (default 0)))


(deftemplate Edict-Hdict (multislot E_id (default 0)) (multislot E_word (default 0)) (multislot H_id (default 0)) (multislot H_word (default 0) ))

(deftemplate E_group (slot language (default 0)) (slot grp_hid (default 0)) ( slot grp_head_word (default 0)) (multislot grp_element_ids (default 0))(multislot grp_element_words (default 0)))

(deftemplate H_group (slot language (default 0)) (slot grp_hid (default 0)) (slot grp_head_word (default 0)) (multislot grp_element_ids (default 0))(multislot grp_element_words (default 0)))

(deftemplate alignment_info (slot anu_id (default 0)) (multislot anu_meaning (default 0)) (slot man_id (default 0)) (multislot  man_meaning (default 0)) ( multislot man_group_ids (default 0)))
(deftemplate Allfacts (slot A)(slot K)(multislot L)(multislot M)(multislot N)(multislot O)(multislot P)(multislot P1)(multislot DICT))


(defrule stop_wrong_clause_grouping
	?f0 <- (alignment_info (anu_id ?x) (man_id ?hid) (man_group_ids $?man_grp_ids) )
	?f1 <- (alignment_info (anu_id ?x1) (man_id ?hid1) (man_group_ids $?man_grp_ids1) )
	(chunk_type-name-headid-ids NP ?  ?  $?  ?x ?x1 $?)
	;(chunk_type-name-headid-ids ?ct&~S&~ROOT ?  ?  $?  ?x ?x1 $?)
	(H_group (language hindi) (grp_element_ids  $? ?hid ?del $?) (grp_hid ?hin_grp_id))
	(test (neq ?hid1 ?del))
;	(test (neq ?hin_grp_id 0))
	=>
	(retract ?f0 ?f1)
)
