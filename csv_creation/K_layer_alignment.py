import sys, re 
import csv
log=open('K_log','w')

flag=0
flag10=0
flag11=0
flag12=0
flag13=0
flag14=0
flag15=0
flag16=0
flag17=0

try:
    f=open("word.dat",'r').readlines()
    n=len(f)-1
except:
    flag=1
    log.write("word.dat not found\n")
try:
    f10=open("H_wordid-word_mapping.dat","r").readlines()
except:
    flag10=1
    log.write("H_wordid-word_mapping.dat not found\n")
try:
    f11=open("id_Apertium_output.dat", "r").readlines()
except:
    flag11=1
    log.write("id_Apertium_output.dat not found\n")
try:
    f12=open(sys.argv[1], "r").read()
except:
    flag12=1
    log.write(sys.argv[1],"file not found\n")
try:
    f13=open("GNP_agmt_info.dat", "r").readlines()
except:
    flag13=1
    log.write("GNP_agmt_info.dat not found")
try:
    f14=open("anu_root.dat", "r").readlines()
except:
    flag14=1
    log.write("anu_root.dat not found")
try:
    f15=open("H_headid-root_info.dat", "r")
except:
    flag15=1
    log.write("H_headid-root_info.dat not found") 
try:
    f16=open("database_mng.dat", "r")
except:
    flag16=1
    log.write("database_mng.dat not found")   
try:
    f17=open("revised_root.dat", "r")
except:
    flag17=1
    log.write("revised_root.dat not found")   


list_A=['A']
list_K=['K']
list_K_partial=['K_par']
list_K_Root=['K_Root']
list_K_Dic=['K_Dic']
list_K_ex_without_vib=['K_exact_without_vib']

for i in range(n):
    list_A.append("_")
    list_K.append("_")
    list_K_partial.append("_")
    list_K_Root.append("_")
    list_K_Dic.append("_")
    list_K_ex_without_vib.append("_")

wrd_dic= {}

if(flag==0):
    for i in range(1,n+1):
        word=re.split(r'\s+',f[i-1].rstrip())
        #print('word is ', word[1])
        list_A[i]=word[1] #A_Layer
        if word[1] not in wrd_dic.keys():
            #print word[1]
            wrd_dic[word[1]] = word[2][:-1]


######## Displaying K layer and K layer partial, K layer root . Added by Roja
m_dic = {}
k_dic = {}
k_par_dic = {}
a_root_dic = {}
m_root_dic = {}
##===================
def add_data_in_dic(dic, key, val):
    if key not in dic:
        dic[key] = val
    elif(val not in dic[key].split('/')):
        dic[key] = dic[key] + '/' + val

##===================
if(flag10==0):
    for i in f10:
        hword=re.split(r'\s+',i[:-2])
        add_data_in_dic(m_dic, hword[2], hword[1])
##===================
if(flag14==0):
    for i in f14:
        root=re.split(r'\s+',i[:-2])
        add_data_in_dic(a_root_dic, int(root[1]), root[2])
##===================
if(flag15==0):
    for i in f15:
        root=re.split(r'\s+',i[:-2])
        #add_data_in_dic(m_root_dic, int(root[1]), root[2])
        add_data_in_dic(m_root_dic, root[2], root[1])

##===================
#for key in sorted(m_root_dic):
#	print(key + '\t' + m_root_dic[key])

##===================
#Return key for a known value:
def return_key(val, dic):
    for key in dic:
        if val == dic[key]:
            return key
        elif val in dic[key].split('/'):
            return key
##===================
def check_for_vib(m_mng, vib):
    if m_mng not in vib:
        return True
##===================
def check_for_consecutive_ids(ids, id2):
    if '/' in ids:
        ids_lst = ids.split('/')
    elif ' ' in ids:
        ids_lst = ids.split('/')
    else:
        if int(ids) + 1 == int(id2) :
            return True
    for each in ids_lst:
        if ' ' in each:
            ides = each.split()
            if int(id2) == int(ides[-1]) + 1:
        #        print 'True' + ' ' + ' '.join(ids_lst)
                return 'True' + ' ' + ' '.join(ids_lst)
        else:
            if int(id2) == int(each) + 1:
                out = 'True' + ' ' + each 
                return out
            if int(id2) == int(each) + 2:  #anuvAxa kI [guNavawwA]
                mid_id = int(each) + 1  #kI
                m_mng = return_key(str(mid_id), m_dic)
                o =  check_for_vib(m_mng, f12)
                if o != True:               
                    out = 'True' + ' ' + each #Even if vib is not matched moving to next wrd and checking 
                    return out

##===================
#print in k_dic
def store_data_in_k_dic(key, inp, val1, val2):
        if inp == True:
            k_dic[key] = val1 + ' ' + val2
        elif 'True' in inp.split():
            k_dic[key] = ' '.join(inp.split()[1:]) + ' ' + val2

