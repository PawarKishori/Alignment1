import os, re, sys
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
eng_file_name = sys.argv[1]
sent_no = sys.argv[2]
#eng_file_name = 'ai1E'
#sent_no = '2.18' #2.29, 2.21, 2.61, 2.14, 2.64
path_tmp= tmp_path + eng_file_name + "_tmp/" + sent_no
sent_dir =  tmp_path + eng_file_name + "_tmp/"
lwg_info_file = path_tmp +  '/tam_id.dat'


def extract_eng_lwg_dictionary_from_ordered_fact_tam_id(filename):
        hindi_dict_id_root={}
        with open(filename, "r") as f:
                data = f.read().split("\n")
                while "" in data:
                        data.remove("")
		#print(data)
        hid_gid_dict={}
        for entry in data:
		#pid_wid=re.findall("(id-tam_type\t\w+\t\w+)",entry)[0].split("\t")
		hid_tam=re.findall("(id-TAM \w+ \w+)",entry)
		#print(hid_tam)
		if(len(hid_tam)>0):
			hid_tam=re.findall("(id-TAM \w+ \w+)",entry)[0].split(" ")
			#print(hid_tam)
			hid=hid_tam[1]                
			tam=hid_tam[2]
			#print(hid,tam,tam.count('_'), range(int(hid)-tam.count('_'), int(hid)+1))
			#hid_gid_dict[int(hid)]=range(int(hid)-tam.count('_'), int(hid)+1)
			seq=range(int(hid)-tam.count('_'), int(hid)+1)
			str_seq=[str(i) for i in seq]
			hid_gid_dict[hid]=" ".join(str_seq)
	return(hid_gid_dict)

def write_dictionary_row_by_row_in_fact_file(dict1, fact_label, filename):
	with open(path_tmp + '/' + filename, 'w') as f:
		for k,v in dict1.items():
			print('('+fact_label+'\t'+ k + '\t'+v+')\n')
			f.write('('+fact_label+'\t'+ k + '\t'+v+')\n')
		

hid_gid_dict=extract_eng_lwg_dictionary_from_ordered_fact_tam_id(lwg_info_file)
print(hid_gid_dict)

write_dictionary_row_by_row_in_fact_file(hid_gid_dict,"E_hid-grp_ids","E_lwg.dat" )
