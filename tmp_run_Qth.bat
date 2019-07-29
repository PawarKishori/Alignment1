;---------------------------------------------------------
;Bottom-Up Approach by most correct logic program
; lwg and chunking module(confirm the terminology from sir) for enflish sentence: NP, VP chunks are found
; Finding all small chunks in english sentence with their heads, irrespective of total number of heads in overall sentence.

(load "new_alignment.clp")
(bind ?*hpath* (str-cat ?*hpath* "/tmp_generateEngChunks.clp"))
(load ?*hpath*)
(load-facts "E_constituents_info.dat")
(load-facts "word.dat")
(load-facts "Node_category.dat")
(facts)
(watch activations)
(watch facts)
(run)
(facts)
(save-facts "E_chunk_ids.dat"  local chunk_type-name-headid-ids)
(save-facts "E_ancestor-successor.dat" local Head-Level-Successor_depth-Ancestor-Successor)
(clear)
;---------------------------------------------------------
(load "new_alignment.clp")
;(bind ?*hpath* (str-cat ?*hpath* "/parser_anchor.clp"))
;(load ?*hpath*)
(load-facts "H_relation_final_facts")
(load-facts "E_relation_final_facts")
(load-facts "anchor.dat")
;(run)
;(save-facts "A_parser.dat"  local eid-hid)
(exit)
