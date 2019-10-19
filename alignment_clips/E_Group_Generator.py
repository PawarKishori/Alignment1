import os,sys
from itertools import groupby
# from collections import OrderedDict
#input_file=os.getenv("HOME_anu_tmp")+"/tmp/ai1E_tmp/2.2/E_Word_Group_MFS.dat"
e_input_file=sys.argv[1]
temp_path="/".join(e_input_file.split("/")[:-1])
#print(temp_path)
sent_no=temp_path.split("/")[-1]
#print(sent_no)
e_output_file=temp_path+"/E_Group_Facts_Parser_POS.dat"
log_path="/".join(temp_path.split("/")[:-1])
log_file=log_path+"/Group_Facts_Parser_POS_log"
try:
    e_mfs_data=open(e_input_file).read().split(" ")
    e_mfs_data=e_mfs_data[1:-1] #ignoring string and )
except:
    with open(log_file,"a") as log :
        log.write("In "+sent_no+" E_Word_Group_MFS.dat doesn't exist.\n")
        sys.exit()
def list_of_groups(e_mfs):
    #mfs=[[i] for i in mfs_file] 
    #print(mfs)
    e_result = [list(g) for k,g in groupby(e_mfs,lambda x: '"' in x) if not k]
    #print (result)
    return e_result
def create_e_final_grouping_from_mfs() :
    e_groups=list_of_groups(e_mfs_data)
    #print(groups)
    with open(e_output_file,"w") as e_out:
        for gid in range(len(e_groups)):
            grouping=" ".join(str(x) for x in e_groups[gid])
            #print(grouping)
            str1="(Egroup_id-group_elements\t"+str(gid+1)+"\t"+grouping+")\n"
            #print(str1)
            e_out.write(str1)
create_e_final_grouping_from_mfs()

