;File originally added by Prashant Raj. For any queries feel free to contact me on "prashantraj012@gmail.com".

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Here I have tried to implement the logic that whenever for an English ID we get an anchor (Starting Anchor), we consider 
;it to be reliable and hence we directly put it forth as final or proposed anchors for the N1 layer in the final.html file.
;At the time of proposing this I also store the information of the groups to which these IDs belong. For example if an ID
;of English belongs to group number 'X' of English and the corresponding suggestion for it belongs to group number 'Y' of
;Hindi, a new fact will be asserted which stores the information X-->Y. This information will later be helpful in the task
;of resolving the potential anchors wherever required and also suggesting where multiple groups need to be merged in a
;bi-directional manner.

;Corpus: BUgol2.1E_tmp (NCERT Geography, Chapter-2)
;Sentence: 2.77

;English sentence: The part of the Himalayas lying between Satluj and Kali rivers is known as Kumaon Himalayas.
;Hindi sentence: सतलुज तथा काली नदियों के बीच स्थित हिमालय के भाग को कुमाँऊ हिमालय के नाम से भी जाना जाता है.

;English Grouping: [The part][of the Himalayas][lying][between Satluj and Kali][rivers][is known][as Kumaon Himalayas]
;Hindi Grouping: [sawaluja][waWA][kAlI][naxiyoM ke bIca][sWiwa himAlaya ke][BAga ko][kumAzU himAlaya ke][nAma se][BI jAnA jAwA hE]

;For this example sentence, we got anchors for 'part', 'Satluj', 'and', 'Kali', 'rivers', 'known', and 'Kumaon'. So for these
;IDs of English the code will automatically assert the information about which groups of English are getting aligned with
;which groups of Hindi.

;Some facts asserted after this rule fires for every starting anchor:
;
;(final_set-eid-hid 2 10 11)	|
;(final_set-eid-hid 8 1)		| Anchor alignment info.
;
;(proposed_groups 1 6)			|
;(proposed_groups 4 1)			| Group alignment info.

(defrule check_anchor
	(declare (salience 500))
	?e <- (anchor_type-english_id-hindi_id anchor ?a $?y)
	;?E <- (english_group_ids_mfs $?n)
	?EG <- (Egroup_id-group_elements ?egid $?gpe)
	?HG <- (Hgroup_id-group_elements ?hgid $?gph)
	;?P <- (proposed_anchor_ids $?r)
	(test (and (member$ ?a $?gpe) (member$ $?y $?gph)))
	=>
	(retract ?e)
	(assert (remove ?a $?y))
	(printout t "Rule check_anchor fired for " ?a " " $?y crlf)
	(assert (proposed_groups ?egid ?hgid))
	(assert (final_set-eid-hid ?a $?y)))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?a $?n) (member$ ?a $?n) $?y))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Sometimes it may happen that the IDs 'Y' and 'Z' which are being suggested by the resources for a single English ID 'X' are 
;present in different groups in Hindi. In such cases we need to propose that X-->Y and X-->Z. This means that the group in
;which X is present, let us suppose 'A', needs to be mapped with the group in which Y and Z are present, let us suppose 'B'
;and 'C' respectively. Hence we need to assert the information that English group A should align to Hindi groups B and C.
;


