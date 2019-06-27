file_path = '' #/home/akanksha/Alignment/tam_local/cl_english_100_detok_tmp/2.52/'
with open(file_path+"revised_manual_local_word_group.dat","r") as g:
    data = g.read().strip().split("\n")
with open(file_path+"H_sentence","r") as g:
    sentence = g.read().strip()
data_enhanced = list(map(lambda x:x.split("\t"),data))
verb_entry = {int(j[-1].strip(")").split()[-1]):(j[1:]) for j in data_enhanced if j[-1]!="0)"}
fact_ = []
j=0
word_list = sentence.split()
with open(file_path+"finite_clause.dat","w") as g:
    for loc, i in enumerate(verb_entry):
            clause = " ".join(word_list[j:i])
            ids = " ".join(list(map(lambda x: str(x+1), range(int(j),int(i)))))
            fact = "(clause (cl_id {}) (cl_words {}) (cl_member_ids {}) (finite_verb_grp {}) (finite_verb_grp_ids {}) (finite_verb_root {}) (finite_verb_root_id {}) (finite_verb_tam {}))".format(loc, clause, ids, verb_entry[i][3], verb_entry[i][4].strip(")"), verb_entry[i][1], verb_entry[i][0], verb_entry[i][2])
            fact_.append(fact)
            g.write(fact)
            g.write("\n")
            j=i