##===================
if(flag11==0):
    for i in f11:
        ap_out=re.split(r'\s+', i[:-2].strip())
        mngs = []
        try:
            if(len(ap_out) > 2):
                for each in ap_out[2:]:
                    k_mng = re.sub(r'[_-]', ' ', each) #parvawa_pafkwi
                    k_mng = re.sub(r'@', '' , k_mng) #@1000                        
                    l = k_mng.split()
                    for item in l:
                        mngs.append(item)
                for wrd in mngs:
                    wrd_id = int(ap_out[1]) #to get eng_wrd_id in id_Apertium_output
                    #print wrd, wrd_id, k_dic.keys()
                    if wrd_id not in k_dic.keys() and wrd in m_dic.keys():  #Initial storage of wrd_id in k_dic
                        k_dic[wrd_id] = str(m_dic[wrd])
#                        print('$$$', wrd, wrd_id, k_dic[wrd_id], m_dic[wrd])
                    elif wrd_id in k_dic.keys() and wrd in m_dic.keys():
                        if ' ' not in k_dic[wrd_id] and '/' not in str(m_dic[wrd]):
#                            print('&&',  k_dic[wrd_id], m_dic[wrd], wrd, m_dic.keys(), m_dic.values())
                            o = check_for_consecutive_ids(k_dic[wrd_id], m_dic[wrd])
                            store_data_in_k_dic(wrd_id, o, k_dic[wrd_id], str(m_dic[wrd]))
                        elif '/' not in str(m_dic[wrd]):
#                            print('^^', k_dic[wrd_id], m_dic[wrd], wrd, m_dic.keys(), m_dic.values())
                            o = check_for_consecutive_ids(k_dic[wrd_id], m_dic[wrd])
                            store_data_in_k_dic(wrd_id, o, k_dic[wrd_id], str(m_dic[wrd]))
                        else:
                   #         print k_dic[wrd_id], m_dic[wrd], wrd
                            if '/' not in k_dic[wrd_id]:
                                a = k_dic[wrd_id].split()
                                if str(int(a[-1])+1) in  m_dic[wrd].split('/'):
                                    o = check_for_consecutive_ids(k_dic[wrd_id], int(a[-1])+1)
                                    store_data_in_k_dic(wrd_id, o, k_dic[wrd_id], str(int(a[-1])+1))
                            a = k_dic[wrd_id].split('/') #Ex: 2.9, sWAna se 
#                            print '##', a
                            for each in a:
                                if ' ' in each :
                                    each = each[-1]
                                if str(int(each)+1) in  m_dic[wrd].split('/'):
                                        o = check_for_consecutive_ids(each, int(each)+1)
                                        store_data_in_k_dic(wrd_id, o, each, str(int(each)+1))

        except:
#            else:
                log.write('Check this mng::,')
                log.write(str(ap_out[2:]))
                #print('1111', ap_out[2:])

##===================
#return manual mngs:
def return_mng(ids, dic):
    mng = []
    if '/' in ids:
#        print '$$$Ids are ',ids 
        a = re.sub('/', ' ', ids)
    for each in ids:
        m = return_key(each, dic)
#        print each, m , dic.values()
        if m!= None:
            mng.append(m)
    return ' '.join(mng)

##===================
def check_for_root(a_root, m_root):
	if a_root == m_root :
		return True
	elif m_root in a_root.split():
		return True

##===================
anu_rt_dic = {}
if(flag17 == 0):
    for line in f17:
        lst = line.strip().split()
        add_data_in_dic(anu_rt_dic, lst[1], lst[2])  

##===================
database_dic = {}
if(flag16 == 0):
    for line in f16:
        lst = line[:-2].split()
        if 'default-iit-bombay-shabdanjali-dic_smt.gdbm' in line.strip():
            if(lst[4] == 'default-iit-bombay-shabdanjali-dic_smt.gdbm'):
                #for key in sorted(wrd_dic):
                for key in sorted(anu_rt_dic):
                    if(anu_rt_dic[key] == lst[3]):
                        add_data_in_dic(database_dic, key, '_'.join(lst[5:]))  
                        
##===================
#To handle hE/hEM etc. using tam info. If this is part of tam then restricting them to display in partial layer.
tam_dic = {}
restricted_wrds = ['hE', 'hEM', 'WA', 'WIM', 'WI', 'nahIM']
if(flag13==0):
    for line in f13:
        if line.startswith('(pada_info'):
            t = re.split(r'\)', line.strip())
            key =  t[0].split()[-1]
            print(key, t[8][8:])
            tam = t[8][8:]
            if tam != '0':
                tam_dic[int(key)] = 'yes'
#            tam_info = t[8].split('_')[-1]
#            if tam_info in restricted_wrds:
#                tam_dic[int(key)] = 'yes'

#print tam_dic.keys()
##===================
new_k_dic = {}
k_rt = {}
k_database_dic = {}
k_ex_without_vib_dic = {}

for i in f11:
    
    ap_out=re.split(r'\s+', i[:-2].strip())
    if(len(ap_out) > 2):
        if int(ap_out[1]) in k_dic.keys():
            ids = k_dic[int(ap_out[1])].split()
            mngs = []
            for each in ap_out[2:]:
                k_mng = re.sub(r'_', ' ', each)
                k_mng = re.sub(r'@', '', k_mng)  #@1000
                mngs.append(k_mng)
            anu_mng = ' '.join(mngs)
            man_mng = return_mng(ids, m_dic)
            #print(anu_mng)
            ############ K Exact code            
            if anu_mng == man_mng:
                new_k_dic[int(ap_out[1])] = ' '.join(ids)
                print('Exact', anu_mng)
            ############ K partial code            
            else:
