import csv,sys, os
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'

# eng_file_name = 'ai1E'
# sent_no='2.78'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
sent_dir = tmp_path + eng_file_name + "_tmp/" + sent_no
log_file = sent_dir + "Deciding_Anchor.log"
##############################################CREATING LOG OBJECT##################################################
if os.path.exists(log_file):
    os.remove(log_file)
log = open(log_file,'a')
######################################################################################################################
def reading_all_resources():
    try :
        with open(sent_dir+'/All_Resources.csv','rt')as f: ####PATH TO BE CHANGED
            data = csv.reader(f)
            rows=list(data)
    except :
        print("All_Resources.csv is Missing")
        log.write("In "+sent_no+" All_resources.csv is missing")
        sys.exit(0)
        
    return rows
all_resources=reading_all_resources()
def resources_for_deciding_potential_anchor():
    anu_exact_match=[]
    nandani_dict=[]
    tech_dict=[]
    roja_transliterate=[]
    kishori_WSD_modulo=[]
    anu_exact_wo_vib=all_resources[2]
    nandani_dict=all_resources[6]
    tech_dict=all_resources[7]
    roja_transliterate=all_resources[8]
    kishori_WSD_modulo=all_resources[9]
    return anu_exact_wo_vib,nandani_dict,tech_dict,roja_transliterate,kishori_WSD_modulo

anu_exact_wo_vib,nandani_dict,tech_dict,roja_transliterate,kishori_WSD_modulo=resources_for_deciding_potential_anchor()
#print(anu_exact_wo_vib,nandani_dict,tech_dict,roja_transliterate,kishori_WSD_modulo)


def resources_for_deciding_probable_potential_anchor():
    K_exact = []
    K_partial = []
    K_root = []
    K_dict = []
    K_exact = all_resources[1]
    K_partial = all_resources[3]
    K_root = all_resources[4]
    K_dict = all_resources[5]
    return K_exact,K_partial,K_root, K_dict
K_exact,K_partial,K_root, K_dict=resources_for_deciding_probable_potential_anchor()
#print(K_exact)
#print(K_partial)
#print(K_root)
#print(K_dict)
###########################################POTENTIAL_ANCHOR########################################################

def setting_potential_anchor():
    potential_anchor = ['0'] * len(anu_exact_wo_vib)
    potential_anchor[0]="Potential Anchor:"
    for i in range(len(anu_exact_wo_vib)):
        if i!=0 :
##########################################ANU_EXACT_WO_VIB#########################################################
            if "(" not in potential_anchor[i] and ")" not in potential_anchor[i] :
                if str(anu_exact_wo_vib[i]) != "0" and "(" not in anu_exact_wo_vib[i] and ")" not in anu_exact_wo_vib[i] :
                    if str(potential_anchor[i]) != "0" :
                        if anu_exact_wo_vib[i] not in potential_anchor[i].split("/"):
                            temp=potential_anchor[i]
                            potential_anchor[i]=temp+"/"+anu_exact_wo_vib[i]
                    else :
                        potential_anchor[i]=anu_exact_wo_vib[i]
                elif "(" in anu_exact_wo_vib[i] or ")" in anu_exact_wo_vib[i] :
                    potential_anchor[i]=anu_exact_wo_vib[i]
#######################################NANDANI_DICT################################################################
            if "(" not in potential_anchor[i] and ")" not in potential_anchor[i] :
                if str(nandani_dict[i]) !=  "0" and "(" not in nandani_dict[i] and ")" not in nandani_dict[i] :
                    if str(potential_anchor[i]) != "0" :
                        if nandani_dict[i] not in potential_anchor[i].split("/"):
                            temp=potential_anchor[i]
                            potential_anchor[i]=temp+"/"+nandani_dict[i]
                    else :
                        potential_anchor[i]=nandani_dict[i]
                elif "(" in nandani_dict[i] or ")" in nandani_dict[i]:
                    potential_anchor[i]=nandani_dict[i]
#####################################################TECH_DICT#####################################################  
            if "(" not in potential_anchor[i] and ")" not in potential_anchor[i] :
                if str(tech_dict[i]) !=  "0" and "(" not in tech_dict[i] and ")" not in tech_dict[i] :
                    if str(potential_anchor[i]) != "0" :
                        if tech_dict[i] not in potential_anchor[i].split("/"):
                            temp=potential_anchor[i]
                            potential_anchor[i]=temp+"/"+tech_dict[i]
                    else :
                        potential_anchor[i]=tech_dict[i]
                elif "(" in tech_dict[i] or ")" in tech_dict[i] :
                    potential_anchor[i]=tech_dict[i]
