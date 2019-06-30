(deftemplate alignment (slot anu_id (default 0))(slot man_id (default 0))(multislot anu_meaning (default 0))(multislot man_meaning(default 0)))

(deftemplate manual_word_info (slot head_id (default 0))(multislot word (default 0))(multislot word_components (default 0))(multislot root (default 0))(multislot root_components (default 0))(multislot vibakthi (default 0))(multislot vibakthi_components (default 0))(slot tam (default 0))(multislot tam_components (default 0))(multislot group_ids (default 0)))

(deftemplate alignment_info (slot anu_id (default 0)) (multislot anu_meaning (default 0)) (slot man_id (default 0)) (multislot  man_meaning (default 0)) ( multislot man_group_ids (default 0)))

(defrule generate_minimal_facts
	(alignment (anu_id ?x) (man_id ?hid) (anu_meaning $?anu_words) (man_meaning $?man_word))
	(manual_word_info (head_id ?hid) (group_ids $?man_grp_ids))
	=>
	(assert	(alignment_info (anu_id ?x) (man_id ?hid) (anu_meaning $?anu_words) (man_meaning $?man_word) (man_group_ids $?man_grp_ids)))
)

