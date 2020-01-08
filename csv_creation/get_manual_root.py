#Written by Roja(08-01-20)
#python3 $HOME_alignment/csv_creation/get_manual_root.py  manual_id_wrdid.dat manual_lwg_new.dat > manual_mapped_id_root_info.dat

import sys, re

pid_wid_dic = {}

for line in open(sys.argv[1]):
    lst = line[:-2].split()
    pid_wid_dic[int(lst[1])] = lst[2]


for line in open(sys.argv[2]):
    headid = re.findall(r'head_id \d+', line)
    root = re.findall(r'root [^)]+', line)

    head_id = headid[0][8:]
    m_root = root[0][5:]

    print('(manual_mapped_id-root',  pid_wid_dic[int(head_id)],  m_root, ')')
