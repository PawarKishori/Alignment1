def create_dict(filename,string):
    with open(filename,"r") as f1: 
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        p2w = {}
        for line in text:
            t = line.lstrip(string).strip(')').split("\t")
            p2w[int(t[1].lstrip("P"))] = t[2]
    return(p2w)


def eng_id_to_idword_pair_hash(e_file):
    e2w=[]
    show_eng ={}  
    try:   
        e2w = create_dict(e_file, '(E_wordid-word')
        e2w=dict((k, v) for k,v in e2w.items())
#         print(e2w)
           
        for k,v in e2w.items():
            show_eng[k] = str(k)+"_"+v
#         print(show_hindi)
        
    except FileNotFoundError:
        print("FILE MISSING: " + e_file )
        log.write("FILE MISSING: " + e_file + "\n")
        sys.exit(0)
#     print(e2w)
    return show_eng
    

def hin_id_to_idword_pair_hash(h_file):
    h2w=[]
    show_hin={}
    try:   
        h2w = create_dict(h_file, '(H_wordid-word')
        h2w=dict((k, v) for k,v in h2w.items())
        print(h2w)
           
        for k,v in h2w.items():
            show_hin[k] = str(k)+"_"+v
        
    except FileNotFoundError:
        print("FILE MISSING: " + h_file )
        log.write("FILE MISSING: " + h_file + "\n")
        sys.exit(0)
#     print(e2w)
    return show_hin


def reading_all_resources(all_resource_after_srun):
    all_data=[]
    try :
        with open(all_resource_after_srun,'rt')as f: ####PATH TO BE CHANGED
            data = csv.reader(f)
            rows=list(data)
    except :
        log.write(all_resource_after_srun +" is missing")
        print(all_resource_after_srun +" is missing")
        sys.exit(0)
    return rows


def E_id_conversion(eng_id_to_idword_pair,all_resources):
    row0=[]
    row0.append("English_Word")
    #print(row0)
    #print(all_resources[0][1:])
    for i in all_resources[0][1:] :
#         print(eng_id_to_idword_pair[i])
        row0.append(eng_id_to_idword_pair[int(i)])
    #print(row0)
    return row0

'''def H_id_conversion(hin_id_to_idword_pair, all_resources) :
    all_rows= []
    print(all_resources)
    
    for i in all_resources[1:] :
        print(i)
    return all_rows'''


'''def H_id_conversion(hin_id_to_idword_pair,all_resources) :
    all_rows= []
    for i in all_resources[1:] :
        temp_list=[]
        temp_list.append(i[0])
        for j in i[1:] :
#             print(j)
            if str(j) != '0' and "(" not in str(j) and ")" not in str(j):
                if "/" not in str(j) and " " not in str(j)  :
                    temp_list.append(hin_id_to_idword_pair[int(j)])
                elif "/" in str(j) and " " not in str(j) :
                    j=str(j).split("/")
                    temp_list.append("/".join(hin_id_to_idword_pair[int(k)] for k in j)) 
                elif " " in str(j) and "/" not in str(j) :
                    j=str(j).split(" ")
                    temp_list.append(" ".join(hin_id_to_idword_pair[int(k)] for k in j)) 
                elif " " in str(j) and "/" in str(j) :
                    j=str(j).split(" ")
                    temp=[]
                    for  k in j : 
                        if "/" not in k : 
                            temp.append((hin_id_to_idword_pair[int(k)]))
                        else :
                            k=str(k).split("/")
                            temp.append("/".join(hin_id_to_idword_pair[int(z)] for z in k ))
                    temp_list.append(" ".join(temp))
            elif "(" in str(j):
                temp_list.append(j)
            elif ")" in str(j) :
                j=str(j).strip(")").split(" ")
                temp_list.append(" ".join(hin_id_to_idword_pair[int(k)] for k in j)+")")
            else :
                temp_list.append('0')
        all_rows.append(temp_list)
    return all_rows'''


def H_id_conversion(hin_id_to_idword_pair,all_resources) :
    all_rows= []
    for i in all_resources[1:] :
        temp_list=[]
        temp_list.append(i[0])
        for j in i[1:] :
