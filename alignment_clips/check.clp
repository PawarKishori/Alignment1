;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;; Rule to check anchors and directly move them as proposed anchors ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule check_anchor
	(declare (salience 500))
	?e <- (anchor_type-english_id-hindi_id anchor ?a $?y)
	;?E <- (english_group_ids_mfs $?n)
	?EG <- (Egroup_id-group_elements ?egid $?gpe)
	?HG <- (Hgroup_id-group_elements ?hgid $?gph)
	;?P <- (proposed_anchor_ids $?r)
	(test (and (member$ ?a $?gpe) (member$ $?y $?gph)))
	=>
	(retract ?e)
	(printout t "Rule check_anchor fired for " ?a " " $?y crlf)
	(assert (proposed_groups ?egid ?hgid))
	(assert (final_set-eid-hid ?a $?y)))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?a $?n) (member$ ?a $?n) $?y))))

;;;;;;;;;;;;;;;;;;;; Rule to check if one english anchor matches to IDs in multiple hindi groups ;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule check_anchor_multiple_hindi_group_match
	(declare (salience -500))
	?e <- (anchor_type-english_id-hindi_id anchor ?a $?y1 $?y2)
	;?E <- (english_group_ids_mfs $?n)
	?EG <- (Egroup_id-group_elements ?egid $?gpe)
	?HG1 <- (Hgroup_id-group_elements ?hgid1 $?gph1)
	?HG2 <- (Hgroup_id-group_elements ?hgid2 $?gph2)
	;?P <- (proposed_anchor_ids $?r)
	(test (and (member$ ?a $?gpe) (member$ $?y1 $?gph1) (member$ $?y2 $?gph2)))
	=>
	(retract ?e)
	(printout t "Rule check_anchor_multiple_hindi_group_match " ?a " " $?y1 " " $?y2 crlf)
	(assert (proposed_groups ?egid ?hgid1))
	(assert (proposed_groups ?egid ?hgid2))
	(assert (final_set-eid-hid ?a $?y1 $?y2)))
	;(assert (new_proposed_anchors_ids (replace$ $?r (member$ ?a $?n) (member$ ?a $?n) (create$ $?y1 $?y2)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;; Rule to check if some proposed anchors (groups) suggest matching of potential anchor ;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule check_potential
	?p1 <- (anchor_type-english_id-hindi_id potential ?x $?y)
	?g1 <- (proposed_groups ?p ?q)
	?g2 <- (Egroup_id-group_elements ?p $?pgroup)
	?g3 <- (Hgroup_id-group_elements ?q $?qgroup)
	;?P <- (proposed_anchors_ids $?r)
	(test (and (member$ ?x $?pgroup) (member$ $?y $?qgroup)))
	=>
	(retract ?p1)
	(printout t "Rule check_potential fired for " ?x " " $?y crlf)
	(assert (remove ?x $?y))
	(assert (final_set-eid-hid ?x $?y)))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?x $?pgroup) (member$ ?x $?pgroup) $?y))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;; Rule to remove the other potential facts for '?x' once '?x' is processed for some hindi ID '?y' ;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule remove_eng_part
	?r <- (remove ?x $?y)
	?pot <- (anchor_type-english_id-hindi_id potential ?x $?)
	=>
	(printout t "Rule remove_eng_part fired for " ?x crlf)
	(retract ?pot))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;; Rule to remove the other facts present for hindi ID '?y' after '?y' is proposed for '?x' ;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule remove_hin_part
	?r <- (remove ?x $?y)
	?pot <- (anchor_type-english_id-hindi_id potential ? $?y)
	=>
	(printout t "Rule remove_hin_part fired for " $?y crlf)
	(retract ?pot))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;; Rule to retract the 'remove' fact once its work of removing resolved IDs from potential is over ;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule remove_remove-fact
	?r <- (remove ?x $?y)
	(not (or (exists (anchor_type-english_id-hindi_id potential ?x $?)) (exists (anchor_type-english_id-hindi_id potential ? $?y))))
	=>
	(printout t "Rule remove_remove-fact fired for " ?x " " $?y crlf)
	(retract ?r))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;; Rule to check if a match exists in the vicinity of pre-proposed Hindi group '?q' for ;;;;;;;;;;;;;;;;;;;;; 
