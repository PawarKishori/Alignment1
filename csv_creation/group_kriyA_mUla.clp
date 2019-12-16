(deffunction remove_character(?char ?str ?replace_char)
                        (bind ?new_str "")
                        (bind ?index (str-index ?char ?str))
                        (if (neq ?index FALSE) then
                        (while (neq ?index FALSE) 
                        (bind ?new_str (str-cat ?new_str (sub-string 1 (- ?index 1) ?str) ?replace_char))
                        (bind ?str (sub-string (+ ?index 1) (length ?str) ?str))
                        (bind ?index (str-index ?char ?str))
                        )
                        )
                (bind ?new_str (explode$ (str-cat ?new_str (sub-string 1 (length ?str) ?str))))
 )

;Added by Roja(19-11-19)
 ;[Image analysis] [systems] are examples of this kind of situation.
 (defrule assert_dummy_fact
 (declare (salience 3))
 (id-HM-source-grp_ids ?id ?mng ?s $?pre ?id1 $?post)
 (not (fact_created ?id))
 =>
        (assert (id-HM-source-grp_rts ?id ?mng ?s $?pre ?id1 $?post))
        (assert (fact_created ?id))
 )

 ;Added by Roja (19-11-19)
 ;To replace ids with word in hindi meaning group fact (for printing suggestion in below rules wrd info needed)
 (defrule create_eng_wrds_info
 (declare (salience 2))
 (id-root ?id1 ?r)
 ?f<-(id-HM-source-grp_rts ?id ?mng ?s $?pre ?id1 $?post)
 (test (neq (numberp ?r) TRUE))
 =>
        (retract ?f)
        (assert (id-HM-source-grp_rts ?id ?mng ?s $?pre ?r $?post))
 )

;As parser splits for kriyA mUla correct the grouping
(defrule correct_eng_grouping_kriyA_mUla
(id-HM-source-grp_ids ?id ?mng ?source $?gids)
(id-HM-source-grp_rts ?id ?mng ?source $?rts)
(id-cat_coarse ?id1 verb)
(test (and (member$ ?id1 $?gids) (> (length $?gids) 1)))
?f<-(Eng_label-group_elements ?lab  $?ids)
?f1<-(Eng_label-group_elements ?lab1  $?ids1)
(test (member$ ?id1 $?ids))
(test (member$ (+ ?id1 1) $?ids1))
(not (grouping_decided ?id1))
=>
	(retract ?f ?f1)
	(bind ?new_lab (string-to-field (str-cat ?lab "_" ?lab1)))
	(assert (Eng_label-group_elements ?new_lab $?ids $?ids1))
	(assert (grouping_decided ?id1))
)


(defrule get_mng_for_kriyA_mUla
(id-HM-source-grp_ids ?id ?mng ?source $?gids)
(grouping_decided ?id)
(H_wordid-word	?hid ?hwrd)
(test (neq (str-index ?hwrd ?mng) FALSE))
(id-root ?id ?rt)
(test (neq (gdbm_lookup "default-iit-bombay-shabdanjali-dic.gdbm" (str-cat ?rt "_verb")) "FALSE"))
=>
	(bind ?mng (gdbm_lookup "default-iit-bombay-shabdanjali-dic.gdbm" (str-cat ?rt "_verb")))
        (bind $?mng_lst (create$ (remove_character "/" ?mng " ")))
	(printout t $?mng_lst crlf)
	(loop-for-count (?i 1 (length $?mng_lst)) 
		(if (neq (str-index ?hwrd (nth$ ?i $?mng_lst)) FALSE) then
			(assert (eng_id-hin_id-hin_mng  ?id ?hid (nth$ ?i $?mng_lst)))
			(printout t "hello " ?hid  "  "   (nth$ ?i $?mng_lst) crlf)
		)
	)
)


;(defrule insert_mng_in_P
;(eng_id-hin_id-hin_mng  ?id ?hid ?hmng)
;(P $?ids)
;(H_wordid-word  ?hid ?hwrd)
;(H_wordid-word  ?hid1 ?hwrd1)
;=>
;	(bind ?i (str-index ?hwrd ?hmng))
;	(bind ?i (+ ?i (length ?hwrd)))
;	(bind ?mng (string-to-field (sub-string (+ ?i 1) (length ?hmng) ?hmng) ))
;	(if (neq (str-index ?mng ?hwrd1) FALSE) then
;		(printout t ?hid1 crlf)
;	)
;
;)


