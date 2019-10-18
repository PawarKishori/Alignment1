
# coding: utf-8

# In[26]:


import csv,sys, os, string
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
#eng_file_name = 'ai1E'
#sent_no='2.77'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
sent_dir = tmp_path + eng_file_name + "_tmp/" + sent_no
e_sent_file=sent_dir+"/E_sentence"
h_sent_file=sent_dir+"/H_sentence"
def eng_id_to_idword_pair_hash():
    id_to_word_pair={}
    e_sent=open(e_sent_file,"r").read().strip("\n")
    e_sent = e_sent.translate(e_sent.maketrans('', '', string.punctuation))
    e_sent = e_sent.split()
    for index,word in enumerate(e_sent):
        temp=str(index+1)+"_"+word
        id_to_word_pair[str(index+1)]=temp
    return id_to_word_pair
eng_id_to_idword_pair=eng_id_to_idword_pair_hash()

def hin_id_to_idword_pair_hash():
    id_to_word_pair={}
    h_sent=open(h_sent_file,"r").read().strip("\n")
    h_sent = h_sent.translate(h_sent.maketrans('', '', string.punctuation))
    h_sent = h_sent.split()
    for index,word in enumerate(h_sent):
        temp=str(index+1)+"_"+word
        id_to_word_pair[str(index+1)]=temp
    return id_to_word_pair
hin_id_to_idword_pair=hin_id_to_idword_pair_hash()
# print(hin_id_to_idword_pair)

def reading_all_resources():
    all_data=[]
    with open(sent_dir+'/All_Resources.csv','rt')as f: ####PATH TO BE CHANGED
        data = csv.reader(f)
        rows=list(data)
    return rows
all_resources=reading_all_resources()
# print(all_resources)
def E_id_conversion():
    row0=[]
    row0.append("English_Word")
    for i in all_resources[0][1:] :
        row0.append(eng_id_to_idword_pair[str(i)])
    return row0
row0=E_id_conversion()
def H_id_conversion() :
    all_rows= []
    for i in all_resources[1:] :
        temp_list=[]
        temp_list.append(i[0])
        for j in i[1:] :
#             print(j)
            if str(j) != '0' and "(" not in str(j) and " " not in str(j) and ")" not in str(j):
                if "/" not in str(j):
                    if " " not in str(j):
                        temp_list.append(hin_id_to_idword_pair[str(j)])  
                elif "/" in str(j):
                    j=str(j).split("/")
                    temp_list.append("/".join(hin_id_to_idword_pair[k] for k in j))
            elif "(" in str(j):
                temp_list.append(j)
            elif ")" in str(j) :
                j=str(j).strip(")").split(" ")
                temp_list.append(" ".join(hin_id_to_idword_pair[k] for k in j)+")")
            elif " " in str(j) :
                j=str(j).split(" ")
                temp_list.append(" ".join(hin_id_to_idword_pair[k] for k in j))
            else :
                temp_list.append('0')
        all_rows.append(temp_list)
    return all_rows
all_rows=H_id_conversion()
print(all_rows)
def creating_new_csv():
    with open(sent_dir+"/All_Resources_id_word.csv","w") as csvfile :
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row0)
        for i in all_rows:
            csvwriter.writerow(i)
                
creating_new_csv()
#print(all_resources)



