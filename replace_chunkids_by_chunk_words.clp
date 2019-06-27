;###########################Rules to replace ids by their respective words and roots in english chunks formed using constituency parser (sd_chunk.dat) #####################################3
(defrule eng_ids_replaced_by_words_in_chunk_helper1
        (id-original_word ?y ?word1)
	?f1<-(chunk-ids ?  $?preEid ?y $?postEid)
        =>
        (assert (fact_no-chunk_ids-sep-chunk_wrds ?f1 (length$ $?preEid) "-" ?y "-" ?word1))         
)

(defrule eng_ids_replaced_by_words_in_chunk
	?f0<-(fact_no-chunk_ids-sep-chunk_wrds ?f $?indices1 "-" $?ids "-" $?words)
        ?f1<-(fact_no-chunk_ids-sep-chunk_wrds ?f $?indices2 "-" $?rest_ids "-" $?rest_words)
        (test (neq ?f0 ?f1))
	(test (eq (- (nth$ 1 $?indices2) (nth$ (length$ $?indices1) $?indices1)) 1))
        =>
        (retract ?f0 ?f1)
        (assert (fact_no-chunk_ids-sep-chunk_wrds ?f $?indices1 $?indices2 "-" $?ids $?rest_ids  "-" $?words $?rest_words ))
)

(defrule eng_ids_replaced_by_words_in_chunk_final_facts
	(declare (salience -1))
	?f0<-(fact_no-chunk_ids-sep-chunk_wrds ?f $?indices "-" $?ids  "-" $?words )
	=>
	(retract ?f0)
	(assert (chunk_ids-sep-chunk_wrds $?ids "-" $?words ))
)
	  
(defrule eng_ids_replaced_by_roots_in_chunk_helper1
        (id-root ?y ?root1)
	?f1<-(chunk-ids ?  $?preEid ?y $?postEid)
        =>
        (assert (fact_no-chunk_ids-sep-chunk_roots ?f1 (length$ $?preEid) "-" ?y "-" ?root1))         
)

(defrule eng_ids_replaced_by_roots_in_chunk
	?f0<-(fact_no-chunk_ids-sep-chunk_roots ?f $?indices1 "-" $?ids "-" $?roots)
        ?f1<-(fact_no-chunk_ids-sep-chunk_roots ?f $?indices2 "-" $?rest_ids "-" $?rest_roots)
        (test (neq ?f0 ?f1))
	(test (eq (- (nth$ 1 $?indices2) (nth$ (length$ $?indices1) $?indices1)) 1))
        =>
        (retract ?f0 ?f1)
        (assert (fact_no-chunk_ids-sep-chunk_roots ?f $?indices1 $?indices2 "-" $?ids $?rest_ids  "-" $?roots $?rest_roots ))
)

(defrule eng_ids_replaced_by_roots_in_chunk_final_facts
	(declare (salience -1))
	?f0<-(fact_no-chunk_ids-sep-chunk_roots ?f $?indices "-" $?ids  "-" $?roots )
	=>
	(retract ?f0)
	(assert (chunk_ids-sep-chunk_roots $?ids "-" $?roots ))
)
	  
