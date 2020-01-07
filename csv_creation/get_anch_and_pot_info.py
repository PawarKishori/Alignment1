#Writtem by Roja(02-01-2020)
#Programme to decide type of anchors using slot_debug_info.txt
#RUN: python3 ~/Alignment1/csv_creation/get_anch_and_pot_info.py slot_debug_input.txt word.dat  manual_id_mapped.dat  > anchor.dat
################################################################################
import sys, re

from functions import unique_val
from functions import add_data_in_dic
#from functions import return_key


m_info_dic = {}
wrd_f = open(sys.argv[2], 'r').readlines()
wrd_len = len(wrd_f)

hwrd_f = open(sys.argv[3], 'r').readlines()
hwrd_len = len(hwrd_f)

def return_index(lst, val):
    index = []
    for i in range(len(lst)):
        if '/' in lst[i]:
            item = lst[i].split('/')
            for each in item:
                if val == each:
                    index.append(i)
        elif val == lst[i]:
            index.append(i)
    return(index)

e_lst = []
g_lst = []
h_lst = []

#Function to define array with a specified length
def define_array(lst, length):
    lst = []
    for i in range(0, length-1):
        lst.append('')
    return lst    
 
e_lst = define_array(e_lst, wrd_len) 

for line in open(sys.argv[1]):
    if '_info' in line.strip():
        lst = line.strip().split()
        hid = lst[0][:-5]
        wrdid = lst[1].split(',')[0]
        col = lst[1].split(',')[1]
        val = col + '_' + wrdid
        if val not in e_lst:
            if e_lst[int(col)-1] == '':
                e_lst[int(col)-1] =  wrdid
            else:
                if wrdid not in e_lst[int(col)-1].split('/'):
                    e_lst[int(col)-1] =  e_lst[int(col)-1] + '/' + wrdid
    if 'no_match_found' in line.strip():
        lst = line.strip().split()
        print('(no_match_found', lst[1], ')')

#print(e_lst)
g_lst = define_array(g_lst, hwrd_len+1)

for line in open(sys.argv[1]):
    if '_info' in line.strip():
        lst = line.strip().split()
        hid = lst[0][:-5]
        wrdid = lst[1].split(',')[0]
        col = lst[1].split(',')[1]
        g_lst[int(hid)-1] = wrdid



#To print hindi group head and ids
for i in range(0, len(g_lst)):
    lst = g_lst[i].split('+')
    if lst != ['']:
        print('(hindi_head_id-grp_ids', i+1 , ' '.join(lst), ')')

new_lst  = e_lst


for i in range(0, len(e_lst)):
    if '+' in e_lst[i]:
        if '/' not in e_lst[i]:
            out = return_index(g_lst, e_lst[i])
            new_lst[i] = str(out[0]+1)
        else:
            lst = e_lst[i].split('/')
            j = []
            for each in lst:
                if '+' in each:
                    out = return_index(g_lst, each)
                    j.append(str(out[0]+1))
                else:
                    j.append(each)
            new_lst[i] = '/'.join(j)        
           

#new_lst after renaming with group head ids: new_lst
#print('Eng_lst after reanaming with grp ids', new_lst)

h_lst = g_lst 
#to get h_lst
for i in range(1, hwrd_len):
    out = return_index(new_lst, str(i))
    j = []
    for each in out :
        j.append(str(each+1))
    h_lst[i-1] = '/'.join(j)   

#print('Eng lst', e_lst)
#print('Hindi lst', h_lst)

#Deciding Anchors and potential facts 
anc_lst = [] 
for i in range(0, wrd_len-1):
    lst = new_lst[i].split('/')
    if lst != ['']:
        if len(lst) == 1 :
            lst1 = h_lst[int(lst[0])-1].split('/')
            if len(lst1) == 1:
                print('(iter-type-eng_g_id-h_g_id 1 anchor', i+1, ' '.join(lst), ')')
            else:
                print('(iter-type-eng_g_id-h_g_id 1 potential', i+1, ' '.join(lst), ')')
        else:
            print('(iter-type-eng_g_id-h_g_id 1 potential', i+1, ' '.join(lst), ')')
        anc_lst.append(','.join(lst))
    else:
        anc_lst.append('0')

print('(iter-h_g_id ',  1, ' '.join(anc_lst), ')')

    
