import sys, re

root_dic = {}

for line in open(sys.argv[1]):
    lst = line.strip().split()
    if lst[2].startswith('root:'):
        rt = lst[2].split(',')[0][5:]
        root_dic[int(lst[1])] =  rt
        #print rt
    elif lst[2].startswith('^'):
        rt = lst[2].split('<')[0][1:]
        root_dic[int(lst[1])] =  rt
        #print rt
    elif lst[2] == ')':
        rt = '-'
        root_dic[int(lst[1])] =  rt
        #print rt
    else:
        rt = lst[2]
        root_dic[int(lst[1])] =  rt
        #print rt


for key in sorted(root_dic):
    print '(id-anu_root ', key, root_dic[key], ')'


