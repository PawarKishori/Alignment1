;ai2E 2.3, [Human beings] do not satisfy this definition of rationality.
; [manuRya] buxXi kI isa pariBARA se sanwuRta nahIM howA.
(defrule eng_comp_rule_with_same_mng
?f<-(iter-type-eng_g_id-h_g_id ?iter potential ?head  $?ids)
?f1<-(iter-type-eng_g_id-h_g_id ?iter1 potential ?child  $?ids)
(eng_relation_name-head-chiid compound ?head  ?child )
=>
	(retract ?f ?f1)
	(assert (iter-type-eng_g_id-h_g_id (+ ?iter 1) anchor  ?head $?ids))
	(assert (iter-type-eng_g_id-h_g_id (+ ?iter1 1) anchor  ?child 0))
)


;ai2E, 2.38 Rational Action is the [action] that maximizes the expected value of the performance measure given the percept sequence to date.
;yukwisafgawa kriyA, vaha [kriyA howI] hE, jo wiWi karane ke lie boXa anukrama meM xie gae niRpAxana mApa ke apekRiwa mUlya ko aXikawama karawI hE.
(defrule comp_rule_in_hin
?f<-(iter-type-eng_g_id-h_g_id ?iter potential ?h $?hids)
(hnd_relation_name-head-chiid compound ?h ?hid )
(test (member$ ?hid $?hids))
=>
	(retract ?f)
	(assert (iter-type-eng_g_id-h_g_id  (+ ?iter 1) anchor ?h ?hid))
	(assert (anchor_decided ?hid))
)


(defrule del_if_anch_decided
?f<-(iter-type-eng_g_id-h_g_id ?iter potential ?h $?hids)
(anchor_decided ?hid)
(test (member$ ?hid $?hids))
=>
	(retract ?f)
	(bind ?new_ids (delete-member$ $?hids ?hid))
	(assert (iter-type-eng_g_id-h_g_id  (+ ?iter 1) potential ?h ?new_ids))
)


;ai2E, 2.38 [Rational Action] is the action that maximizes the expected value of the performance measure given the percept sequence to date.
;[yukwisafgawa kriyA], vaha kriyA howI hE, jo wiWi karane ke lie boXa anukrama meM xie gae niRpAxana mApa ke apekRiwa mUlya ko aXikawama karawI hE.
(defrule align_comp_using_grouping
(iter-type-eng_g_id-h_g_id ?iter anchor ?id $?hids)
(eng_relation_name-head-chiid compound ?id ?c )
(Eng_label-group_elements ?lab $?eids)
(test (and (member$ ?id $?eids) (member$ ?c $?eids)))
(Hnd_label-group_elements ? $?h_ids)
(test (member$ $?hids $?h_ids))
=>
	(bind ?new_id (delete-member$ $?h_ids $?hids))
	(assert (iter-type-eng_g_id-h_g_id (+ ?iter 1) anchor ?c ?new_id))
	(assert (anchor_decided ?new_id))
)

;;ai2E, 2.38 [Rational Action] is the action that maximizes the expected value of the performance measure given the percept sequence to date.
;;yukwisafgawa kriyA, vaha [kriyA howI] hE, jo wiWi karane ke lie boXa anukrama meM xie gae niRpAxana mApa ke apekRiwa mUlya ko aXikawama karawI hE.
;(defrule align_using_eng_and_hindi_parse
;(eng_relation_name-head-chiid ?rel  ?h ?c )
;(iter-type-eng_g_id-h_g_id ?iter anchor ?h $?hids)
;(hnd_relation_name-head-chiid ?rel ?h1 ?c1 )
;(test (or (member$ ?h1 $?hids)
	  









(defrule create_fact
(declare (salience -100))
?f<-(iter-h_g_id  ?iter  $?hids)
(iter-type-eng_g_id-h_g_id ?iter1 ? ?id ?hid)
(test (neq (nth$ ?id $?hids) ?hid))
(not (anchor_replaced ?id))
=>
        (retract ?f)
        (bind $?hids (replace$ $?hids ?id ?id ?hid))
        (if (>= ?iter1 ?iter) then
                (assert (iter-h_g_id  ?iter1  $?hids))
        else
                (assert (iter-h_g_id  ?iter  $?hids))
        )
        (assert (anchor_replaced ?id))
)


(defrule check_potential_anchor
(declare (salience -200))
?f<-(iter-h_g_id  ?iter  $?hids)
?f1<-(iter-type-eng_g_id-h_g_id ?iter1 potential ?id ?hid)
=>
        (bind ?type "")
        (printout t ?type crlf)
        (loop-for-count (?i (length $?hids))
                (bind ?val (nth$ ?i $?hids))
                (if (and (neq ?i ?id) (neq ?val ?hid)) then
                        (bind ?type "anchor")
                else (if (neq ?i ?id) then

                        (bind ?type "potential")
                        (break)
                )
                )
        )
        (if (eq ?type "anchor") then
                (retract ?f1)
                (assert (iter-type-eng_g_id-h_g_id (+ ?iter1 1) anchor ?id ?hid))
        )
)