(defrule check_anchor_multiple_hindi_group_match
	(declare (salience -500))
	?e <- (anchor_type-english_id-hindi_id anchor ?a $?y1 $?y2)
	;?E <- (english_group_ids_mfs $?n)
	?EG <- (Egroup_id-group_elements ?egid $?gpe)
	?HG1 <- (Hgroup_id-group_elements ?hgid1 $?gph1)
	?HG2 <- (Hgroup_id-group_elements ?hgid2 $?gph2)
	;?P <- (proposed_anchor_ids $?r)
	(test (and (member$ ?a $?gpe) (member$ $?y1 $?gph1) (member$ $?y2 $?gph2)))
	=>
	(retract ?e)
	(assert (remove ?a $?y1))
	(assert (remove ?a $?y2))
	(printout t "Rule check_anchor_multiple_hindi_group_match " ?a " " $?y1 " " $?y2 crlf)
	(assert (proposed_groups ?egid ?hgid1))
	(assert (proposed_groups ?egid ?hgid2))
	(assert (final_set-eid-hid ?a $?y1 $?y2)))
	;(assert (new_proposed_anchors_ids (replace$ $?r (member$ ?a $?n) (member$ ?a $?n) (create$ $?y1 $?y2)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Once all the reliable anchors(starting anchors) are fixed, we shift the focus to resolving the ambiguous potential anchors.
;One method of resolving the potential anchors is that we look back at the proposed_groups information which we get from the
;setting of anchors(starting anchors). Now we try to check whether one of the suggestions for the potential matches the group
;information that has already been proposed. Let us suppose that we have an information that group 'A' of English gets aligned
;with group 'P' of Hindi, and the entries present for the potential anchor are X<<maybe>>Y or X<<maybe>>Z. Now if X belongs to
;group A and Y belongs to P, we can in a way conclude that X should definitely be aligned to Y, and vice-versa if Z belongs to
;P. 
;In the above example of sentence 2.77, the words 'Kumaon Himalayas' are present in one single group in both English and Hindi.
;The word 'Kumaon'-->'कुमाँऊ' is being proposed as the final anchor. Now because the word 'Himalaya' exists twice in the sentence
;there is an ambiguity and hence it needs to be resolved. Now because we know where 'Kumaon' maps, we know where the group of
;'Kumaon' should match to, i.e. English group 7 to Hindi group 7. As we have two possibilities here that 'Himalayas' suggests 
;aligning of English group 7 to Hindi group 5 and English group 7 to Hindi group 7, we select the one which suggests English
;group 7 being aligned to Hindi group 7.

(defrule check_potential
	?p1 <- (anchor_type-english_id-hindi_id potential ?x $?y)
	?g1 <- (proposed_groups ?p ?q)
	?g2 <- (Egroup_id-group_elements ?p $?pgroup)
	?g3 <- (Hgroup_id-group_elements ?q $?qgroup)
	;?P <- (proposed_anchors_ids $?r)
	(test (and (member$ ?x $?pgroup) (member$ $?y $?qgroup)))
	=>
	(retract ?p1)
	(printout t "Rule check_potential fired for " ?x " " $?y crlf)
	(assert (remove ?x $?y))
	(assert (final_set-eid-hid ?x $?y)))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?x $?pgroup) (member$ ?x $?pgroup) $?y))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Now the suggestions present in the potential may not always point towards alignment of type 'one to one'. They may point 
;that one group of the English may align to multiple Hindi groups, i.e. relation of type 'one to many'. In such a case the
;code tries to find out a suggestion of form P-->Q and P-->R and if we have an information from our starting anchors that
;the English group P either aligns with Q or it aligns with R, meaning to say that there is an overlapping of the groups.
;Because we have a partial match with our proposed group information, we assert the partially matching suggestion as a 
;proposed anchor, and remove the other ambiguous entries present for the English ID.

