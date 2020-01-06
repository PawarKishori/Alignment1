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


(defrule replace_head_with_childs
?f<-(iter-h_g_id ?iter $?hids)
(hindi_head_id-grp_ids ?hid $?gids)
?f1<-(iter-type-eng_g_id-h_g_id ?iter1 ?type  ?id  ?hid)
(test (member$ ?hid $?hids))
(test (neq ?hid $?gids))
=>
	(retract ?f ?f1)
	(bind ?new_id  (explode$ (implode$ (remove_character " "  (implode$ $?gids) ","))))
	(bind $?hids (replace$ $?hids ?id ?id ?new_id))
	(if (>= ?iter ?iter1) then 
		(assert (iter-h_g_id ?iter $?hids))
	else
		(assert (iter-h_g_id ?iter1 $?hids))
	)
)


(defrule modify_fact
(declare (salience -100))
?f<-(iter-h_g_id ?iter $?hids)
(label ?lab)
=>
	(retract ?f)
	(assert (dummy ?lab $?hids))
)

			

