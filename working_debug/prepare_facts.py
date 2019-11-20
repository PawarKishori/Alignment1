import sys, os, anchor, csv
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
sent_dir = tmp_path + eng_file_name + "_tmp/" + sent_no
file_ = sent_dir+"/All_Resources.csv"
facts = sent_dir+"/facts.dat"

print(file_)
k_dict = anchor.load_row_from_csv(file_ , 11)
wsd_modulo = anchor.load_row_from_csv(file_ , 10)
print(k_dict)
print(wsd_modulo)
print('================')
with open(facts , 'w') as f:
    for i in range(1,len(k_dict)):
        print("(E_id-k_dict-mfs-wsd_modulo\t"+ str(i)+"\t"+k_dict[i].replace("_", '0') + '\tmfs\t'+ wsd_modulo[i]+ ')')
        f.write("(E_id-k_dict-mfs-wsd_modulo\t"+ str(i) +"\t" +k_dict[i].replace("_", '0') + '\tmfs\t'+ wsd_modulo[i]+ ')\n')