#                print('Manual_mng is', man_mng)
                out = check_for_vib(man_mng, f12)
                if out == True:
#                    print('%%', man_mng, '**', anu_mng, tam_dic.keys())
                    if man_mng not in restricted_wrds:
                        if len(man_mng.split()) == len(mngs): #Counter ex: ai2E/2.83 , ai1E/2.15, So wrote this if else condition 
                            print('K exact without vib', anu_mng, man_mng, ' '.join(ids), int(ap_out[1]))
                            k_ex_without_vib_dic[int(ap_out[1])] = ' '.join(ids)
                        elif int(ap_out[1]) not in tam_dic.keys():
#                            print('Testing::', anu_mng, '&&', man_mng)
                            print('partial', anu_mng, man_mng, ' '.join(ids), int(ap_out[1]))
                            k_par_dic[int(ap_out[1])] = ' '.join(ids)
#                    elif man_mng in restricted_wrds and int(ap_out[1]) not in tam_dic.keys() and man_mng != 'nahIM': #Added nahIM for ai1, 2.19 (need to improve)
#                        print('partial', anu_mng, man_mng, ' '.join(ids), int(ap_out[1]))
#                        k_par_dic[int(ap_out[1])] = ' '.join(ids)
                    else:
                        k_par_dic[int(ap_out[1])] = '-'
        ############ K Root code            
        if int(ap_out[1]) in a_root_dic.keys():
            a_root = a_root_dic[int(ap_out[1])]
            ar = []
            for key in sorted(m_root_dic):
                k = key.split('/')
                if '_' in a_root: 
                    ar = a_root.split('_')
                if a_root in k:
                        out = check_for_vib(a_root, f12)
			#print a_root, out, key
                        if(out == True):
                            k_rt[int(ap_out[1])] = m_root_dic[key]
                elif ar != [] and len(k) == 1:   #Ex: ar =  ['sahAyawA', 'kara'], k = ['sahAyawA'] (ai1E , 2.51)
                    if k[0] in ar and k[0] not in restricted_wrds: # ar = ['nahIM', 'jAna'], k = ['nahIM'] (ai1E, 2.25)
                       out = check_for_vib(k[0], f12)
                       if(out == True):
                            k_rt[int(ap_out[1])] = m_root_dic[key]
                else:
                    for each in k:
                        if each in ar:
                            out = check_for_vib(each, f12)
		#	    print '%%%%', m_root_dic[key], out, k
                            if out == True:
                                k_rt[int(ap_out[1])] = m_root_dic[key]
        ############ K Dic code            
        if(ap_out[1]) in database_dic.keys():
            #print('%%', ap_out[1])
            for key in sorted(m_root_dic):
                if(key in database_dic[ap_out[1]].split('/')):
                    k_database_dic[int(ap_out[1])] = m_root_dic[key]

##====================
#for key in sorted(database_dic):
#    print key + '\t' + database_dic[key]   
##====================
#Store data in list_K
for i in range(1, n+1):
    if i in new_k_dic.keys():
        list_K[i] = new_k_dic[i]
    else:
        list_K[i] = '-'
##===================
#Store data in list_K_exact_without_vibhakti
for i in range(1, n+1):
    if i in k_ex_without_vib_dic.keys():
        list_K_ex_without_vib[i]  = k_ex_without_vib_dic[i] 
    else:
        list_K_ex_without_vib[i] = '-'
##===================
#Store data in list_K_partial:
for i in range(1, n+1):
    if i in k_par_dic.keys():
        list_K_partial[i] = k_par_dic[i]
    else:
        list_K_partial[i] = '-'
##===================
#Store data in list_K_Root:
for i in range(1, n+1):
    if i in k_rt.keys():
        list_K_Root[i] = k_rt[i]
    else:
        list_K_Root[i] = '-'
##===================
#Store data in list_K_Dict:
for i in range(1, n+1):
    if i in k_database_dic.keys():
        list_K_Dic[i] = k_database_dic[i]
    else:                
        list_K_Dic[i] = '-'
##===================
print('Kth Layer Exact info::\n', list_K)
print('Kth Layer Exact without vib::\n', list_K_ex_without_vib)
print('Partial K layer info::\n', list_K_partial)
print('Root K layer info::\n', list_K_Root)
print('Dict K layer info::\n', list_K_Dic)

m_dic = {}
k_dic = {}
new_k_dic = {}
k_par_dic = {}
k_database_dic = {}

############# Added by Roja Ended    

log.close()

with open("K_alignment_wordid.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(list_A)
    csvwriter.writerow(list_K)
    csvwriter.writerow(list_K_ex_without_vib)
    csvwriter.writerow(list_K_partial)
    csvwriter.writerow(list_K_Root)
    csvwriter.writerow(list_K_Dic)

