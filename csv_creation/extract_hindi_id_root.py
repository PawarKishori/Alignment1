#Written in python3.6
#To run: python extract_hindi_id_root.py
#Kishori
#28-08-2019
 
import re, os
def extract_dictionary_from_deftemplate(filename):
	hindi_dict_id_root={}
	with open(filename, "r") as f:
		data = f.read().split("\n")
		while "" in data:
			data.remove("")
	with open(writeFile, 'w') as w:
		for entry in data:
			head_id=re.findall("(head_id \w+)",entry)[0].split(" ")[1]
			root_word=re.findall("(root \w+)",entry)[0].split(" ")[1]
			#print(head_id, root_word)
			w.write("(H_headid-root\t"+head_id+"\t"+ root_word+")\n")
			hindi_dict_id_root[head_id]=root_word
	return(hindi_dict_id_root)
		

#tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
#path = tmp_path  + sys.argv[1] + '_tmp'          sys.argv[1] will be BUgol2.1

filename = "manual_lwg.dat"
writeFile = "H_headid-root_info.dat"
hindi_dict_id_root=extract_dictionary_from_deftemplate(filename)
print(hindi_dict_id_root)
