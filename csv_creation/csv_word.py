import re
import csv
log=open('file_missing_log','a')
flagfile=0
try:
    filename="H_alignment_parserid.csv"
    rows = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        #fields = csvreader.next()
        for row in csvreader:
            rows.append(row)
    lengthrows=len(rows)
except:
    flagfile=1
    log.write('H_alignment_parserid is missing\n')
list_AW=["A"]
list_LW=[]
list_MW=[]
list_KW=[]
list_OW=["O"]
list_NW=["N"]
list_PW=["P"]
list_P1W=["P1"]
list_DICTW=["DICT"]
list_RW=["R"]
if(flagfile==0):
    flagc=0
    flagid=0
    flagm=0
    flagcw=0
    flagr=0
    try:    #For A_Layer
        c=open('E_sentence','r').readlines()
        clen=len(c)
    except:
        flagc=1
        log.write('E_sentence is missing\n')

    try:    #For K_Layer
        idaw=open("id_Apertium_output_with_grp.dat","r").readlines()
        ilen=len(idaw)
    except:
        flagid=1
        log.write('id_Apertium_output_with_grp.dat is missing\n')

    try:   #For N_Layer to P1_Layer
        m=open('manual_lwg.dat','r').readlines()
        mlen=len(m)
    except:
        flagm=1
        log.write('manual_lwg.dat is missing\n')

    try:    #For DICT_LAYER
        cw=open('corpus_specific_dic_facts_for_one_sent.dat','r').readlines()
        cwlen=len(cw)
    except:
        flagcw=1
        log.write("corpus_specific_dic_facts_for_one_sent.dat is missing\n")

    try:    #For R_LAYER
        rw=open('R_layer_final_facts.dat','r').readlines()
        rwlen=len(rw)
    except:
        flagr=1
        log.write('R_layer_final_facts.dat is missing\n')
    for i in range(lengthrows):
        list_LW.append("_")
        list_MW.append("_")


    if(flagc==0):
    #A_Layer
        for i in range(clen):
            res=re.split(r'\s+',c[i])
            for j in range(len(res)-1):
                list_AW.append(res[j])

        print(list_AW)

    if(flagid==0):
    #K_Layer
        list1=rows[1]
        print(list1)
        length=len(list1)
        list_temp=["K"]
        for i in range(1,length):
            temp=0
            for j in range(ilen):
                res1=idaw[j][1:]
                res2=res1[:-3]
                res3=res2.rsplit()
                res=re.split(r'\s+',res2)
                length=len(res)
                if(length==2):
                    res.append(" ")
                if(length>3):
                    for k in range(3,length):
                        res[2]=res[2]+" "+res[k]
                temparray=res[0:3]
                
                #if(int(temparray[1])==int(list1[i])):
                if(temparray[1]==list1[i]):
                    temp=1
                    list_temp.append(temparray[2])
                    break
            if(temp==0):
                list_temp.append("_")

        list4=[]
        lentemp=len(list_temp)
        for i in range(lentemp):
            list4.append(" ")
            if('@PUNCT-OpenParen' in list_temp[i]):
                list4[i]=list_temp[i].replace("@PUNCT-OpenParen","(")
            elif('@PUNCT-ClosedParen' in list_temp[i]):
                list4[i]=list_temp[i].replace("@PUNCT-ClosedParen",")")
            else:
                list4[i]=list_temp[i]
            if('@PUNCT-OpenParen'in list4[i]):
                list4[i]=list4[i].replace("@PUNCT-OpenParen","(")
            if('@PUNCT-ClosedParen' in list4[i]):
                list4[i]=list4[i].replace("@PUNCT-ClosedParen",")")

            list_KW.append(list4[i])
        print(list_KW)


    #L_layer
    list_LW[0]="L"
    print(list_LW)

    #M_Layer
    list_MW[0]="M"
    print(list_MW)
    #N_Layer
    if(flagm==0):

        list1=rows[4]
        print(list1)
        n100=len(list1)
        for i in range(1,n100):
            temp=0
            for j in range(mlen):
                res1=m[j][1:]
                res2=res1[:-3]
                res=re.split(r'\)?\s+\(',res2)
                a=res[-1] #GROUP_ID
                b=res[2]  #WORDS
                res3=" ".join(a.split()[1:])  #GROUP_ID
                res4=" ".join(b.split()[1:])  #WORDS
                if(res3==list1[i]):
                    temp=1
                    list_NW.append(res4)
            if(temp==0):
                list_NW.append("_")
        print(list_NW)

        #O_Layer
        list1=rows[5]
        print(list1)
        n100=len(list1)
        for i in range(1,n100):
            temp=0
            for j in range(mlen):
                res1=m[j][1:]
                res2=res1[:-3]
                res=re.split(r'\)?\s+\(',res2)
                a=res[-1] #GROUP_ID
                b=res[2]  #WORDS
                res3=" ".join(a.split()[1:])  #GROUP_ID
                res4=" ".join(b.split()[1:])  #WORDS
                if(res3==list1[i]):
                    temp=1
                    list_OW.append(res4)
            if(temp==0):
                list_OW.append("_")
        print(list_OW)

        #P_Layer

        list1=rows[6]
        print(list1)
        n100=len(list1)
        for i in range(1,n100):
            temp=0
            for j in range(mlen):
                res1=m[j][1:]
                res2=res1[:-3]
                res=re.split(r'\)?\s+\(',res2)
                a=res[-1] #GROUP_ID
                b=res[2]  #WORDS
                res3=" ".join(a.split()[1:])  #GROUP_ID
                res4=" ".join(b.split()[1:])  #WORDS
                if(res3==list1[i]):
                    temp=1
                    list_PW.append(res4)
            if(temp==0):
                list_PW.append("_")
        print(list_PW)


        #P1_Layer
        list1=rows[7]
        print(list1)
        n100=len(list1)
        for i in range(1,n100):
            temp=0
            for j in range(mlen):
                res1=m[j][1:]
                res2=res1[:-3]
                res=re.split(r'\)?\s+\(',res2)
                a=res[-1] #GROUP_ID
                b=res[2]  #WORDS
                res3=" ".join(a.split()[1:])  #GROUP_ID
                res4=" ".join(b.split()[1:])  #WORDS
                if(res3==list1[i]):
                    temp=1
                    list_P1W.append(res4)
            if(temp==0):
                list_P1W.append("_")
        print(list_P1W)

    #DICT_LAYER
    if(flagcw==0):
        list1=rows[8]
        print(list1)
        n99=len(list1)
        for j in range(1,n99):
            temp=0
            for i in range(cwlen):
                res1=cw[i][:-3]
                res2=res1[1:]
                res=re.split(r'\)?\s\(',res2)
                a=res[3] #H_ID
                b=res[4] #H_Word
                res3=" ".join(a.split()[1:])#H_ID
                res4=" ".join(b.split()[1:])#H_Word
                if(list1[j]==res3):
                    temp=1
                    list_DICTW.append(res4)
            if(temp==0):
                list_DICTW.append("_")
        print(list_DICTW)

    #R_LAYER
    if(flagr==0):
        list1=rows[9]
        print(list1)
        n98=len(list1)
        for j in range(1,n98):
            temp=0
            for i in range(rwlen):
                res1=rw[i][:-3]
                res2=res1[1:]
                res=re.split(r'\)?\s\(',res2)
                a=res[3] #H_ID
                b=res[4] #H_Word
                res3=" ".join(a.split()[1:])#H_ID
                res4=" ".join(b.split()[1:])#H_Word
                if(list1[j]==res3):
                    temp=1
                    list_RW.append(res4)
            if(temp==0):
                list_RW.append("_")
        print(list_RW)
        print(len(list_RW))


with open('H_alignment_parserword.csv','w') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(list_AW)
    csvwriter.writerow(list_KW)
    csvwriter.writerow(list_LW)
    csvwriter.writerow(list_MW)
    csvwriter.writerow(list_NW)
    csvwriter.writerow(list_OW)
    csvwriter.writerow(list_PW)
    csvwriter.writerow(list_P1W)
    csvwriter.writerow(list_DICTW)
    csvwriter.writerow(list_RW)
log.close()
