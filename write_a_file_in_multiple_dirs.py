#python write_a_file_in_multiple_dirs.py cl_english_100_detok cl_hindi_100_detok_multiwords_underscored Hindi_sent_mwes_underscored.dat /home/user/forked/alignment_manju
import sys
import os
import subprocess
#corpus_file_path="/home/user/forked/alignment_manju"
corpus_file_path=sys.argv[4]
print(corpus_file_path)
cmd="echo $HOME_anu_tmp"
result=subprocess.check_output(cmd, shell=True)
sent_dir_path=result.strip()+"/tmp/"+sys.argv[1]+"_tmp"
print(sent_dir_path)
count=0
for line in open(corpus_file_path+"/"+sys.argv[2],"r"):
	count=count+1
	dir="2."+str(count)
	f2 = open(sent_dir_path+"/"+dir+"/"+sys.argv[3],"w")	
	f2.write(line)
	f2.close()
