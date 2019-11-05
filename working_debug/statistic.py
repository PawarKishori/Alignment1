
# coding: utf-8

# In[33]:


import sys,os,re
from os import path
#csv_file="/home/nupur/ai1E_tmp/2.1/new_N1.csv" 

temp_path = sys.argv[1]
sent_no = sys.argv[2]
csv_file = temp_path + '/' +sent_no +'/new_N1.csv'
hindi_file = temp_path +  '/' +sent_no +'/H_wordid-word_mapping.dat'
lwg_file = temp_path + '/' +sent_no + '/E_lwg.dat'

#temp = hindi_file.split("/")[:-1]
#temp_path="/".join(temp[:-1])
#sent_no = "".join(temp[-1:])

align_per_info="/alignment_percent_info.txt"
align_leftover="/alignment_leftover_info.txt"
align_aligned="/alignment_aligned_info.txt"
log=open(temp_path+"/statistic_info_log","a")


class EmptyError():
    pass
def ids_from_csv() :
    try :
        csv=open(csv_file,"r")
        csvread=csv.read()
        if len(csvread) == 0 :
            raise EmptyError
        
        id_split=csvread.split("\n")[:-1]
        e_ids=id_split[0].split(",")
        h_ids=id_split[1].split(",")
        e_total=e_ids[-1]
        return e_ids,h_ids,int(e_total)
    except(EmptyError) :
        log.write("In "+sent_no+" new_N1.csv file is absent\n")
        exit()
    
    
#######
e_ids,h_ids,e_total=ids_from_csv() 
#print(e_ids,h_ids,e_total)

def h_total_words() :
    try:
        hid=open(hindi_file,"r")
        hl=hid.read()
        if len(hl) == 0 :
            raise EmptyError
        hlist=hl.split("\n")[:-1]
        h_total=len(hlist)
        return h_total
    except(EmptyError) :
        log.write("In "+sent_no+" H_wordid-word_mapping.dat file is absent\n")
        exit()
#####
h_total=h_total_words()


def left_and_mapping_list():
    left=[]
    e_mapp=[]
    for i,j in zip(e_ids,h_ids) :
        if j == '0' :
            left.append(i)
        else :
            str1=i
            e_mapp.append(str1)
    return e_mapp,left
e_mapp,left=left_and_mapping_list()


def e_mapping_info() :
    all_lwg=[]
    all_mapped=[]
    try :
        e_lwg=open(lwg_file,"r").read()
        if len(e_lwg) == 0 :
            raise EmptyError 
        lwg=e_lwg.split("\n")[:-1]
        for i in lwg :
            lwg_col=i.split("\t")[1:]
            all_lwg.append(lwg_col)
    #print(all_lwg)  
        for i in all_lwg :
            mapped=i[1].strip(")").split(" ")
            if i[0] in e_mapp :
                #print(i)
                all_mapped.append(mapped)
    #print(all_grouped)
        flat_all_mapped = [item for sublist in all_mapped for item in sublist]
    #print(flat_all_grouped)
        for i in left :
            for j in flat_all_mapped :
                if i == j :
                    e_mapp.append(i)
        return len(e_mapp),e_mapp
    except(EmptyError) :
        log.write("In "+sent_no+" H_wordid-word_mapping.dat file is absent\n")
        exit()
        
        
        
mapp_len,e_mapped_ids=e_mapping_info()

def h_mapping_info() :
    final=[]
    h_mapped=[]
    for i in h_ids :
        final.append(i.split(" "))
    #print(final)
    flat=[item for sublist in final for item in sublist]
    #print(flat)
    for i in flat :
        if i != '0' :
            h_mapped.append(i)
    return len(h_mapped),h_mapped
h_len,h_mapped_ids=h_mapping_info()
def e_leftovers():
    e_left_ids=[]
    
    for i in range(1,e_total+1) :
        if str(i) not in e_mapped_ids :
            e_left_ids.append(str(i))
            #print(i)
    return e_left_ids
def h_leftovers() :
    h_left_ids=[]
    for i in range(1,h_total+1) :
        if str(i) not in h_mapped_ids :
            h_left_ids.append(str(i))
    return h_left_ids
def h_stat() :
    per = (float(h_len)/h_total)*100
    return round(per,2)


def e_stat() :
    per = (float(mapp_len)/e_total)*100
    return round(per,2)
def final_output() :
    e_per=e_stat()
    h_per=h_stat()
    h_left_ids=h_leftovers()
    e_left_ids=e_leftovers()
    per=open(temp_path+align_per_info,"a")
    left=open(temp_path+align_leftover,"a")
    aligned=open(temp_path+align_aligned,"a")
    
    #print(sent_no)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("English  Aligned" , e_mapped_ids)
    print("English Left over ids are",e_left_ids)
    print("English Alignment Info. is "+str(e_per))
    print("###################################")
    print("Hindi Aligned ",h_mapped_ids)
    print("Hindi Left over ids are",h_left_ids)
    print("Hindi Alignment Info. is "+str(h_per))
    per_format=sent_no+"\t"+str(h_per)+"\t"+str(e_per)
    leftover_format=sent_no+"\t"+" ".join(h_left_ids)+"\t"+" ".join(e_left_ids)
    aligned_format=sent_no+"\t"+" ".join(h_mapped_ids)+"\t"+" ".join(e_mapped_ids)
    #print(per_format)
    #print(leftover_format)
    #print(aligned_format)
    per.write(per_format+"\n")
    left.write(leftover_format+"\n")
    aligned.write(aligned_format+"\n")
final_output()

