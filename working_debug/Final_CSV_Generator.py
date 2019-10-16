
# coding: utf-8

# In[6]:


import csv,sys, os
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'

#eng_file_name = 'ai1E'
#sent_no='2.5'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
sent_dir = tmp_path + eng_file_name + "_tmp/" + sent_no

def reading_new_N1():
    all_data=[]
    with open(sent_dir+'/new_N1.csv','rt')as f: ####PATH TO BE CHANGED
        data = csv.reader(f)
        rows=list(data)
    return rows[-1]
N1_Layer=reading_new_N1()
# print(N1_Layer)
N1_Layer.insert(0,"N1_Layer")
# print(N1_Layer)
print("#############################################################")
def final_csv_creation():
    with open(sent_dir+'/All_Resources.csv','a')as f1:
        dwrite = csv.writer(f1)  
        dwrite.writerow(N1_Layer)
final_csv_creation()

