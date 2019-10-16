#!/usr/bin/env python
# coding: utf-8

# In[101]:


import os,sys,csv
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
# eng_file_name="ai1E"
eng_file_name=sys.argv[1]
# sent_no="2.2"
sent_no = sys.argv[2]
sent_dir = tmp_path+eng_file_name+"_tmp/"+sent_no
csv_file = sent_dir+"/All_Resources.csv"
anchor_fact_file = sent_dir+"/Anchor_Facts.dat"
# csv_file="/home/jagrati/tmp_anu_dir/tmp/ai1E_tmp/2.2/All_Resources.csv"

def reading_csv():
    with open(csv_file,'rt')as f: 
        data = csv.reader(f)
        rows=list(data)
        probable=rows[-1][1:]
        starting=rows[-2][1:]
        potential=rows[-3][1:]
        
    return probable,starting,potential

def generate_starting_anchor():
    starting_facts = []
    for i in range(len(starting)) :
        if str(starting[i]) != str('0') :
            if  '(' not in starting[i] and ')' not in starting[i]:
                print("(anchor_type-english_id-hindi_id starting "+str(i+1)+" "+starting[i]+")")
                singleword_fact="(anchor_type-english_id-hindi_id starting "+str(i+1)+" "+starting[i]+")\n"
                starting_facts.append(singleword_fact)
            else :
                if '(' in starting[i]:
                    for j in range(i+1,len(starting)) :
                        if ')' in starting[j] :
                            print("(anchor_type-english_ids-mfs-hindi_ids starting "+str(i+1)+" "+str(j+1)+" mfs "+starting[j].strip(")"),")")
                            multiword_fact="(anchor_type-english_ids-mfs-hindi_ids starting "+str(i+1)+" "+str(j+1)+" mfs "+starting[j].strip(")")+")\n"
                            starting_facts.append(multiword_fact)
    return starting_facts

def generate_potential_anchor():
    potential_facts = []
    for i in range(len(potential)) :
        if str(potential[i]) != str('0') :
            if  '(' not in potential[i] and ')' not in potential[i]:
                hids=i.split("/")
                for h in hids:
                    print("(anchor_type-english_id-hindi_id potential "+str(i+1)+" "+h+")\n")
                    potential_fact="(anchor_type-english_id-hindi_id potential "+str(i+1)+" "+h+")\n"
                    potential_facts.append(potential_fact)
            #else not getting handled at the moment as there aren't enough cases
    return potential_facts

def generate_probable_anchor():
    probable_facts = []
    for i in range(len(probable)) :
        if str(probable[i]) != str('0') :
            if  '(' not in probable[i] and ')' not in probable[i]:
                hids=probable[i].split("/")
                for h in hids:
                    print("(anchor_type-english_id-hindi_id probable "+str(i+1)+" "+h+")\n")
                    probable_fact="(anchor_type-english_id-hindi_id probable "+str(i+1)+" "+h+")\n"
                    probable_facts.append(probable_fact)
            #else not getting handled at the moment as there aren't enough cases
    return probable_facts

def generate_unknown_anchor():
    unknown_facts= []
    for count, (i,j,k) in enumerate(zip(starting,potential,probable)):
        if str(i) == str(j) == str(k) == str('0') :
            print("(anchor_type-english_id-hindi_id unknown "+str(count+1)+" 0 )\n")
            unknown_fact="(anchor_type-english_id-hindi_id unknown "+str(count+1)+" 0 )\n"
            unknown_facts.append(unknown_fact)
        #else not getting handled at the moment as there aren't enough cases
    return unknown_facts
 
def writing_facts():   
    starting_facts=generate_starting_anchor()
    potential_facts=generate_potential_anchor()
    probable_facts=generate_probable_anchor()
    unknown_facts=generate_unknown_anchor()
    
    with open(anchor_fact_file,'w')as out_file:
        for s in starting_facts:
            out_file.write(str(s))
        for p in potential_facts:
            out_file.write(str(p))
        for r in probable_facts:
            out_file.write(str(r))
        for u in unknown_facts:
            out_file.write(str(u))
probable,starting,potential=reading_csv()
print(starting)
print(potential)
print(probable)
writing_facts()


# In[ ]:





# In[ ]:




