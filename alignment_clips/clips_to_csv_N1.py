import sys, csv, os
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'

eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
path_tmp= tmp_path + eng_file_name + "_tmp"
sent_dir =  tmp_path + eng_file_name + "_tmp/" + sent_no


with open(sent_dir + '/save_facts1', 'r') as f1:
    data = f1.read().split('\n')
    while "" in data:
         data.remove("")
    eid = [x.split(' ')[1] for x in data]
    hid = [" ".join(x.split(' ')[2:]).strip(')') for x in data]
    #print(data)
    print(eid)
    print(hid)

with open(sent_dir + '/save_facts_unknown', 'r') as f1:
    potential_data = f1.read().split('\n')
    while "" in potential_data:
         potential_data.remove("")
    potential_eid = [x.split(' ')[2] for x in potential_data]
    #potential_hid = [" ".join(x.split(' ')[3:]).strip(')') for x in potential_data]
    potential_hid = ['0' for x in potential_data]
    #print(potential_data)
    print(potential_eid)
    print(potential_hid)


eid_n1_dict={}

for e,h in zip(eid, hid):
    if e not in eid_n1_dict.keys():
        eid_n1_dict[e] = [h]
    else:
        eid_n1_dict[e].append(h)

for e,h in zip(potential_eid, potential_hid):
    if e not in eid_n1_dict.keys():
        eid_n1_dict[e] = [h]
    else:
        eid_n1_dict[e].append(h)
    

print(eid_n1_dict)

final_dict={}

for k,v in eid_n1_dict.items():
    if len(v)==1:
        final_dict[int(k)]=v[0]
    else:
        final_dict[int(k)]='0'
final = sorted(final_dict.items())
print(final)

n1_eids = [x[0] for x in final]
n1_hids = [x[1] for x in final]
print(n1_eids)
print(n1_hids)


with open(sent_dir+'/N1.csv', 'w') as csvfile :
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(n1_eids)
    csvwriter.writerow(n1_hids)




