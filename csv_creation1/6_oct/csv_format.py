import csv
import re
log=open('file_missing_log1','w')
flag=0
flag4=0
flag5=0
flag6=0
flag7=0
flag8=0
flag9=0
flagg=0
flag10=0
flag11=0
flag12=0
flag13=0
flag14=0
flag15=0
flag16=0

try:
    f=open("word.dat",'r').readlines()
    n=len(f)-1
except:
    flag=1
    log.write("E_id_word_dictionary.dat not found\n")

try:
    f4=open("parser_alignment.dat",'r').readlines()
except:
    flag4=1
    log.write("parser_alignment.dat not found\n")
try:
    f5=open("word_alignment_tmp.dat",'r').readlines()
except:
    flag5=1
    log.write("word_alignment_tmp.dat not found\n")
try:
    f6=open("word_alignment.dat",'r').readlines()
except:
    flag6=1
    log.write("word_alignment.dat not found\n")
try:
    f7=open("corrected_pth.dat",'r').readlines()
except:
    flag7=1
    log.write("corrected_pth.dat not found\n")
try:
    f8=open("corpus_specific_dic_facts_for_one_sent.dat",'r').readlines()
except:
    flag8=1
    log.write("corpus_specific_dic_facts_for_one_sent.dat not found\n")
try:
    f9=open("R_layer_final_facts.dat",'r').readlines()
except:
    flag9=1
    log.write("R_layer_final_facts.dat not found\n")
try:
    g=open("manual_lwg.dat",'r').readlines()
    glen=len(g)
except:
    flagg=1
    log.write("manual_lwg.dat not found\n")
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
    f12=open("vibhakti", "r").read()
except:
    flag12=1
    log.write("vibhakti file not found\n")
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
   

list_A=['A']
list_K=['K']
list_L=['L']
list_M=['M']
list_N=['N']
list_O=['O']
list_P=['P']
list_P1=['P1']
list_DICT=['DICT']
list_R=['R']
list_K_partial=['K_par']
list_K_Root=['K_Root']
list_K_Dic=['K_Dic']
list_K_ex_without_vib=['K_exact_without_vib']

for i in range(n):
    list_A.append("_")
    list_K.append("_")
    list_L.append("_")
    list_M.append("_")
    list_N.append("_")
    list_O.append("_")
    list_P.append("_")
    list_P1.append("_")
    list_DICT.append("_")
    list_R.append("_")
    list_K_partial.append("_")    
    list_K_Root.append("_")    
    list_K_Dic.append("_")    
    list_K_ex_without_vib.append("_")    

wrd_dic= {}

if(flag==0):
    for i in range(1,n+1):

        word=re.split(r'\s+',f[i-1].rstrip())
        # print 'word is ', word
        list_A[i]=word[1] #A_Layer
        if word[1] not in wrd_dic.keys():
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
for key in sorted(m_root_dic):
	print(str(key) + '\t' + m_root_dic[key])

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
                    if wrd_id not in k_dic.keys() and wrd in m_dic.keys():
                        k_dic[wrd_id] = str(m_dic[wrd])
#                        print '$$$', wrd, wrd_id, k_dic[wrd_id], m_dic[wrd]
                    elif wrd_id in k_dic.keys() and wrd in m_dic.keys():
                        if ' ' not in k_dic[wrd_id] and '/' not in str(m_dic[wrd]):
#                            print '&&',  k_dic[wrd_id], m_dic[wrd], wrd, m_dic.keys(), m_dic.values()
                            o = check_for_consecutive_ids(k_dic[wrd_id], m_dic[wrd])
                            store_data_in_k_dic(wrd_id, o, k_dic[wrd_id], str(m_dic[wrd]))
                        elif '/' not in str(m_dic[wrd]):
#                            print '^^', k_dic[wrd_id], m_dic[wrd], wrd, m_dic.keys(), m_dic.values()
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
                print('1111', ap_out[2:])

##===================
#Return key for a known value:
def return_key(val, dic):
    for key in dic:
        if val == dic[key]:
            return key
        elif val in dic[key].split('/'):
            return key

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
def check_for_vib(m_mng, vib):
    if m_mng not in vib:
        return True
##===================
def check_for_root(a_root, m_root):
	if a_root == m_root :
		return True
	elif m_root in a_root.split():
		return True

##===================
database_dic = {}
if(flag16 == 0):
    for line in f16:
        lst = line[:-2].split()
        if 'default-iit-bombay-shabdanjali-dic_smt.gdbm' in line.strip():
            if(lst[4] == 'default-iit-bombay-shabdanjali-dic_smt.gdbm'):
                for key in sorted(wrd_dic):
                    if(wrd_dic[key] == lst[3]):
                        add_data_in_dic(database_dic, key, lst[5])
                        
