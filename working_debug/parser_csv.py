import sys, os, pandas as pd, numpy as np

tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
eng_file_name = sys.argv[1]
# eng_file_name = 'BUgol2.2E'

sent_no = sys.argv[2]
path_tmp= tmp_path + eng_file_name + "_tmp/" + sent_no
filename =path_tmp +  '/H_wordid-word_mapping.dat'
efilename = path_tmp + '/E_wordid-word_mapping.dat'
def parser2wordid1(filename):
    with open(filename,"r") as f1: 
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        p2w = {}
        for line in text:
            t = line.lstrip('(H_wordid-word').strip(')').split("\t")
            p2w[int(t[1].lstrip("P"))] = t[2]
    return(p2w)


def parser2wordid(filename):
    with open(filename,"r") as f1: 
        text = f1.read().split("\n")
        while("" in text) :
            text.remove("")
        p2w = {}
        for line in text:
            t = line.lstrip('(E_wordid-word').strip(')').split("\t")
            p2w[int(t[1].lstrip("P"))] = t[2]
    return(p2w)
    
p2w = parser2wordid1(filename)
e2w = parser2wordid(efilename)
# print(p2w)
# print(e2w)

dfs = pd.read_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_1.csv")
dfs.index = np.arange(1,len(dfs)+1)
# print(dfs.shape)

# r = len(p2w)
# c = dfs.shape[1] - 1
# print(r, c)
# r_list = range(1,r+1)
# c_list =range(1,c+1)
# print(r_list, c_list)

# df = pd.Dataframe(rows=r_list, columns = c_list)
# df = pd.DataFrame(index=r_list, columns = c_list)
# print(df)

resources = [i.lstrip().rstrip() for i in dfs.iloc[:, 0].tolist()]
letters = [chr(i) for i in range(65, 88)]
resource_dict={}

for k,v in zip(letters,resources):
    resource_dict[k]=v

show_hindi ={}    
for k,v in p2w.items():
    show_hindi[k] = str(k)+"_"+v
    
show_eng ={}    
for k,v in e2w.items():
    show_eng[k] = str(k)+"_"+v
    
# print(show_eng)
# print(show_hindi)

eng = [show_eng[i] for i in sorted(show_eng.keys())]
hin = [show_hindi[i] for i in sorted(show_hindi.keys())]

eng, hin
df = pd.DataFrame(index=hin, columns = eng)
df
p2w
e2w
resources
resource_dict
print()
# resource_dict_invert= {v: k for k, v in resource_dict.items()}
# dfs.replace({0=})


import sys, os, pandas as pd, numpy as np

# tmp_path=os.getenv('HOME_anu_tmp')+'/tmp/'
# eng_file_name = 'BUgol2.1E'
# eng_file_name = 'BUgol2.2E'
# sent_no = '2.25'
path_tmp= tmp_path + eng_file_name + "_tmp/" + sent_no

dfs = pd.read_csv(path_tmp +'/'+ eng_file_name + "_"+sent_no + "_1.csv")
dfs. index = np.arange(1,len(dfs)+1)
print(dfs.shape)
no_of_eng_words = dfs.shape[1]
# zero_remover = lambda x: x != '0'
# hindi_allocations= list(map(zero_remover, dfs.iloc[:,7].tolist()))
dfs.iloc[:,7].tolist()
final_row_in_csv=[]; final_row_in_csv1=[]
for j in range(0,no_of_eng_words):
    
    hindi_allocations_list = [str(i) for i in dfs.iloc[:,j].tolist() if i!='0' and i!=0]
    
    if not hindi_allocations_list:
        hindi_allocations_list.append('0')
    hindi_allocations = "#".join([str(i) for i in hindi_allocations_list])
    
    if j==0:
        hindi_allocations = "all"
    final_row_in_csv.append(hindi_allocations)
    
    for item in hindi_allocations_list:
        if '/' in item:
            [hindi_allocations_list.append(x) for x in item.split('/')]     
#     print(hindi_allocations_list)

    hindi_allocations_list = list(dict.fromkeys(hindi_allocations_list))

    
    for item in hindi_allocations_list:
#         print(item)
        if '/' in item:
            hindi_allocations_list.remove(item)

    print(hindi_allocations_list)

    hindi_allocations_updated = "#".join(hindi_allocations_list)
    if j==0:
        hindi_allocations_updated = "all_intersect"
    final_row_in_csv1.append(hindi_allocations_updated)
#     print(hindi_allocations_list)
# print(hindi_allocations_list)

