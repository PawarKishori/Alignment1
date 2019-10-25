import csv,sys, os, string
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
# eng_file_name = 'ai2E'
# sent_no='2.2'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
sent_dir = tmp_path + eng_file_name + "_tmp/" + sent_no
e_file=sent_dir+"/E_wordid-word_mapping.dat"
h_file=sent_dir+"/H_wordid-word_mapping.dat"
log_file = sent_dir+"/All_Resources_id_word.log"
if os.path.exists(log_file) :
    os.remove(log_file)
log = open(log_file,'a')
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
def eng_id_to_idword_pair_hash():
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
    
eng_id_to_idword_pair=eng_id_to_idword_pair_hash()
print(eng_id_to_idword_pair)
for i in eng_id_to_idword_pair :
    print
def hin_id_to_idword_pair_hash():
    h2w=[]
    show_hin ={}  
    try:   
        h2w = create_dict(h_file, '(H_wordid-word')
        h2w=dict((k, v) for k,v in h2w.items())
#         print(e2w)
           
        for k,v in h2w.items():
            show_hin[k] = str(k)+"_"+v
#         print(show_hindi)
        
    except FileNotFoundError:
        print("FILE MISSING: " + h_file )
        log.write("FILE MISSING: " + h_file + "\n")
        sys.exit(0)
#     print(e2w)
    return show_hin
hin_id_to_idword_pair=hin_id_to_idword_pair_hash()
# print(hin_id_to_idword_pair)

def reading_all_resources():
    all_data=[]
    try :
        with open(sent_dir+'/All_Resources.csv','rt')as f: ####PATH TO BE CHANGED
             data = csv.reader(f)
             rows=list(data)
    except :
        log.write(sent_dir+"/All_Resources.csv is missing")
        print(sent_dir+"/All_Resources.csv is missing")
        sys.exit(0)
    return rows
all_resources=reading_all_resources()
#print(all_resources)
def E_id_conversion():
    row0=[]
    row0.append("English_Word")
    #print(row0)
    print(all_resources[0][1:])
    for i in all_resources[0][1:] :
#         print(eng_id_to_idword_pair[i])
        row0.append(eng_id_to_idword_pair[int(i)])
    #print(row0)
    return row0
row0=E_id_conversion()
def H_id_conversion() :
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
    return all_rows
all_rows=H_id_conversion()
#print(all_rows)
def creating_new_csv():
    with open(sent_dir+"/All_Resources_id_word.csv","w") as csvfile :
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row0)
        for i in all_rows:
            #print(i)
            csvwriter.writerow(i)
                
creating_new_csv()
#print(all_resources)


