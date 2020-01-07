import sys, re

p_id_w_id_dic = {}

#mapping parser id to worid and storing both mapping facts and mapped facts
for line in open(sys.argv[1]):
    lst = line[:-2].split()
    p_id_w_id_dic[int(lst[1])] = int(lst[2])

def replace_pid_with_id(string, par_id):
    string = re.sub(par_id, str(p_id_w_id_dic[int(par_id)]), string)
    return string

def check_for_mul_ids(ids):
    if '+' in ids:
        lst = ids.split('+')
        for each in lst:
            ids = replace_pid_with_id(ids, each)
    else:
            ids = replace_pid_with_id(ids, ids)
    return ids        



for line in open(sys.argv[2]):
    a = line
    if line != '\n':
        lst = line.strip().split()
        hids = lst[1].split(',')
        if '_info' in lst[0]:
            ids = lst[0].split('_')
            lst[0] = replace_pid_with_id(lst[0], ids[0])
            hids[0] = check_for_mul_ids(hids[0])
            lst[1] = hids[0]+','+','.join(hids[1:])
            line = lst[0] + ' ' + lst[1]
        if 'no_match_found' in lst[0]:
            lst[1] = check_for_mul_ids(lst[1])
            line = lst[0] + ' ' + lst[1]
        if 'manual_sen_length' in line:
            line = replace_pid_with_id(line.strip(), lst[2])
        print(line)
