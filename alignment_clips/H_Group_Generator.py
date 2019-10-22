import os,sys
from itertools import groupby
# from collections import OrderedDict
#input_file=os.getenv("HOME_anu_tmp")+"/tmp/ai1E_tmp/2.2/E_Word_Group_MFS.dat"
h_input_file=sys.argv[1]
temp_path="/".join(h_input_file.split("/")[:-1])
#print(temp_path)
sent_no=temp_path.split("/")[-1]
#print(sent_no)
h_output_file=temp_path+"/H_Group_Facts_Parser_POS.dat"
log_path="/".join(temp_path.split("/")[:-1])
log_file=log_path+"/Group_Facts_Parser_POS_log"
try:
    h_mfs_data=open(h_input_file).read().split(" ")
    h_mfs_data=h_mfs_data[1:-1] #ignoring string and )
except:
    with open(log_file,"a") as log :
        log.write("In "+sent_no+" H_Word_Group_MFS.dat doesn't exist.\n")
        sys.exit()
def list_of_groups(h_mfs):
    #mfs=[[i] for i in mfs_file] 
    #print(mfs)
    h_result = [list(g) for k,g in groupby(h_mfs,lambda x: '"' in x) if not k]
    print (h_result)
    return h_result
def create_h_final_grouping_from_mfs() :
    h_groups=list_of_groups(h_mfs_data)
    #print(groups)
    with open(h_output_file,"w") as h_out:
        for gid in range(len(h_groups)):
            grouping=" ".join(str(x) for x in h_groups[gid])
            #print(grouping)
            str1="(Hgroup_id-group_elements\t"+str(gid+1)+"\t"+grouping+")\n"
            #print(str1)
            h_out.write(str1)
create_h_final_grouping_from_mfs()

