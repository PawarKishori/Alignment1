import csv
import re
log=open('file_missing_log','a')
flag=0
flag4=0
flag5=0
flag6=0
flag7=0
flag8=0
flag9=0
flagg=0
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


if(flag==0):
    for i in range(1,n+1):

        word=re.split(r'\s+',f[i-1].rstrip())
        list_A[i]=word[1] #A_Layer

    for i in range(1,n+1):

        word=re.split(r'\s+',f[i-1].rstrip())
        list_K[i]=word[1] #K_Layer



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

with open("H_alignment_parserid.csv", 'w') as csvfile:

    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(list_A)
    csvwriter.writerow(list_K)
    csvwriter.writerow(list_L)
    csvwriter.writerow(list_M)
    csvwriter.writerow(list_N)
    csvwriter.writerow(list_O)
    csvwriter.writerow(list_P)
    csvwriter.writerow(list_P1)
    csvwriter.writerow(list_DICT)
    csvwriter.writerow(list_R)
