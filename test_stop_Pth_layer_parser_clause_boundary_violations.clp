(deftemplate  database_info (slot root (default 0))(slot meaning (default 0))(multislot components (default 0))(slot database_name (default 0))( slot database_type (default 0))(multislot group_ids (default 0)))


(deftemplate Edict-Hdict (multislot E_id (default 0)) (multislot E_word (default 0)) (multislot H_id (default 0)) (multislot H_word (default 0) ))

(deftemplate E_group (slot language (default 0)) (slot grp_hid (default 0)) ( slot grp_head_word (default 0)) (multislot grp_element_ids (default 0))(multislot grp_element_words (default 0)))

(deftemplate H_group (slot language (default 0)) (slot grp_hid (default 0)) (slot grp_head_word (default 0)) (multislot grp_element_ids (default 0))(multislot grp_element_words (default 0)))

(deftemplate alignment_info (slot anu_id (default 0)) (multislot anu_meaning (default 0)) (slot man_id (default 0)) (multislot  man_meaning (default 0)) ( multislot man_group_ids (default 0)))

(defrule suspicious_mark "This rule will assert a fact if Eng or hindi word is repeated in the sentence"
	(E_wordid-word ?wid1 ?org_word1)
	(id-root-category-suffix-number ?wid1 ?root1 ? ? ?)
	(E_wordid-word ?wid2 ?org_word2)
	(id-root-category-suffix-number ?wid2 ?root2 ? ? ?)
	(test (eq ?root1 ?root2))
	=> 
	(assert (word_repeated_in_lang-wid-word_root english ?wid1 ?root1))
	(assert (word_repeated_in_lang-wid-word_root english ?wid2 ?root2))

)


(defrule stop_wrong_clause_grouping "This rule is marking suspicious words in Pth layer"
	(word_repeated_in_lang-wid-word_root ?lang ?x ?repeated_root)
	(word_repeated_in_lang-wid-word_root ?lang ?x1 ?repeated_root)

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
