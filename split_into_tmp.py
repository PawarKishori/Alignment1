#AUTHOR: Kishori
#python split_into_tmp.py <50-sent-filename> <new-file-name-in-tmp> <sent-folder-name>
#python split_into_tmp.py rGitaH012 H_sentence rGitaE_Up_012
import os
import sys

#alignment_path=os.getenv('HOME_alignment')
#print(alignment_path)
#filename='/home/kishori/codes/'+sys.argv[1]
#filename=alignment_path+'/'+sys.argv[1]
filename=sys.argv[1]
tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
print("File to be opened: ",filename)
with open(filename,'r')as f:
    all_sentences=f.readlines()
    for i in range(0,len(all_sentences)):
        fileid=i+1
#       with open("/home/kishori/forked/tmp_anu_dir/tmp/"+sys.argv[3]+"_tmp/2."+str(fileid)+"/"+sys.argv[2],"w") as f1:
	with open(tmp_path+sys.argv[3]+"_tmp/2."+str(fileid)+"/"+sys.argv[2],"w") as f1:

            print("Creating "+sys.argv[2]+" in "+tmp_path+sys.argv[3]+"_tmp/2."+str(fileid))
            f1.write(all_sentences[i])