#             print(j)
            if str(j) != '0' and "(" not in str(j) and ")" not in str(j):
                if "/" not in str(j) and " " not in str(j)  :
                    temp_list.append(hin_id_to_idword_pair[int(j)])
                elif "/" in str(j) and " " not in str(j) :
                    j=str(j).split("/")
                    temp_list.append("/".join(hin_id_to_idword_pair[int(k)] for k in j))
                elif " " in str(j) and "/" not in str(j) :
                    j=str(j).split(" ")
                    print(j)
                    temp_list.append(" ".join(hin_id_to_idword_pair[int(k)] for k in j))
                elif " " in str(j) and "/" in str(j) :
                    j=str(j).split(" ")
                    temp=[]
                    for  k in j :
                        if "/" not in k :
                            temp.append((hin_id_to_idword_pair[int(k)]))
                        else :
                            k=str(k).split("/")
                            temp.append("/".join(hin_id_to_idword_pair[int(z)] for z in k ))
                    temp_list.append(" ".join(temp))
            elif "(" in str(j):
                temp_list.append(j)
            elif ")" in str(j) :
                j=str(j).strip(")").split(" ")
                temp_list.append(" ".join(hin_id_to_idword_pair[int(k)] for k in j)+")")
            else :
                temp_list.append('0')
        all_rows.append(temp_list)
    return all_rows

#print(all_rows)

def add_anusaaraka_layer():
    k_data = [ i.rstrip("\n") for i in open(k_layer_file).readlines()]
    k_data = [item.rstrip(")") for item in k_data]
    e_data = [ i.rstrip("\n") for i in open(e_file).readlines()]
    k_enhanced_data = open(k_enhanced_file).read()
    k_enhanced_list = k_enhanced_data.split(",")
    k_enhanced_corrected_data = open(k_enhanced_corrected_file).read()
    k_enhanced_corrected_list = k_enhanced_corrected_data.split(",")
    k_list = list()
    k_list.append("Anusaaraka Layer")

    for i in e_data:
        k_list.append(str(0))

    for i in k_data:
        eid = i.split(" ")[1]
        if len(i.split(" ")) > 2:
            word = i.split(" ")[2:]
            hword = ""
            for i in word:
                hword = hword + " " +  i
        else :
            hword = "0"
        k_list[int(eid)] = hword

    k_list_utf = [H_Modules.wx_utf_converter_sentence(i) for i in k_list]
    k_list_utf[0] = k_list[0]
    
    for i in range(len(k_enhanced_list)):
        if "((" in k_enhanced_list[i]:
            if k_list_utf[i] =="0":
                k_list_utf[i] = "(("
            else:
                k_list_utf[i] = "(( " + k_list_utf[i]

        elif "))" in k_enhanced_list[i]:
            if k_list_utf[i] =="0":
                k_list_utf[i] = "))"
            else:
                k_list_utf[i] = k_list_utf[i] + " ))"

    k_enhanced_list[0] = "Shreya's_Layer"
    k_enhanced_corrected_list[0] = "Shreya's_Grouping_Improved"
    return(k_list_utf,k_enhanced_list,k_enhanced_corrected_list)


def creating_new_csv():
    with open(sent_dir+"/srun_All_Resources_id_word.csv","w") as csvfile :
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row0)
        csvwriter.writerow(anusaaraka_layer)
        csvwriter.writerow(shreya_layer)
        print(row0)
        print(anusaaraka_layer)
        print(shreya_layer)
        if len(shreya_layer) == len(shreya_layer_corr):
            csvwriter.writerow(shreya_layer_corr)
            print(shreya_layer_corr)
        for i in all_rows:
            if i[0] == "K_exact_with_tam_analysis":
                with open (sent_dir + '/K_tam_layer_v.csv','r')  as f:
                   data = csv.reader(f)
                   for r in data:

                       j1=[ii.replace("-",'0') for ii in r]
                       csvwriter.writerow(j1[:-1])
                       print(j1[:-1])
            else:
                csvwriter.writerow(i) 
                

import csv,sys, os, string,re,H_Modules
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
# eng_file_name = 'ai2E'
# sent_no='2.2'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
sent_dir = tmp_path + eng_file_name + "_tmp/" + sent_no

e_file=sent_dir+"/E_wordid-word_mapping.dat"
h_file=sent_dir+"/H_wordid-word_mapping.dat"
log_file = sent_dir+"/srun_All_Resources.log"
k_layer_file = sent_dir + '/id_Apertium_output.dat'
k_enhanced_file = sent_dir + '/K_enhanced.dat'
k_enhanced_corrected_file = sent_dir + '/K_enhanced_corrected.dat'

all_resource_after_srun = sent_dir+"/srun_All_Resources.csv"

if os.path.exists(log_file) :
    os.remove(log_file)
log = open(log_file,'a')
eng_id_to_idword_pair = eng_id_to_idword_pair_hash(e_file)
hin_id_to_idword_pair = hin_id_to_idword_pair_hash(h_file)
all_resources = reading_all_resources(all_resource_after_srun)
row0 = E_id_conversion(eng_id_to_idword_pair,all_resources)
all_rows = H_id_conversion(hin_id_to_idword_pair,all_resources)
anusaaraka_layer,shreya_layer,shreya_layer_corr = add_anusaaraka_layer()
creating_new_csv()

