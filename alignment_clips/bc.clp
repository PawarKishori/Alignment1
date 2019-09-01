(defrule check_anchor
	?e <- (anchor_type-english_id-hindi_id anchor ?a $?y)
	?E <- (Egroup_id-group_elements ? $?n)
	?H <- (Hgroup_id-group_elements ? $?p)
	(test (and (member$ ?a $?n) (member$ $?y $?p)))
	=>
	(retract ?e)
	(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
	(assert (final_english_id-final_hindi_id anchor ?a $?y)))

(defrule check_potential
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?y2)
	?f <- (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p)
	(test (and (member$ ?a $?n) (member$ $?y1 $?p) (neq ?e1 ?e2) (not (member$ $?y2 $?y1))))
	=>
	(assert (final_english_id-final_hindi_id anchor ?a $?y1))
	(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
	(assert (rem ?a $?y1))
	(retract ?e1)
	(retract ?e2))

(defrule check_potential_helper
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?y2)
	?f <- (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p)
	(test (and (member$ ?a $?n) (member$ $?y2 $?p) (neq ?e1 ?e2) (not (member$ $?y2 $?y1))))
	=>
	(assert (final_english_id-final_hindi_id anchor ?a $?y2))
	(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
	(assert (rem ?a $?y2))
	(retract ?e1)
	(retract ?e2))

(defrule remove_ambiguity
	?r <- (rem ?x $?y1)
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?y2)
	?E <- (Egroup_id-group_elements ? $?n)
	?H <- (Hgroup_id-group_elements ? $?p)
	(test (and (member$ ?a $?n) (member$ $?y2 $?p) (neq ?e1 ?e2) (not (member$ $?y2 $?y1))))
	=>
	(retract ?e1)
	(retract ?r)
	(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
	(assert (final_english_id-final_hindi_id anchor ?a $?y2))
	(retract ?e2))

(defrule check_intersecting_potential
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?y2)
	?E <- (Egroup_id-group_elements ? $?n)
	?H <- (Hgroup_id-group_elements ? $?p)
	(test (and (member$ ?a $?n) (member$ $?y2 $?p) (neq ?e1 ?e2) (member$ $?y2 $?y1)))
	=>
	(if (> (length $?y1) (length $?y2))
		then
		(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
		(assert (final_english_id-final_hindi_id anchor ?a $?y1))
		else
		(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
		(assert (final_english_id-final_hindi_id anchor ?a $?y2)))
	(retract ?e1)
	(retract ?e2))