;;;;;;;;;;;;;; 			the English group "?p" in which the English ID '?x' is present.        		;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule check_vicinity_potential_english
	?p1 <- (anchor_type-english_id-hindi_id potential ?x $?y)
	;?e <- (english_group_ids_mfs $?n)
	?g1 <- (proposed_groups ?p ?q)
	?g2 <- (Egroup_id-group_elements ?p $?pgroup)
	?g3 <- (Hgroup_id-group_elements ?q $?qgroup)
	?g6 <- (Hgroup_id-group_elements ?q1 $?hgroup1)
	?g7 <- (Hgroup_id-group_elements ?q2 $?hgroup2)
	?P <- (proposed_anchor_ids $?r)
	(test (and (= ?q1 (+ ?q 1)) (= ?q2 (- ?q 1)) (member$ ?x $?pgroup) (or (member$ $?y $?hgroup1) (member$ $?y $?hgroup2))))
	=>
	(printout t "Rule check_vicinity_potential_english fired for " ?x " " $?y crlf)
	(assert (final_set-eid-hid ?x $?y))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?x $?n) (member$ ?x $?n) $?y)))
	(if (member$ $?y $?hgroup1)
		then
		(assert (proposed_groups ?p (+ ?q 1)))
		else
		(assert (proposed_groups ?p (- ?q 1))))
	(assert (remove ?x $?y))
	(retract ?p1))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;; Rule to check if a match exists in the vicinity of pre-proposed English group '?p' for ;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;			 the Hindi group "?q" in which the Hindi ID '?y' is present.				  ;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule check_vicinity_potential_hindi
	?a1 <- (anchor_type-english_id-hindi_id potential ?x $?y)
	;?e <- (english_group_ids_mfs $?n)
	?g1 <- (proposed_groups ?p ?q)
	?g2 <- (Egroup_id-group_elements ?p $?pgroup)
	?g3 <- (Hgroup_id-group_elements ?q $?qgroup)
	?g6 <- (Egroup_id-group_elements ?p1 $?egroup1)
	?g7 <- (Egroup_id-group_elements ?p2 $?egroup2)
	;?P <- (proposed_anchor_ids $?r)
	(test (and (= ?p1 (+ ?p 1)) (= ?p2 (- ?p 1)) (member$ ?y $?qgroup) (or (member$ ?x $?egroup1) (member$ ?x $?egroup2))))
	=>
	(printout t "Rule check_vicinity_potential_hindi fired for " ?x " " $?y crlf)
	(assert (final_set-eid-hid ?x $?y))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?x $?n) (member$ ?x $?n) $?y)))
	(if (member$ ?x $?egroup1)
		then
		(assert (proposed_groups ?p1 ?q))
		else
		(assert (proposed_groups ?p2 ?q)))
	(assert (remove ?x $?y))
	(retract ?a1))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;	
;;;;;;;;;;;;;;;;;;; Rule to check if there is some intersection in the entries of an English ID '?a' ;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;					and select largest instersecting group.							 ;;;;;;;;;;;;;;;;;;;;

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

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;; Rule to check if only a single entry is present in potential and assert it as proposed anchor ;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defrule check_unique_potential
	(declare (salience -500))

	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?)
	?e3 <- (anchor_type-english_id-hindi_id potential ? $?y1)
	;?E <- (english_group_ids_mfs $?n)
	?EG <- (Egroup_id-group_elements ?egid $?gpe)
	?HG <- (Hgroup_id-group_elements ?hgid $?gph)
	;?P <- (proposed_anchor_ids $?r) 
	(test (and (eq ?e1 ?e2 ?e3) (member$ ?a $?gpe) (member$ $?y1 $?gph)))
	=>
	(retract ?e1)
	(assert (remove ?a $?y1))
	(printout t "Rule check_unique_potential fired for " ?a " " $?y1 crlf)
	(assert (proposed_groups ?egid ?hgid))
	(assert (final_set-eid-hid ?a $?y1)))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?a $?n) (member$ ?a $?n) $?y1))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


(defrule check_unique_potential_multiple_hindi_groups
	(declare (salience -500))
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1 $?y2)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $? $?)
	?e3 <- (anchor_type-english_id-hindi_id potential ? $?y1 $?y2)
	;?E <- (english_group_ids_mfs $?n)
	?EG <- (Egroup_id-group_elements ?egid $?gpe)
	?HG1 <- (Hgroup_id-group_elements ?hgid1 $?gph1)
	?HG2 <- (Hgroup_id-group_elements ?hgid2 $?gph2)
	;?P <- (proposed_anchor_ids $?r) 
	(test (and (eq ?e1 ?e2 ?e3) (member$ ?a $?gpe) (member$ $?y2 $?gph2) (member$ $?y1 $?gph1)))
	=>
	(retract ?e1)
	(assert (remove ?a $?y1))
	(assert (remove ?a $?y2))
	(printout t "Rule check_unique_potential fired for " ?a " " $?y1 crlf)
	(assert (proposed_groups ?egid ?hgid1))
	(assert (proposed_groups ?egid ?hgid2))
	(assert (final_set-eid-hid ?a $?y1 $?y2)))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?a $?n) (member$ ?a $?n) $?y1))))
