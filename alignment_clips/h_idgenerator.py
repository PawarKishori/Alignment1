'''
import os
import glob
xxx = os.getenv("HOME")
print("   "+xxx)
s__=glob.glob(xxx+'/*/*/B*/2.*')
print(s__)
path = str(s__)+"/2.56/H_Word_Group.txt"
#path = "/media/hackhard/Data/IIIT H/BUgol_31st_july_2019/BUgol2.1E_tmp/2.56/H_Word_Group.txt"
n_file ='H_clip_deffact'
open_file = open(path,'r')
new_f=open(n_file,'w')

lis = open_file.readlines()

for i in range(0,len(lis)):
    st = (str(lis[i]))
    brac = (st[43:])
    print_ = "(Hgroup_id-group_elements "+str(i+1)+brac[0:brac.find(")")]+")"
    new_f.write(print_)
    print(print_)
'''

import os,sys
temp = sys.argv[1]     #BUgol2.1E
for k in range(1,116):
    print()
    print("2."+str(k))
    print("----------")
    path = os.getenv("HOME_anu_tmp")+"/tmp/"+temp+"_tmp"+"/2."+str(k)+"/H_Word_Group.dat"
    n_file =os.getenv("HOME_anu_tmp")+"/tmp/"+temp+"_tmp"+"/2."+str(k)+"/H_clip_deffact.dat"
    open_file = open(path,'r')
    new_f=open(n_file,'w')

    lis = open_file.readlines()
    #new_f.write("\n")
    #new_f.write("2."+str(k)+"------------------------"+"\n")
    for i in range(0,len(lis)):
        st = (str(lis[i]))
        brac = (st[43:])
        print_ = "(Hgroup_id-group_elements "+str(i+1)+brac[0:brac.find(")")]+")"+"\n"
        new_f.write(print_)
        print(print_.replace('\n',""))