(defrule check_potential_multiple_hindi_groups
	?p1 <- (anchor_type-english_id-hindi_id potential ?x $?y1 $?y2)
	?g1 <- (proposed_groups ?p ?q)
	?g2 <- (Egroup_id-group_elements ?p $?pgroup)
	?g3 <- (Hgroup_id-group_elements ?q $?qgroup)
	?g4 <- (Hgroup_id-group_elements ?q1 $?qgroup1)
	(test (and (member$ ?x $?pgroup) (member$ $?y1 $?qgroup) (member$ $?y2 $?qgroup1)))
	=>
	(retract ?p1)
	(printout t "Rule check_potential_multiple_hindi_groups fired for " ?x " " $?y1 " " $?y2 crlf)
	(assert (remove ?x $?y1))
	(assert (remove ?x $?y2))
	(assert (final_set-eid-hid ?x $?y1 $?y2))
	(assert (proposed_groups ?p ?q1)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Everytime we propose an anchor as a final ID, we also assert the same pair of IDs as (remove ?a $?b). This is done to
;help us remove any ambiguity, if present. For example if X-->Y is being proposed as a final ID, then we do a check that
;neither X nor Y are being repeated anywhere in the other facts. If there exists a fact which contains either X or Y, the
;fact is retracted. 
;To implement this the following rule was written which retracts all the repeating facts for 'X' or '?x', after it was
;proposed to be a final anchor. It looks for any fact in which X is repeated and if found retracts the fact.

(defrule remove_eng_part
	(declare (salience 300))
	?r <- (remove ?x $?y)
	?pot <- (anchor_type-english_id-hindi_id potential ?x $?)
	=>
	(printout t "Rule remove_eng_part fired for " ?x crlf)
	(retract ?pot))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Just like the previous rule, the following rule tries to find the ambiguous entries and remove such facts, difference being
;that this rule tries to remove ambiguous facts based on Hindi IDs. As in the data structure the Hindi ID part is a multislot
;value, we consider the ID which was fixed to be $?y. Now the code tries to look for any occurance of $?y as a whole or even
;partial occurance of the Hindi ID, for example, if the ID which got fixed was X-->Y,Z, the value $?y represent Y and Z and
;if there is a repeatation of these IDs = {Y, Z, (Y,Z)}, the code removes such facts.

(defrule remove_hin_part
	(declare (salience 300))
	?r <- (remove ?x $?y)
	?pot <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	(test (and (or (member$ $?y1 $?y) (member$ $?y $?y1) (eq $?y $?y1)) (neq (length$ $?y) 0)))
	=>
	(printout t "Rule remove_hin_part fired for " $?y crlf)
	(assert (removed ?a))
	(retract ?pot))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;In the above rule I also keep a track of which English IDs get retracted. This is required because we don't want to
;lose complete information about any English ID. For example if we have 1-->5 and 2-->5 as facts of type potential, and 1-->5
;is being suggested as a final anchor, the code will try to look for such facts 1 and 5 are present and remove them. So when
;it removes 2-->5 (because 5 is present in this fact), 2 will also get removed and as there is no other fact present for 2,
;we miss out on the information that English ID 2 is of type unknown anchor. If information about any ID is being lost in 
;such a form, the generation of N1 layer fails because of having less information than what is actually needed to generate the
;layer. Each column in the final.html represents an English ID and in cases where we lose information about English IDs, there
;is a mismatch between the number of columns required and the output provided.

;To overcome this, we already store information about the English ID being retracted in the fact (removed ?a), and using it
;the following rule finds out whether any information about the ID is present in the anchor facts or not. If no such fact 
;exists where the English ID 2 (refer previous paragraph) is present, it means that there is a case of information loss and
;so the code asserts a new fact that keeps the information that the English ID 2 is of type unknown anchor.

(defrule check_removed_english
	?r <- (removed ?a)
	(not (anchor_type-english_id-hindi_id ? ?a $?))
	=>
	(printout t "Rule check_removed_english fired for " ?a " asserting it as unknown anchor." crlf)
	(assert (anchor_type-english_id-hindi_id unknown ?a 0))
	(retract ?r))

;Similarly if it is found that there is some fact present for the English ID 2, we conclude that removing the Hindi ID 5 did
;not cause any loss of information about the English ID and so the code retract the (removed ?a) fact.

(defrule check_removed_english_helper
	?r <- (removed ?a)
	(anchor_type-english_id-hindi_id ? ?a $?)
	=>
	(printout t "Rule check_removed_english_helper fired for " ?a crlf)
	(retract ?r))
	
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Once all the repeating facts for the entry (remove ?x $?y) are removed, meaning to say when all facts containing either ?x
;or $?y values are removed, we do not need the fact (remove ?x $?y) anymore and so this rule retracts the 'remove' facts.

(defrule remove_remove-fact
	(declare (salience 300))
	?r <- (remove ?x $?y)
	(not (or (anchor_type-english_id-hindi_id potential ?x $?) (anchor_type-english_id-hindi_id potential ? $?y)))
	=>
	(printout t "Rule remove_remove-fact fired for " ?x " " $?y crlf)
	(retract ?r))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;For cases in which we have the information that group P of English is aligned with group Q of Hindi, and we have a fact
;which does not suggest that group P aligns with group Q, the rule checks whether it is being aligned with groups Q+1 or
;Q-1 of Hindi. If there is an entry present which suggests that it may be mapped to Q+1 or Q-1, the vicinity of original
;information that P aligns with Q, we assert it as a final ID by the vicinity rule. On its execution we also store the 
;information that P-->Q+1 or P-->Q-1, based on the scenario.

(defrule check_vicinity_potential_hindi_side
	?p1 <- (anchor_type-english_id-hindi_id potential ?x $?y)
	;?e <- (english_group_ids_mfs $?n)
	?g1 <- (proposed_groups ?p ?q)
	?g2 <- (Egroup_id-group_elements ?p $?pgroup)
	?g3 <- (Hgroup_id-group_elements ?q $?qgroup)
	?g6 <- (Hgroup_id-group_elements ?q1 $?hgroup1)
	?g7 <- (Hgroup_id-group_elements ?q2 $?hgroup2)
	?P <- (proposed_anchor_ids $?r)
	(test (and (= ?q1 (+ ?q 1)) (= ?q2 (- ?q 1)) (member$ ?x $?pgroup) (or (member$ $?y $?hgroup1) (member$ $?y $?hgroup2))))
	=>
	(printout t "Rule check_vicinity_potential_hindi_side fired for " ?x " " $?y crlf)
	(assert (final_set-eid-hid ?x $?y))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?x $?n) (member$ ?x $?n) $?y)))
	(if (member$ $?y $?hgroup1)
		then
		(assert (proposed_groups ?p (+ ?q 1)))
		else
		(assert (proposed_groups ?p (- ?q 1))))
	(assert (remove ?x $?y))
	(retract ?p1))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;This rule will not fire with the present data structure. I wrote this rule with the thought that on changing the data