##===================
#To handle hE/hEM etc. using tam info. If this is part of tam then restricting them to display in partial layer.
tam_dic = {}
restricted_wrds = ['hE', 'hEM', 'WA', 'WIM', 'WI']
if(flag13==0):
    for line in f13:
        if line.startswith('(pada_info'):
            t = re.split(r'\)', line.strip())
            key =  t[0].split()[-1]
            tam_info = t[8].split('_')[-1]
            if tam_info in restricted_wrds:
                tam_dic[int(key)] = 'yes'

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
                print('Manual_mng is', man_mng)
                out = check_for_vib(man_mng, f12)
                if out == True:
                    if man_mng not in restricted_wrds:
                        print('K exact without vib', anu_mng, man_mng, ' '.join(ids), int(ap_out[1]))
                        k_ex_without_vib_dic[int(ap_out[1])] = ' '.join(ids)
                    elif man_mng in restricted_wrds and int(ap_out[1]) not in tam_dic.keys():
                        print(man_mng, int(ap_out[1]))
                        print('partial', anu_mng, man_mng, ' '.join(ids), int(ap_out[1]))
                        k_par_dic[int(ap_out[1])] = ' '.join(ids)
                    else:
                        k_par_dic[int(ap_out[1])] = '-'
        ############ K Root code            
        if int(ap_out[1]) in a_root_dic.keys():
            a_root = a_root_dic[int(ap_out[1])]
            for key in sorted(m_root_dic):
                if key == a_root:
                        out = check_for_vib(a_root, f12)
			#print a_root, out, key
                        if(out == True):
                            k_rt[int(ap_out[1])] = m_root_dic[key] 
                elif key in a_root.split():
                        out = check_for_vib(key, f12)
			#print m_root_dic[key], out, key
                        if out == True:
                            k_rt[int(ap_out[1])] = m_root_dic[key]
        ############ K Dic code            
        if(ap_out[1]) in database_dic.keys():
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

if(flag4==0):
    n4=len(f4)
    for i in range(n4):#N_Layer

        f4[i]=f4[i].rstrip()[:-1]
        f4[i]=f4[i][1:]

        column=re.split(r'\)?\s\(',f4[i])
        column[4]=column[4][:-1]


        a_id=re.split(r'\s',column[1])

        man_id=re.split(r'\s',column[2])

        res=""
        flagg=0
        try:
            g=open("manual_lwg.dat",'r').readlines()
        except:
            flagg=1
            log.write("manual_lwg.dat not found")
        glen=len(g)
        for j in range(glen):

            g[j]=g[j].rstrip()[:-1]
            g[j]=g[j][1:]

            new=re.split(r'\)?\s\(',g[j])
            new[4]=new[4][:-1]
            h_id=re.split(r'\s',new[1])
            if man_id[1]==h_id[1]:
                res=new[10]
                break

        res=res[:-1]
        res=" ".join(res.split()[1:])
        if res=="":
            res=man_id[1]
            log.write("Issue with parser_alignment.dat: man_id " + man_id[1]+" not found in manual_lwg.dat")
        list_N[int(a_id[1])]=res


flagg=0
try:
    g=open("manual_lwg.dat",'r').readlines()
    glen=len(g)
except:
    flagg=1
    log.write("manual_lwg.dat not found")



if(flag5==0):
    n5=len(f5)
    for i in range(n5): #O_Layer
      res=re.split(r'\s+',f5[i].rstrip())
      number1=res[4][:-1]  #Man_ID
      number2=res[2][:-1]  #ANu_ID
      temp=0
      for j in range(glen):
          res1=re.split(r'\s+',g[j].rstrip())
          number3=res1[2][:-1]
           #print(number3)
          if(int(number1)==int(number3)):
              temp=1
              str1=[]
              m=len(res1)
              for k in range(1,m):
                  k=k*-1
                  if(res1[k]=='(group_ids'):
                      break
                  else:
                      y=k*-1
                      if(y==1):
                          res1[k]=res1[k][:-2]
                      str1.append(res1[k])
              str1.reverse()
              lenstr=len(str1)
              a=""
              for m in range(lenstr):
                  a=a+str1[m]+" "
               #print(a)
              for l in range(n+1):
                  if(int(l)==int(number2)):
                          a=a[:-1]
                          list_O[l]=a
                          #print(list_O[l])
      if(temp==0):
          for l in range(n+1):
              if(int(l)==int(number2)):
                  list_O[l]=number1
    print(list_O)


