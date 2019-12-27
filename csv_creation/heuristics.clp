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


(defrule dummy_fact
(declare (salience 1000))
?f<-(P $?pids)
=>
	(retract ?f)
	(assert (P1_tmp $?pids))
)

;Check prep field is empty or not in P layer. If not empty then remove the ids. 
;ai2E, 2.10, An autonomous agent decides autonomously which action to take [in] the current situation to maximize progress towards its goals.
(defrule check_prep
(id-cat_coarse ?id preposition)
?f<- (P1_tmp $?pids)
(test (neq (nth$ ?id $?pids) 0))
=>
	(retract ?f)
	(bind ?new_pids (replace$ $?pids ?id ?id 0))
	(assert (P1_tmp ?new_pids))
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
?f<-(P1_tmp $?pids)
(not (p1_corrected ?id))
(not (hid_decided ?hid))
=>
	(bind ?rt (string-to-field (sub-string 1 (- (length ?wrd) 2) ?wrd)))
	(bind ?mng (gdbm_lookup "default-iit-bombay-shabdanjali-dic.gdbm" (str-cat ?rt "_adjective")))
	(if (neq ?mng FALSE) then
		(bind $?mngs  (explode$ (implode$ (remove_character "/"  ?mng " "))))
		(if (member$ ?hwrd $?mngs) then
			(bind ?new_id (string-to-field (str-cat ?hid "," (+ ?hid 1) "," (+ ?hid 2))))
			(bind ?new_pids (replace$ $?pids ?id ?id ?new_id))
			(retract ?f)
			(assert (P1_tmp ?new_pids))
			(assert (p1_corrected ?id))
			(assert (hid_decided ?hid))
		)
	)
)

			
(defrule remove_aligned_id
?f<-(P1_tmp $?pids)
(p1_corrected ?id)
(test (neq (nth$ ?id $?pids) 0))
=>
	(bind ?ids (nth$ ?id $?pids))
        (bind ?new_ids (explode$ (implode$ (remove_character ","  ?ids " "))))
	(loop-for-count (?i (length $?pids))
		(if (and (member$ (nth$ ?i $?pids) ?new_ids) (neq ?i ?id)) then
			(bind ?new_pids (replace$ $?pids ?i ?i 0))
			(retract ?f)
			(assert (P1_tmp ?new_pids))
		)
	)
)

;check ai2E, 
;2.35 sir discuss
;2.55 , 2.62, 
;2.102 grouping


(defrule modify_fact
(declare (salience -100))
?f<-(P1_tmp $?pids)
=>
	(retract ?f)
	(assert (P1 $?pids))
)
