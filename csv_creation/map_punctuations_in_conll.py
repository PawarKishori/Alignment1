import sys, re

count = 0
f = open(sys.argv[1], 'r').readlines()

punct_lst = [ ")", "(" , "," , "." , ":" , ";" ,  "?", "!", "'", "\"" , "{", "}", "[", "]", "\n" ]

punc = ''
w_id_dic = {}

for i in range(0, len(f)-1):
    lst = f[i].strip().split('\t')
    if lst[1] in punct_lst:
        count += 1
    else:
        w_id_dic[int(lst[0])] = int(lst[0])-count


#for key in sorted(w_id_dic):
#    print(key, w_id_dic[key])


def replace_dep_rel(rel):
    drel = rel.split('|')
    new_rel = []
    for each in drel:
        lst = each.split(':')
        new_rel.append(str(w_id_dic[int(lst[0])])+':'+ ':'.join(lst[1:]))
    return '|'.join(new_rel)


for i in range(0, len(f)-1):
    lst = f[i].strip().split('\t')
    if i <= len(f)-4:
        n_lst = f[i+1].strip().split('\t')
    if int(lst[0]) in w_id_dic.keys() and lst[6] != '0':
            lst[0] = str(w_id_dic[int(lst[0])])
            lst[6] = str(w_id_dic[int(lst[6])])
            if lst[8] != '_':
                lst[8] = replace_dep_rel(lst[8])
    if n_lst[1] in punct_lst:
        punc = n_lst[1]
        lst[1] = lst[1] + punc
        print('\t'.join(lst[0:]))
    elif lst[1] not in punct_lst:
        print('\t'.join(lst[0:]))