###############################################ROJA TRANSLITERATION################################################
            if "(" not in potential_anchor[i] and ")" not in potential_anchor[i] :
                if str(roja_transliterate[i]) !=  "0"  and "(" not in roja_transliterate[i] and ")" not in roja_transliterate[i]:
                    if str(potential_anchor[i]) != "0" :
                        if roja_transliterate[i] not in potential_anchor[i].split("/"):
                            temp=potential_anchor[i]
                            potential_anchor[i]=temp+"/"+roja_transliterate[i]
                    else :
                        potential_anchor[i]=roja_transliterate[i]
                elif "(" in roja_transliterate[i] or ")" in roja_transliterate[i] :
                    potential_anchor[i]=roja_transliterate[i]
###########################################KISHORI_WSD_MODULO######################################################
            if "(" not in potential_anchor[i] and ")" not in potential_anchor[i] :
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
################################################################################################################

potential_anchor = setting_potential_anchor()
# print(potential_anchor)

#######################################STARTING_ANCHOR#############################################################
def setting_starting_anchor():
    starting_anchor = ['0'] * len(anu_exact_wo_vib)
    starting_anchor[0] = "Starting Anchor:"

    for index,wordid in enumerate(potential_anchor) :
        if index != 0 :
            if "/" not in wordid :
                flag=0
                for temp in (potential_anchor[:index] + potential_anchor[index+1:]) :
                    if "/" in temp:
                        temp=temp.split("/")
                        if wordid in temp :
                            flag = 1
                            break
                    else :
                        if wordid == temp :
                            flag = 1
                            break
                if flag == 0 :
                    starting_anchor[index] = potential_anchor[index]
            else :
                starting_anchor[index]='0'
                   
    return starting_anchor  
starting_anchor = setting_starting_anchor()
#print(starting_anchor)

################################PROBABLE_POTENTIAL_ANCHOR##########################################################
def probable_potential_anchor():
    prob_potential_anchor = ['0'] * len(K_exact)
    prob_potential_anchor[0]="Probable Potential Anchor:"
    for i in range(len(K_exact)):
        if i!=0 :
#############################################K_EXACT##############################################################
            if str(K_exact[i]) != "0" and "(" not in K_exact[i] and ")" not in K_exact[i] and "/" not in K_exact[i] :
                if str(prob_potential_anchor[i]) != "0" :
                    if K_exact[i] not in prob_potential_anchor[i].split("/"):
                        temp=prob_potential_anchor[i]
                        prob_potential_anchor[i]=temp+"/"+K_Exact[i]
                else :
                    prob_potential_anchor[i]=K_exact[i]
            elif "(" in K_exact[i] or ")" in K_exact[i] :
                prob_potential_anchor[i]=K_exact[i]
            elif "/" in K_exact[i] :
                K_exact[i]=K_exact[i].split("/")
                for k in K_exact[i] :
                    if k not in prob_potential_anchor[i].split("/"):
                        temp=prob_potential_anchor[i]
                        if temp == '0':
                            prob_potential_anchor[i]=k
                        else:
                            prob_potential_anchor[i]=temp+"/"+k
##############################################K_PARTIAL###########################################################
            if str(K_partial[i]) != "0" and "(" not in K_partial[i] and ")" not in K_partial[i] and "/" not in K_partial[i] :
                if str(prob_potential_anchor[i]) != "0" :
                    if K_partial[i] not in prob_potential_anchor[i].split("/"):
                        temp=prob_potential_anchor[i]
                        prob_potential_anchor[i]=temp+"/"+K_partial[i]
                else :
                    prob_potential_anchor[i]=K_partial[i]

            elif "(" in K_partial[i] or ")" in K_partial[i] :
                prob_potential_anchor[i]=K_partial[i]
            elif "/" in K_partial[i] :
                K_partial[i]=K_partial[i].split("/")
                for k in K_partial[i] :
                    if k not in prob_potential_anchor[i].split("/"):
                        temp=prob_potential_anchor[i]
                        if temp == '0':
                            prob_potential_anchor[i]=k
                        else:
                            prob_potential_anchor[i]=temp+"/"+k