if(flag6==0):#P_Layer
    n6=len(f6)
    for i in range(n6):
        res1=f6[i][1:]
        res2=res1[:-2]
        res3=re.split(r'-',res2)
        length=len(res3)
        anu_id=re.split(r'\s+',res3[4])[1]
        str1=""
        str2=""
        if(length>6):
            for j in range(5,length):
                if(res3[j]!=' '):
                    str1=str1+res3[j]+"-"
            str2=str1[:-1]
        elif(length==6):
            str2=res3[5]
        str3=str2[1:]
        myre=re.split(r'\s+',str3)
        try:
            myre.remove("-")
        except:
            print(" ")
        abc=len(myre)
        print(myre)
        print(abc)
        str5=""
        for k in range(1,abc):
            str5=str5+myre[k]+" "
        man_id=myre[0]
        str4=str5[:-1]
        print(str4)
        for j in range(glen):
            res11=g[j][:-3]
            res12=res11[1:]
            res13=re.split(r'\)?\s\(',res12)
            res14=re.split(r'\s',res13[1])[-1]
            res15=res13[-1]
            res16=re.split(r'\s+',res15)
            length1=len(res16)
            str10=""
            for k in range(1,length1):
                str10=str10+res16[k]+" "
            if(res14==man_id):
                if('@PUNCT-OpenParen@PUNCT-OpenParen'in str4 and abc==2):
                    print("")
                else:
                    for k in range(1,n+1):
                        if(int(anu_id)==int(k)):
                            list_P[k]=str10[:-1]


flagg=0
try:
    g=open("manual_lwg.dat",'r').readlines()
    glen=len(g)
except:
    flagg=1
    log.write("manual_lwg.dat not found")




if(flag7==0):
    n7=len(f7)
    for i in range(n7): #P1_Layer
       res=f7[i][:-3]
       res1=res[1:]
       res2=re.split(r'\)?\s+\(',res1)
       res3=res2[-1]#for Group_ID
       res4=res2[1]# for Anu_ID
       res5=re.split('\s+',res3)
       res6=re.split('\s+',res4)[1]
       #print(res6)
       #print(res5[1])
       m1=len(res5)
       m2=len(res6)
       str1=""
       for j in range(m1):
           if(j!=0):
               str1=str1+res5[j]+" "
       #print(str1)
       for k in range(n+1):
           if(int(k)==int(res6)):
               str1=str1[:-1]
               list_P1[k]=str1
    print(list_P1)


if(flag8==0):
    n8=len(f8)
    for i in range(n8):#DICT Layer
        res=f8[i][1:]
        res1=res[:-3]
        res2=re.split(r'\)?\s\(',res1)
        id1=re.split('\s+',res2[3])    #H_id
        id2=re.split('\s+',res2[1])    #E_id
        print(id1)
        m1=len(id1)
        m2=len(id2)
        str1=""
        for j in range(m1):
            if(j!=0):
                str1=str1+id1[j]+" "
        number=id2[-1]
        for k in range(n):
           #print("1")
            if(int(k)==int(number)):
                str1=str1[:-1]
                list_DICT[k]=str1
    print(list_DICT)


if(flag9==0):
    n9=len(f9)
    for i in range(n9):#R Layer
        res=f9[i][1:]
        res1=res[:-3]
        res2=re.split(r'\)?\s\(',res1)
        id1=re.split('\s+',res2[3])    #H_id
        id2=re.split('\s+',res2[1])    #E_id
        print(id1)
        m1=len(id1)
        m2=len(id2)
        str1=""
        for j in range(m1):
            if(j!=0):
                str1=str1+id1[j]+" "
        number=id2[-1]
        for k in range(n):
           #print("1")
            if(int(k)==int(number)):
                str1=str1[:-1]
                list_R[k]=str1
    print(list_R)
log.close()

with open("H_alignment_parserid-new.csv", 'w') as csvfile:

    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(list_A)
    csvwriter.writerow(list_K)
    csvwriter.writerow(list_K_ex_without_vib)
    csvwriter.writerow(list_K_partial)
    csvwriter.writerow(list_K_Root)
    csvwriter.writerow(list_K_Dic)
    csvwriter.writerow(list_L)
    csvwriter.writerow(list_M)
    csvwriter.writerow(list_N)
    csvwriter.writerow(list_O)
    csvwriter.writerow(list_P)
    csvwriter.writerow(list_P1)
    csvwriter.writerow(list_DICT)
    csvwriter.writerow(list_R)
