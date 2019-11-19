#Programme to extract anusaaraka root (K layer root info)
#Written by Roja(20-09-19)
#RUN: python3 ~/Alignment1/csv_creation/extract_anu_root_nd_tam.py  id_Apertium_input.dat > anu_root.dat
###############################################
import sys, re

root_dic = {}
tam_dic = {}


def extarct_rt_nd_tam(List):
    if lst[2].startswith('root:'):
        rt = lst[2].split(',')[0][5:]
        root_dic[int(lst[1])] =  rt
        tam = lst[2].split(',')[1][4:]
        tam_dic[int(lst[1])] = tam
    #   print(rt, tam)
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

for line in open(sys.argv[1]):
    lst = line.strip().split()
    extarct_rt_nd_tam(lst)

for key in sorted(root_dic):
    print('(id-anu_root ', key, root_dic[key], ')')

for key in sorted(tam_dic):
    print('id-anu_tam ', key, tam_dic[key], ')')