##############################################K_ROOT##############################################################                
            if str(K_root[i]) != "0" and "(" not in K_root[i] and ")" not in K_root[i] and "/" not in K_root[i] :
                if str(prob_potential_anchor[i]) != "0" :
                    if K_root[i] not in prob_potential_anchor[i].split("/"):
                        temp=prob_potential_anchor[i]
                        prob_potential_anchor[i]=temp+"/"+K_root[i]
                else :
                    prob_potential_anchor[i]=K_root[i]

            elif "(" in K_root[i] or ")" in K_root[i] :
                prob_potential_anchor[i]=K_root[i]
            elif "/" in K_root[i] :
                K_root[i]=K_root[i].split("/")
                for k in K_root[i] :
                    if k not in prob_potential_anchor[i].split("/"):
                        temp=prob_potential_anchor[i]
                        if temp == '0':
                            prob_potential_anchor[i]=k
                        else:
                            prob_potential_anchor[i]=temp+"/"+k
######################################################K_DICT######################################################              
            if str(K_dict[i]) != "0" and "(" not in K_dict[i] and ")" not in K_dict[i] and "/" not in K_dict[i]:
                if str(prob_potential_anchor[i]) != "0" :
                    if str(K_dict[i]) not in prob_potential_anchor[i].split("/"):
                        temp=prob_potential_anchor[i]
                        prob_potential_anchor[i]=temp+"/"+K_dict[i]
                else :
                    prob_potential_anchor[i]=K_dict[i]

            elif "(" in K_dict[i] or ")" in K_dict[i] :
                prob_potential_anchor[i]=K_dict[i]
            elif "/" in K_dict[i] :
                K_dict[i]=K_dict[i].split("/")
                for k in K_dict[i] :
                    if k not in prob_potential_anchor[i].split("/"):
                        temp=prob_potential_anchor[i]
                        if temp == '0':
                            prob_potential_anchor[i]=k
                        else:
                            prob_potential_anchor[i]=temp+"/"+k
    return prob_potential_anchor
###################################################################################################################

prob_potential_anchor = probable_potential_anchor()
# print(prob_potential_anchor)

################################REMOVING POTENTIAL ANCHORS WHICH ARE NOW SET IN STARTING###########################

for i in range(1,len(potential_anchor)) :
    if potential_anchor[i] in starting_anchor :
        potential_anchor[i]='0'
#print(potential_anchor)

############################REMOVING PROBABALE ANCHORS WHICH ARE EITHER POTENTIAL OR STARTING#####################
for i in range(1,len(prob_potential_anchor)) :
    ##########HANDLING STARTING###############
    flat_starting_anchor = []
    for i in starting_anchor :
        if "/" in i :
            i=i.split("/")
            flat_starting_anchor.extend(i)
        elif ")" in i:
            i=i.strip(")").split(" ")
            flat_starting_anchor.extend(i)
        else :
            flat_starting_anchor.append(i)
#     print(flat_starting_anchor) 
    for i in range(len(prob_potential_anchor)) :
        if "/" not in prob_potential_anchor[i] :
            if prob_potential_anchor[i] in flat_starting_anchor :
                prob_potential_anchor[i]='0'
        else :
            temp=prob_potential_anchor[i].split("/")
            current_ele=[]
            current_ele_str=""
            for t in temp :
                if t not in flat_starting_anchor :
                    current_ele.append(t)
            current_ele_str="/".join(current_ele)
            prob_potential_anchor[i]=current_ele_str
        if prob_potential_anchor[i] == '' :
            prob_potential_anchor[i] = '0'
    ################HANDLING_POTENTIAL##################
    flat_potential_anchor = []
    for i in potential_anchor :
        if "/" in i :
            i=i.split("/")
            flat_potential_anchor.extend(i)
        else :
            flat_potential_anchor.append(i)
    #print(flat_potential_anchor) 
    for i in range(len(prob_potential_anchor)) :
        if "/" not in prob_potential_anchor[i] :
            if prob_potential_anchor[i] in flat_potential_anchor :
                prob_potential_anchor[i]='0'
        else :
            temp=prob_potential_anchor[i].split("/")
            current_ele=[]
            current_ele_str=""
            for t in temp :
                if t not in flat_potential_anchor :
                    current_ele.append(t)
            current_ele_str="/".join(current_ele)
            prob_potential_anchor[i]=current_ele_str         
        if prob_potential_anchor[i] == '' :
            prob_potential_anchor[i] = '0'
#print(prob_potential_anchor)
###################################################################################################################
with open(sent_dir+'/All_Resources.csv','a')as f1:
        dwrite = csv.writer(f1)  
        dwrite.writerow(potential_anchor)
        dwrite.writerow(starting_anchor)
        dwrite.writerow(prob_potential_anchor)
