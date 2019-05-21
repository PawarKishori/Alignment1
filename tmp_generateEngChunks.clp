(defrule generate-Daughter-from-Daughters
	?f0<-(Head-Level-Mother-Daughters ?h ?l ?m $?ds)
	(test (> (length$ $?ds) 1))
	=>
	(retract ?f0)
	(assert (Head-Level-Successor_depth-Ancestor-Successor ?h ?l 1 ?m (nth$ 1 $?ds)))
;	(printout t "#################### : " ?h " " ?l " 1 " ?m " " (nth$ 1 $?ds) crlf)
	(assert (Head-Level-Mother-Daughters ?h ?l ?m (rest$ $?ds)))
)
(defrule generate-Daughter-from-Daughters-helper
	?f0<- (Head-Level-Mother-Daughters ?h ?l ?m $?ds)
	(test (= (length$ $?ds) 1)) 
        =>
        (retract ?f0)
        (assert (Head-Level-Successor_depth-Ancestor-Successor ?h ?l 1 ?m $?ds))
;	(printout t "#################### : " ?h " "?l " 1 " ?m " " $?ds crlf)
)

(defrule generate-ancestor-level
;	(declare (salience 10))
	(id-word ?id ?leaf)
	(Head-Level-Successor_depth-Ancestor-Successor ?h ?l ?al1 ?m ?id)
	(Head-Level-Successor_depth-Ancestor-Successor ?h2 ?l2&:(< ?l2 ?l) ?al2 ?gm ?m)
	=>
;	(printout t "**************** : " ?h2 " " ?l2 " " (+ ?al1 1) " " ?gm " " ?id crlf)
	(assert (Head-Level-Successor_depth-Ancestor-Successor ?h2 ?l2 (+ ?al1 1) ?gm ?id))
)

(defrule anc-suc
	(id-word ?id1 ?word1)
	(Head-Level-Successor_depth-Ancestor-Successor ?h1 ?l1 ?al1 ?anc1 ?id1)
	=>
	(assert (chunk_name-head-ids ?h1 ?anc1 ?id1))	
	;(assert (Ancestor-Successors_word ?anc1 ?word1))	
)
(defrule anc-suc-merger
	?f0<-(chunk_name-head-ids ?h1 ?anc1 ?id1)
	?f1<-(chunk_name-head-ids ?h1 ?anc1 $?id2)
	(test (neq ?f0 ?f1))
	=>
	(retract ?f0 ?f1)
	(assert (chunk_name-head-ids ?h1 ?anc1 ?id1 $?id2))
)
(defrule chunk-info-with-chunk-type
	(declare (salience -1))
	(chunk_name-head-ids ?h1 ?anc1 $?ids)	
	(Node-Category ?anc1 ?anc1_type)
	=>
	;(assert (chunk_type-name-headid-ids ?anc1_type ?anc1 (nth$ (length$ $?ids) $?ids) $?ids ))
	(assert (chunk_type-name-headid-ids ?anc1_type ?anc1 ?h1 $?ids ))
)
;Write this rule in case you want to generate Ancestor-Successors_word from chunk_name-ids using loop in LHS block
;(defrule generate-anc-suc-words-from-ids
;	(chunk_name-ids ?anc)
;)

"
(defrule ancestor-successor
	(declare salience
	(id-word ?id ?leaf)
	?f0<-(Head-Level-Successor_depth-Ancestor-Successor ?h ?l ?al ?a ?id)
	(id-word ?id1 ?leaf1)
	?f1<-(Head-Level-Successor_depth-Ancestor-Successor  ?h1 ?l1 ?al1 ?a ?id1)
	(test (neq ?f0 ?f1))
	(test (< ?id ?id1))
;	(bind $?grp_ids (sort > (create$  $?grp_ids ?viSeRaNa)))
;	(test (integerp (member$ $?id1)))
	=>
;	(printout t "Rule fired" ?f0 crlf)
;	(bind $?succs (sort < (create$ ?id1 ?id1)))
	retract ?f0 ?f1)
	(assert (chunk_name-ids ?a ?id ?id1))
;	(assert (chunk_name-ids ?a $?succs))
)

(defrule ancestor-successor-merger
	?f0<-(chunk_name-ids ?a $?id1)
	?f1<-(chunk_name-ids ?a $?id2)
;	(test (< (first$ $?id1) (first$ $?id2)));find correct syntax of this and write this condition to get S2 1 2 3 4 in sequence
	(test (neq ?f0 ?f1)) 
	=>
	(bind $?succs (sort < (create$ $?id1 $?id2)))
	(retract ?f0 ?f1)
	(assert (chunk_name-ids ?a $?succs)) 	
)
"
;(defrule ancestor-successor-combine
;	(id-word ?hid ?hleaf)
;	(id-word ?hid1 ?hleaf1)
;	(id-word ?id ?leaf)
;	?f0<-(Ancestor-Head-Successors_word ?a ?hleaf ?leaf)
;	?f1<-(Ancestor-Head-Successors_word ?a ?hleaf1 $?leaf1)
;	(test (neq ?f0 ?f1))
;	;(test (neq ?pid P1))
;	=>
;	(printout t "FINAL 2: " crlf)
;	(retract ?f0 ?f1)
;	(assert (Ancestor-Head-Successors_word ?a ?hleaf ?leaf $?leaf1))
;	(assert (Ancestor-Head-Successors_id ?a ?hid ?id $?hid1))
;)
