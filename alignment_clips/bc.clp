;Rule to check starting anchor and directly asserting it as final ID.
(defrule check_anchor
	?e <- (anchor_type-english_id-hindi_id anchor ?a $?y)
	?E <- (Egroup_id-group_elements ? $?n)
	?H <- (Hgroup_id-group_elements ? $?p)
	(test (and (member$ ?a $?n) (member$ $?y $?p)))
	=>
	(retract ?e)
	(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
	(assert (final_english_id-final_hindi_id anchor ?a $?y)))



;Rule to check if the first value of potential ID suggestion is correct.
(defrule check_potential
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?y2)
	?f <- (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p)
	(test (and (member$ ?a $?n) (member$ $?y1 $?p) (neq ?e1 ?e2) (not (member$ $?y2 $?y1))))
	=>
	(assert (final_english_id-final_hindi_id anchor ?a $?y1))
	(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
	(assert (remove ?a $?y1))
	(retract ?e1)
	(retract ?e2))



;Rule to check if the other value of potetial ID suggestion is correct.
(defrule check_potential_helper
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?y2)
	?f <- (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p)
	(test (and (member$ ?a $?n) (member$ $?y2 $?p) (neq ?e1 ?e2) (not (member$ $?y2 $?y1))))
	=>
	(assert (final_english_id-final_hindi_id anchor ?a $?y2))
	(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
	(assert (remove ?a $?y2))
	(retract ?e1)
	(retract ?e2))



;Rule to remove ambiguous anchors after conversion of a potential ID ---> anchor ID.
(defrule remove_ambiguity
	?r <- (remove ?x $?y1)
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



;Rule to check the cases of intersecting potential and if found pick up the largest group amongst the intersecting suggestions.
(defrule check_intersecting_potential
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?y2)
	(test (and (neq ?e1 ?e2) (or (member$ $?y2 $?y1) (member$ $?y1 $?y2))))
	=>
	(if (> (length $?y1) (length $?y2))
		then
		(retract ?e2)
		else
		(retract ?e1)))


;Rule to convert potential to anchor when only unique ID exists in the potential field.
(defrule check_unique_potential_ID
	(declare (salience -100))
	?p1 <- (anchor_type-english_id-hindi_id potential ?a $?b)
	?p2 <- (anchor_type-english_id-hindi_id potential ?a $?b)
	?E <- (Egroup_id-group_elements ? $?n)
	?H <- (Hgroup_id-group_elements ? $?p)
	(test (and (member$ ?a $?n) (member$ $?b $?p) (eq ?p2 ?p1)))
	=>
	(assert (final_Egroup_ids-final_Hgroup_ids $?n <=> $?p))
	(assert (final_english_id-final_hindi_id anchor ?a $?b))
	(retract ?p1))


;Rule to check if for an English group is being matched to multiple Hindi groups, if such a case is found, Hindi groups are merged.
(defrule check_hindi_group_merge
	?g1 <- (final_Egroup_ids-final_Hgroup_ids $?a <=> $?b)
	?g2 <- (final_Egroup_ids-final_Hgroup_ids $?a <=> $?c)
	(test (neq ?g1 ?g2))
	=>
	(retract ?g1)
	(retract ?g2)
	(assert (final_Egroup_ids-final_Hgroup_ids $?a <=> $?b $?c)))



;Rule to check if for a Hindi group is being matched to multiple English groups, if such a case is found, English groups are merged.
(defrule check_english_group_merge
	?g1 <- (final_Egroup_ids-final_Hgroup_ids $?a <=> $?b)
	?g2 <- (final_Egroup_ids-final_Hgroup_ids $?c <=> $?b)
	(test (neq ?g1 ?g2))
	=>
	(retract ?g1)
	(retract ?g2)
	(assert (final_Egroup_ids-final_Hgroup_ids $?a $?c <=> $?b)))