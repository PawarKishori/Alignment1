import sys, re

e_sent = []
for line in open(sys.argv[1]):
    lst = line[:-2].split()
    e_sent.append(lst[1]+'_'+lst[2])

print('English_Words'+'\t'+'\t'.join(e_sent))
length = len(e_sent)

K_layer_info_dic = {}

K_layer_info = []
for line in open(sys.argv[2]):
    lst = line[:-2].strip().split()
    mng = lst[2:]
    if '@PUNCT-OpenParen' in mng:
        mng = re.sub('@PUNCT-OpenParen@PUNCT-OpenParen', '((', mng)
    if '@PUNCT-ClosedParen' in mng:
        mng = re.sub('@PUNCT-ClosedParen@PUNCT-ClosedParen', '))', mng)
    if len(lst) <= 2:    
        mng = '-'
    K_layer_info_dic[int(lst[1])] =  ' '.join(mng)



for i in range(0, length):
    if i+1 in K_layer_info_dic.keys():
        K_layer_info.append(str(i+1)+'_'+ K_layer_info_dic[i+1])
    else:
        K_layer_info.append('-')

print('Anusaaraka Translation' +'\t' + '\t'.join(K_layer_info)), 
           







