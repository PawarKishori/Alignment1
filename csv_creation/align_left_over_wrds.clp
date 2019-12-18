
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


(defrule align_left_over_kriyA_mUla
(kriyA_mUla_wrd-ids  ?k_m_mng  $?ids)
(Hnd_label-group_elements ?lab $?hids)
(P1_left_over_ids $?lids)
(test (member$ $?ids $?lids))
(id-root ?id ?rt)
(test (neq (gdbm_lookup "default-iit-bombay-shabdanjali-dic.gdbm" (str-cat ?rt "_verb")) "FALSE"))
?f<-(P1 $?pids)
(test (eq (nth$ ?id $?pids) 0))
;(test (neq (str-index "_" ?lab) FALSE))
=>
	(bind ?mng (gdbm_lookup "default-iit-bombay-shabdanjali-dic.gdbm" (str-cat ?rt "_verb")))
        (bind ?mng_lst (explode$ (implode$ (remove_character "/"  ?mng " "))))
	(if (member$ ?k_m_mng ?mng_lst) then 
		(bind $?new_pids (replace$ $?pids ?id ?id $?hids))
		(retract ?f)
		(assert (P1 $?new_pids))
	)
)

	

