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

;correct repeated eng wrd mng using eng grouping and hindi grouping
;ai2E, 2.106 [multiple goals]
;(defrule correct_p_lay_with_wrng_grp_id
;?f0<-(Repeated_id  ?id)
;(Eng_label-group_elements ?lab  $?e_gids)
;(test (member$ ?id $?e_gids))
;(test (member$ (- ?id 1) $?e_gids))
;(eng_wrd-occurrences ?wrd 1)
;(id-word =(- ?id 1) ?wrd)
;?f1<-(P $?ids)
;(H_wordid-word	?hid&=(nth$ (- ?id 1) $?ids) ?hwrd)
;(hin_wrd-occurrences ?hwrd 1)
;(Hnd_label-group_elements ?hlabel  $?h_gids)
;(test (member$ ?hid $?h_gids))
;=>
;	(printout t (nth$ (- ?id 1) $?ids) " " ?hid " " (+ ?hid 1) " " crlf)
;	(assert (grouping_corrected_id-prev_val ?id (nth$ ?id $?ids)))
;	(retract ?f0 ?f1)
;	(bind ?new_ids (replace$ $?ids ?id ?id (+ ?hid 1)))
;	(assert (P ?new_ids))
;)
;
(defrule interchange_grp_val_aft_correction
(grouping_corrected_id-prev_val	 ?id $?val)
(id-word ?id  ?wrd)
(id-word ?id1  ?wrd)
?f1<-(eng_wrd-occurrences ?wrd ?count&~1)
(test (neq ?id ?id1))
?f<-(P $?ids)
=>
	(if (eq (nth$ ?id1 $?ids) (nth$ ?id $?ids)) then 
		(retract ?f ?f1)
		(bind ?new_ids (replace$ $?ids ?id1 ?id1 $?val))
		(assert (P ?new_ids))
		(assert (eng_wrd-occurrences ?wrd (- ?count 1)))
	)
)


(defrule correct_p_lay_with_repeated_wrd1
?f0<-(Repeated_id  ?id)
(Eng_label-group_elements ?lab  $?e_gids)
(test (member$ ?id $?e_gids))
(test (member$ (- ?id 1) $?e_gids))
(id-word =(- ?id 1) ?wrd)
?f1<-(P $?ids)
(P-head_id-grp_ids ?h_id $?hgids)
(H_wordid-word  ?hid&=(nth$ (- ?id 1) $?ids) ?hwrd)
(Hnd_label-group_elements ?hlabel  $?h_gids)
(test (member$ ?hid $?h_gids))
(test (member$ ?h_id $?h_gids))
=>
	(printout t (nth$ (- ?id 1) $?ids) " " ?hid " " (+ ?hid 1) " " crlf)
	(bind ?new_hids (explode$ (implode$ (remove_character " " (implode$ $?hgids) ","))))
        (assert (grouping_corrected_id-prev_val ?id (nth$ ?id $?ids)))
        (retract ?f0 ?f1)
        (bind ?new_ids (replace$ $?ids ?id ?id $?new_hids))
        (assert (P ?new_ids))
)


(defrule modify_fact
(declare (salience -10))
?f<- (P $?ids)
=>
	(retract ?f)
	(assert (P1 $?ids))
)