;structure to have both English ID corresponding and Hindi ID as a multi slot value (many to many relation), there will be
;cases where this rule will be used.

;For cases in which we have the information that group P of English is aligned with group Q of Hindi, and we have a fact
;which does not suggest that group P aligns with group Q, the rule checks whether group Q is being aligned with groups P+1
;or group P-1 of English. If there is an entry present which suggests that Q may be mapped to P+1 or P-1, the vicinity of
;original information that P aligns with Q, we assert it as a final ID by the vicinity rule.

(defrule check_vicinity_potential_english_side
	?a1 <- (anchor_type-english_id-hindi_id potential ?x $?y)
	;?e <- (english_group_ids_mfs $?n)
	?g1 <- (proposed_groups ?p ?q)
	?g2 <- (Egroup_id-group_elements ?p $?pgroup)
	?g3 <- (Hgroup_id-group_elements ?q $?qgroup)
	?g6 <- (Egroup_id-group_elements ?p1 $?egroup1)
	?g7 <- (Egroup_id-group_elements ?p2 $?egroup2)
	;?P <- (proposed_anchor_ids $?r)
	(test (and (= ?p1 (+ ?p 1)) (= ?p2 (- ?p 1)) (member$ ?y $?qgroup) (or (member$ ?x $?egroup1) (member$ ?x $?egroup2))))
	=>
	(printout t "Rule check_vicinity_potential_english_side fired for " ?x " " $?y crlf)
	(assert (final_set-eid-hid ?x $?y))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?x $?n) (member$ ?x $?n) $?y)))
	(if (member$ ?x $?egroup1)
		then
		(assert (proposed_groups ?p1 ?q))
		else
		(assert (proposed_groups ?p2 ?q)))
	(assert (remove ?x $?y))
	(retract ?a1))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Let us consider such a case where the information present in potential about IDs is X-->Y and X-->Y,Z. For us humans it is
;clear that there are two entries but both point to the same place in the Hindi side. So for such cases this rule was written
;and what it does is pick up the larger of such entries, i.e. entry containing more information. So in such a case the entry
;X-->Y,Z will be kept and the entry X-->Y will be removed.

;Here when we consider the example 2.77, we find that the word 'Himalayas' is present twice and we also see that there is an
;ambiguity created by intersecting entries (of the form X-->Y, 5_Himalayas-->8_himAlaya) for an already present entry (of the
;form X-->Y,Z, 5_Himalayas-->8_himAlaya 9_ke). In such a case the entry having more information is kept and the other retracted.

