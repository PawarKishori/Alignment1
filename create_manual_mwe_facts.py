import sys
mwe_list=[]
#sent_dir_path="/home/user/forked/tmp_anu_dir/tmp/mwe_E_tmp/2.1/"
#corpus_hindi_file="/home/user/forked/alignment_manju/"
for line in open("Hindi_sent_mwes_underscored.dat","r"):
        mwe_list=[word for word in line.strip().split() if "_" in word]
	if len(mwe_list)==0:
		print("manual_mwe_facts.dat is empty")

#Change manual to H_wid-word
with open("manual_word.dat","r") as g:
 	data = g.read()

manual_mwe_words=[]
manual_word_facts=[i.strip()[1:-1].split(" ") for i in data.split("\n") if i.strip()]
new_list=[]
for mwe in mwe_list:
    	mwe=mwe.split("_")
    	possible_mwe_beginnings=[i for i in range(len(manual_word_facts)) if manual_word_facts[i][2]==mwe[0]]
	for i in possible_mwe_beginnings:
		if i+len(mwe)<=len(manual_word_facts):
 	               if [j[2] for j in manual_word_facts[i:i+len(mwe)]] == mwe:
				new_list.append([(j[1],j[2]) for j in manual_word_facts[i:i+len(mwe)]]) 
f1=open("manual_mwe_facts.dat","w")
#print("Creating manual_mwe_facts.dat for the sentence")
for i in new_list:
	print (i)
  	#print("(manual_id-mwe\t"+i[0][0]+"\t"+ "_".join([j[1] for j in i])+")\n")
  	f1.write("(manual_id-mwe\t"+" ".join([j[0] for j in i])+"\t"+ "_".join([j[1] for j in i])+")\n")
f1.close()


