
# coding: utf-8

# In[81]:


import csv,sys, os
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
eng_file_name = 'ai1E'
sent_no='2.28'
#eng_file_name = sys.argv[1]
#sent_no = sys.argv[2]
sent_dir = tmp_path + eng_file_name + "_tmp/" + sent_no
def reading_all_resources():
    all_data=[]
    with open(sent_dir+'/All_Resources.csv','rt')as f: ####PATH TO BE CHANGED
        data = csv.reader(f)
        rows=list(data)
    return rows
all_resources=reading_all_resources()
def resources_for_deciding_potential_anchor():
    anu_exact_match=[]
    nandani_dict=[]
    tech_dict=[]
    roja_transliterate=[]
    kishori_WSD_modulo=[]
    anu_exact_wo_vib=all_resources[1]
    nandani_dict=all_resources[5]
    tech_dict=all_resources[6]
    roja_transliterate=all_resources[7]
    kishori_WSD_modulo=all_resources[8]
    return anu_exact_wo_vib,nandani_dict,tech_dict,roja_transliterate,kishori_WSD_modulo

anu_exact_wo_vib,nandani_dict,tech_dict,roja_transliterate,kishori_WSD_modulo=resources_for_deciding_potential_anchor()
print(anu_exact_wo_vib,nandani_dict,tech_dict,roja_transliterate,kishori_WSD_modulo)

###########################################POTENTIAL_ANCHOR########################################################

def setting_potential_anchor():
    potential_anchor = ['0'] * len(anu_exact_wo_vib)
    potential_anchor[0]="Potential Anchor:"
    for i in range(len(anu_exact_wo_vib)):
        if i!=0 :
            if str(anu_exact_wo_vib[i]) != "0" and "(" not in anu_exact_wo_vib[i] and ")" not in anu_exact_wo_vib[i]:
                if str(potential_anchor[i]) != "0" :
                    temp=potential_anchor[i]
                    potential_anchor[i]=temp+"/"+anu_exact_wo_vib[i]
                elif "(" in anu_exact_wo_vib[i] or ")" in anu_exact_wo_vib[i] :
                    potential_anchor[i]=anu_exact_wo_vib[i]
            else: 
                potential_anchor[i]=anu_exact_wo_vib[i]
            if str(nandani_dict[i]) !=  "0" and "(" not in nandani_dict[i] and ")" not in nandani_dict[i] :
                if str(potential_anchor[i]) != "0" :
                    if anu_exact_match[i] not in potential_anchor[i].split("/"):
                        temp=potential_anchor[i]
                        potential_anchor[i]=temp+"/"+nandani_dict[i]
                else :
                    potential_anchor[i]=nandani_dict[i]
            elif "(" in nandani_dict[i] or ")" in nandani_dict[i]:
                potential_anchor[i]=nandani_dict[i]
            if str(tech_dict[i]) !=  "0" and "(" not in tech_dict[i] and ")" not in tech_dict[i] :
                if str(potential_anchor[i]) != "0" :
                    temp=potential_anchor[i]
                    potential_anchor[i]=temp+"/"+tech_dict[i]
                else :
                    potential_anchor[i]=tech_dict[i]
            elif "(" in tech_dict[i] or ")" in tech_dict[i] :
                potential_anchor[i]=tech_dict[i]
            if str(roja_transliterate[i]) !=  "0"  and "(" not in roja_transliterate[i] and ")" not in roja_transliterate[i]:
                if str(potential_anchor[i]) != "0" :
                    if roja_transliterate[i] not in potential_anchor[i].split("/"):
                        temp=potential_anchor[i]
                        potential_anchor[i]=temp+"/"+roja_transliterate[i]
                else :
                    potential_anchor[i]=roja_transliterate[i]
            elif "(" in roja_transliterate[i] or ")" in roja_transliterate[i] :
                potential_anchor[i]=roja_transliterate[i]
            if str(kishori_WSD_modulo[i]) !=  "0" and "(" not in kishori_WSD_modulo[i] and ")" not in kishori_WSD_modulo[i]:
                if str(potential_anchor[i]) != "0" :
                    if kishori_WSD_modulo[i] not in potential_anchor[i].split("/"):
                        temp=potential_anchor[i]
                        potential_anchor[i]=temp+"/"+kishori_WSD_modulo[i]
                else :
                    potential_anchor[i]=kishori_WSD_modulo[i]
            elif "(" in kishori_WSD_modulo[i] or ")" in kishori_WSD_modulo[i] :
                potential_anchor[i]=kishori_WSD_modulo[i]
    return potential_anchor
potential_anchor = setting_potential_anchor()
print(potential_anchor)


def setting_starting_anchor():
    starting_anchor = ['0'] * len(anu_exact_wo_vib)
    starting_anchor[0] = "Starting Anchor:"

    for index,wordid in enumerate(potential_anchor) :
        if index != 0 :
            if "/" not in wordid :
                flag=0
                for temp in potential_anchor[index+1:] :
                     if "/" in temp:
                        temp=temp.split("/")
                        if wordid in temp :
                            flag = 1
                            break
                if flag == 0 :
                    starting_anchor[index] = potential_anchor[index]
            else :
                starting_anchor[index]='0'
                    
    return starting_anchor  
starting_anchor = setting_starting_anchor()
print(starting_anchor)
with open(sent_dir+'/All_Resources.csv','a')as f1:
        dwrite = csv.writer(f1)   
        dwrite.writerow(potential_anchor)
        dwrite.writerow(starting_anchor)
        


# In[73]:




