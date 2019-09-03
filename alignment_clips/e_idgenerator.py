import os,sys
temp = sys.argv[1]     #BUgol2.1E
for k in range(1,103):
    print()
    print("2."+str(k))
    print("----------")
    path = os.getenv("HOME_anu_tmp")+"/tmp/"+temp +"_tmp"+"/2."+str(k)+"/E_Word_Group.txt"
    n_file =os.getenv("HOME_anu_tmp")+"/tmp/"+temp + "_tmp"+ "/2."+str(k)+"/E_clip_deffact.dat"
    open_file = open(path,'r')
    new_f=open(n_file,'w')

    lis = open_file.readlines()
    #new_f.write("\n")
    #new_f.write("2."+str(k)+"------------------------"+"\n")
    for i in range(0,len(lis)):
        st = (str(lis[i]))
        brac = (st[45:])
        print_ = "(Egroup_id-group_elements "+str(i+1)+brac[0:brac.find(")")]+")"+"\n"
        new_f.write(print_)
        print(print_.replace('\n',""))
