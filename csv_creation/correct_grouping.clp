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

 ;Get word info
 ;Added by Roja(19-11-19)
 ;[Image analysis] [systems] are examples of this kind of situation.
 (defrule assert_dummy_fact
 (declare (salience 3))
 (id-HM-source-grp_ids ?id ?mng ?s $?pre ?id1 $?post)
 (not (fact_created ?id))
 =>
        (assert (id-HM-source-grp_wrds ?id ?mng ?s $?pre ?id1 $?post))
        (assert (fact_created ?id))
 )

 ;Added by Roja (19-11-19)
 ;To replace ids with word in hindi meaning group fact (for printing suggestion in below rules wrd info needed)
 (defrule create_eng_wrds_info
 (declare (salience 2))
 (id-word ?id1 ?w)
 ?f<-(id-HM-source-grp_wrds ?id ?mng ?s $?pre ?id1 $?post)
 (test (neq (numberp ?w) TRUE))

 =>
        (retract ?f)
        (assert (id-HM-source-grp_wrds ?id ?mng ?s $?pre ?w $?post))
 )

 (defrule create_hindi_wrd_info
 (declare (salience 12))
 (manual_mapped_id-word	?id ?wrd)
 ?f<-(E_head_id-Hindi_ids ?eid $?pre ?id $?post)
 =>
	(retract ?f)
	(assert (E_head_id-Hindi_ids ?eid $?pre ?wrd $?post))
 )

(defrule check_mwe
(id-HM-source-grp_ids ?id ?hmng ?s $?g_ids)
(Eng_label-group_elements ?lab  $?g_ids1)
(test (member$ $?g_ids $?g_ids1))
(test (> (length $?g_ids) 1))
(id-HM-source-grp_wrds ?id ?hmng ?s $?wrds)
(K_exact_match $?ids)
=>
	(bind ?val (nth$ ?id $?ids))
	(if (neq ?val 0) then 
		(bind ?mwe (string-to-field (implode$ (remove_character " " (implode$ $?wrds) "_"))))
		(bind ?hids (explode$ (implode$ (remove_character "," ?val " "))))
		(assert (E_head_id-Hindi_ids ?id ?hids))
		(assert (E_head_id-E_mwe ?id ?mwe))
		(printout t "MWE expr " ?val " " ?mwe " "?hids crlf)
	)
	
)


(defrule calling_shreya_module
(declare (salience -1))
(E_head_id-E_mwe ?id ?emwe)
(E_head_id-Hindi_ids ?id $?wrds)
=>
	(bind ?hmwe (implode$ (remove_character " " (implode$ $?wrds) "_")))
;	(bind ?mng (system "python3 $HOME_alignment/csv_creation/meaning_of_every_word_shreya.py " ?emwe " "?hmwe " $HOME_anu_test/Anu_data/domain/computer_science_dic.txt"))
	(printout t ?hmwe " " (type ?hmwe) crlf)
	(assert (E_head_id-H_ids ?id 10 12,13))
;	(printout t ?mng crlf)
)

(defrule replace_in_K_exact
(E_head_id-H_ids ?id $?hids)
(id-HM-source-grp_ids ?id ?hmng ?s $?g_ids)
?f1<- (K_exact_match $?ids)
(not (fact_replaced ?id))
=>
	(loop-for-count (?i 1 (length $?g_ids))
		(bind ?m  (nth$ ?i $?g_ids))
		(bind ?n (nth$ ?i $?hids))
		(printout t ?m ?n crlf)
		(loop-for-count (?j (length $?ids)) 
			(if (eq ?j ?m) then
				(bind $?ids (replace$ $?ids ?m ?m ?n))
;				(printout t $?ids crlf)
			)	
		)
	)
	(retract ?f1)
	(assert (K_exact_match_using_shreya $?ids))
	(assert (fact_replaced ?id))
)

;Eng: While some translation systems have been developed, there is a lot of scope for improvement in [translation quality].
;Anu: jaba ki kuCa anuvAxa praNAliyAz vikAsa kI gayIM hEM, bahuwa sArA guFjAiSa [anuvAxa guNavawwA meM] suXAra ke lie hE.
;NMT: jabaki kuCa anuvAxa praNAliyoM ko vikasiwa kiyA gayA hE, [anuvAxa kI] [guNavawwA meM] suXAra kI kAPI guFjAiSa hE.
(defrule merge_group
(fact_replaced ?id)
?f0<-(E_head_id-H_ids ?id $?h_ids)
(id-HM-source-grp_ids ?id ?hmng ?s $?g_ids)
(Eng_label-group_elements ?lab $?g_ids1)
(test (member$ $?g_ids $?g_ids1))
?f<-(Hnd_label-group_elements ?h_lab $?hids)
?f1<-(Hnd_label-group_elements ?h_lab1 $?hids1)
(K_exact_match_using_shreya $?ids)
(test (neq (str-index "," (nth$ ?id $?ids)) FALSE))
(test (member$ (remove_character "," (nth$ ?id $?ids) " ") $?hids))
=>
	(loop-for-count (?i 1 (length $?h_ids)) 
		(if (member$ (nth$ ?i $?h_ids) $?hids1) then 
			(retract ?f ?f0 ?f1)
			(bind ?new_lab (string-to-field (str-cat ?h_lab "_" ?h_lab1)))
			(assert (Hnd_label-group_elements ?new_lab $?hids1 $?hids)) ;assuming ?f1 > f as we are picking in sequence
		)
	)	
)

;Need to test below rule
(defrule merge_group1
(fact_replaced ?id)
?f0<-(E_head_id-H_ids ?id $?h_ids) 
(id-HM-source-grp_ids ?id ?hmng ?s $?g_ids)
(Eng_label-group_elements ?lab $?g_ids1)
(test (member$ $?g_ids $?g_ids1))
?f<-(Hnd_label-group_elements ?h_lab $?hids)
?f1<-(Hnd_label-group_elements ?h_lab1 $?hids1)
(K_exact_match_using_shreya $?ids)
=>
        (loop-for-count (?i 1 (length $?h_ids)) 
                (if (member$ (nth$ ?i $?h_ids) $?hids1) then
                        (retract ?f ?f0 ?f1)
                        (bind ?new_lab (string-to-field (str-cat ?h_lab "_" ?h_lab1)))
                        (assert (Hnd_label-group_elements ?new_lab $?hids1 $?hids)) ;assuming ?f1 > f as we are picking in sequence
                )
        )
)