(defrule check_intersecting_potential
	(declare (salience 300))
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?y2)
	(test (and (neq ?e1 ?e2) (or (member$ $?y2 $?y1) (member$ $?y1 $?y2))))
	=>
	(if (> (length $?y1) (length $?y2))
		then
		(retract ?e2)
		(printout t "Rule check_intersecting_potential fired for " ?a " " $?y2 crlf)
		else
		(retract ?e1)
		(printout t "Rule check_intersecting_potential fired for " ?a " " $?y1 crlf)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Let us assume that after the above rule fires and removes the entry X-->Y, we are now just left with X-->Y,Z with no ambiguity
;present anywhere else for X, Y, Z. For such cases where after some rules being fired, only a single entry is left in the
;potential for a particular English ID(in this case X), I call it as the case of having a unique potential and because the
;potential entry is single and there is no ambiguity, I assert it as a final anchor. It should be noted that even though this
;rule works, sometimes it fires at places where it should not fire. The condition needs to be much more robust. So do check if
;this rule causes some errors. I'll be replacing it with a better and robust condition soon enough.

;From the above rule's example the things we can observe is, intersecting entries are resolved by the intersecting rule after
;which the Kumaon being a starting anchor helps in resolving the Himalayas present in Kumaon Himalayas. This in turn removes the
;ambiguous entries present for 'Himalayas' in the 'part of the Himalayas lying' and now only a single entry is left as potential
;for which this rule will fire and assert it as a final anchor, it will also store the information about the group.

(defrule check_unique_potential
	(declare (salience -500))
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $?)
	?e3 <- (anchor_type-english_id-hindi_id potential ? $?y1)
	;?E <- (english_group_ids_mfs $?n)
	?EG <- (Egroup_id-group_elements ?egid $?gpe)
	?HG <- (Hgroup_id-group_elements ?hgid $?gph)
	;?P <- (proposed_anchor_ids $?r) 
	(test (and (eq ?e1 ?e2 ?e3) (member$ ?a $?gpe) (member$ $?y1 $?gph) (neq (length$ $?y1) 0)))
	=>
	(retract ?e1)
	(assert (remove ?a $?y1))
	(printout t "Rule check_unique_potential fired for " ?a " " $?y1 crlf)
	(assert (proposed_groups ?egid ?hgid))
	(assert (final_set-eid-hid ?a $?y1)))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?a $?n) (member$ ?a $?n) $?y1))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;Adding to the above rule, if X-->Y,Z is the information present with us and Y and Z belong to different groups of Hindi,
;this rule asserts that they should be aligned and corresponding group alignment information is also asserted.

(defrule check_unique_potential_multiple_hindi_groups
	(declare (salience -500))
	?e1 <- (anchor_type-english_id-hindi_id potential ?a $?y1 $?y2)
	?e2 <- (anchor_type-english_id-hindi_id potential ?a $? $?)
	?e3 <- (anchor_type-english_id-hindi_id potential ? $?y1 $?y2)
	;?E <- (english_group_ids_mfs $?n)
	?EG <- (Egroup_id-group_elements ?egid $?gpe)
	?HG1 <- (Hgroup_id-group_elements ?hgid1 $?gph1)
	?HG2 <- (Hgroup_id-group_elements ?hgid2 $?gph2)
	;?P <- (proposed_anchor_ids $?r) 
	(test (and (eq ?e1 ?e2 ?e3) (member$ ?a $?gpe) (member$ $?y2 $?gph2) (member$ $?y1 $?gph1) (neq (length$ $?y1) 0) (neq (length$ $?y2) 0)))
	=>
	(retract ?e1)
	(assert (remove ?a $?y1))
	(assert (remove ?a $?y2))
	(printout t "Rule check_unique_potential fired for " ?a " " $?y1 crlf)
	(assert (proposed_groups ?egid ?hgid1))
	(assert (proposed_groups ?egid ?hgid2))
	(assert (final_set-eid-hid ?a $?y1 $?y2)))
	;(assert (new_proposed_anchor_ids (replace$ $?r (member$ ?a $?n) (member$ ?a $?n) $?y1))))
