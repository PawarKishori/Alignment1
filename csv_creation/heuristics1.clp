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



;Check prep field is empty or not in P layer. If not empty then remove the ids. 
;ai2E, 2.10, An autonomous agent decides autonomously which action to take [in] the current situation to maximize progress towards its goals.
(defrule check_prep
(id-cat_coarse ?id preposition)
=>
	(assert (P1_tmp ?id 0))
	(assert (eng_id_decided ?id))
)


;Rule for adverb
;An autonomous agent decides [autonomously] which action to take in the current situation to maximize progress towards its goals.
(defrule adv_rule
(id-word ?id ?wrd)
(test (neq (numberp ?wrd) TRUE))
(test (eq (sub-string (- (length ?wrd) 1) (length ?wrd) ?wrd) "ly"))
(H_wordid-word	?hid ?hwrd)
(H_wordid-word  =(+ ?hid 1) rUpa)
(H_wordid-word  =(+ ?hid 2) se)
(not (hid_id_decided ?hid))
=>
	(bind ?rt (string-to-field (sub-string 1 (- (length ?wrd) 2) ?wrd)))
	(bind ?mng (gdbm_lookup "default-iit-bombay-shabdanjali-dic.gdbm" (str-cat ?rt "_adjective")))
	(if (neq ?mng FALSE) then
		(bind $?mngs  (explode$ (implode$ (remove_character "/"  ?mng " "))))
		(if (member$ ?hwrd $?mngs) then
			;(bind ?new_id (string-to-field (str-cat ?hid "," (+ ?hid 1) "," (+ ?hid 2))))
			;(assert (P1_tmp ?id ?new_id))
			(assert (P1_tmp ?id ?hid (+ ?hid 1) (+ ?hid 2)))
			(assert (eng_id_decided ?id))
			(assert (hid_id_decided ?hid))
			(assert (hid_id_decided (+ ?hid 1)))
			(assert (hid_id_decided (+ ?hid 2)))
		)
	)
)
