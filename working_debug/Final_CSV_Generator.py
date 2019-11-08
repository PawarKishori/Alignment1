
# coding: utf-8

# In[6]:


import csv,sys, os
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'

# eng_file_name = 'ai2E'
# sent_no='2.20'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
sent_dir = tmp_path + eng_file_name + "_tmp/" + sent_no
log_file = sent_dir+"/Final_CSV_Generator.log"
if os.path.exists(log_file) :
    os.remove(log_file)
log = open(log_file,'a')
def reading_N1():
    try:
        with open(sent_dir+'/new_N1.csv','rt')as f: ####PATH TO BE CHANGED
            data = csv.reader(f)
            rows=list(data)
        return rows[-1]
    except :
        print("new_N1.csv is absent in "+sent_no)
        log.write("new_N1.csv is absent in "+sent_no)
        sys.exit(0)
    
N1_Layer=reading_N1()
# print(N1_Layer)
N1_Layer.insert(0,"N1_Layer")
print(N1_Layer)
print("#############################################################")
def final_csv_creation():
    with open(sent_dir+'/All_Resources.csv','a')as f1:
        dwrite = csv.writer(f1)  
        dwrite.writerow(N1_Layer)
final_csv_creation()

