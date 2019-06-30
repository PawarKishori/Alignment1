import sys
mwe_list=[]
#sent_dir_path="/home/user/forked/tmp_anu_dir/tmp/mwe_E_tmp/2.1/"
#corpus_hindi_file="/home/user/forked/alignment_manju/"
#with open("H_wid-word.dat","r") as g:
with open("H_wordid-word_mapping.dat","r") as g:
	data = g.read()
for line in open("Hindi_sent_mwes_underscored.dat","r"):
        mwe_list=[word for word in line.strip().split() if "_" in word]
	if len(mwe_list)==0:
		print("No multiword expressions in this hindi sentence.")
	else:
		f1=open("manual_mwe_facts.dat","w")
		manual_mwe_words=[]
		manual_word_facts=[i.strip()[1:-1].split(" ") for i in data.split("\n") if i.strip()]
		new_list=[]
		#print(list(set(mwe_list)))
		for mwe in list(set(mwe_list)):
    			mwe=mwe.split("_")
			sent_words=["".join(l).split('\t')[2] for l in manual_word_facts]
			mwe_occurrence_indices=[i for i,val in enumerate(sent_words) if sent_words[i:i+len(mwe)]==mwe]	
    			print(mwe_occurrence_indices)
			for index in mwe_occurrence_indices:
  				print("(manual_id-mwe\t"+" ".join([str(i) for i in range(index+1,index+1+len(mwe))])+"\t"+" ".join(mwe)+")\n")
  				f1.write("(manual_id-mwe\t"+" ".join([str(i) for i in range(index+1,index+1+len(mwe))])+"\t"+"_".join(mwe)+")\n")
		f1.close()
