(defglobal ?*var* = debug_v)

(defrule generating_proposed_merging_groups "merging hindi groups1"
    ?org <- (K_group_elements $?fulleng )
    ?process <- (K_group_elements $?p1 ?x $?p2 )
    (K_id-word ?x  ?anu_meaning)
    (or (E_id-k_dict-mfs-wsd_modulo  ?x  $?p3 ?anu_meaning_id $p4 mfs ?)
        (E_id-k_dict-mfs-wsd_modulo  ?x ? mfs $?p5 ?anu_meaning_id $?p6))

    (H_wordid-word ?anu_meaning_id ?anu_meaning)
    (Hgroup_id-group_elements ? $?hgrpids)
    (test (member$ ?anu_meaning_id  $?hgrpids))
    (test (eq ?org ?process))
    =>
    ;(printout t "Eng grp ids " $?p1 ?x  $?p2 " hindi ids allocated => " ?anu_meaning_id crlf ) 
    (printout t "Eng grp ids " $?fulleng " hindi grp ids => " $?hgrpids crlf ) 
    (printout ?*var* "(proposed_merge_group_egids-mfs-hgids	" (implode$ $?fulleng) "	mfs	" (implode$ $?hgrpids) ")"  crlf ) 
    (assert (proposed_merge_group_egids-mfs-hgids $?fulleng mfs $?hgrpids))    

)

(defrule merging_proposed_grouping  "merging hindi group2" 
?g <- (Hgroup_id-group_elements ? $?hgrpids1)
?h <- (Hgroup_id-group_elements ? $?hgrpids2)

?f1 <- (proposed_merge_group_egids-mfs-hgids $?egids mfs $?hgrpids1)    
?f2 <- (proposed_merge_group_egids-mfs-hgids $?egids mfs $?hgrpids2)    
(test (neq ?f1 ?f2))

?f3 <- (proposed_merge_group_egids-mfs-hgids $?egids mfs $?X ?x)    
?f4 <- (proposed_merge_group_egids-mfs-hgids $?egids mfs  ?y $?Y)    
(test (eq ?f1 ?f3))
(test (eq ?f2 ?f4))
(test (< ?x ?y) )
=>
(retract ?g ?h)
(assert (H_gids $?hgrpids1 $?hgrpids2))    
(assert (egids-mfs-hgids $?egids mfs $?hgrpids1 $?hgrpids2))    
)


(defrule generate_merged_hindi_fact_file_v2 "Generating new grouping fact file"
(H_gids $?hgids)
(Hgroup_id-group_elements ? $?OldHGrpIds)
(test (not (member$ $?OldHGrpIds $?hgids)))
=>
(assert (H_gids $?OldHGrpIds))
;(printout t "PPP" crlf)
)

