(defrule check_anchor
	(declare (salience 500))
	?e <- (anchor_type-english_id-hindi_id anchor ?a $?y)
	?E <- (Egroup_id-group_elements ? $?n)
	?H <- (Hgroup_id-group_elements ? $?p)
	(test (and (member$ ?a $?n) (member$ $?y $?p)))
	=>
	(retract ?e)
	(printout t "Rule check_anchor fired for " ?a " " $?y crlf)
	(assert (final_english_id-final_hindi_id anchor ?a $?y))
	(assert (final_Egroup_ids-final_Hgroup_ids $?n MFS $?p)))


(defrule check_intersecting_potential
	(declare (salience 300))
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?y2)
	(test (and (neq ?e1 ?e2) (or (member$ $?y2 $?y1) (member$ $?y1 $?y2))))
	=>
	(if (> (length $?y1) (length $?y2))
		then
		(retract ?e2)
		(printout t "Rule check_intersecting_potential fired for " ?a " " $?y2 crlf)
		else
		(retract ?e1)
		(printout t "Rule check_intersecting_potential fired for " ?a " " $?y1 crlf)))
