import csv
import re
log=open('file_missing_log','a')
filename="H_alignment_parserid.csv"
rows = []
flagfile=0
flagparse=0
try:
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        #fields = csvreader.next()
        for row in csvreader:
            rows.append(row)
except:
    flagfile=1
    log.write("H_alignment_parserid.csv not found:PLEASE TRY RUNNING csv_format.py\n")

try:
    parse=open('H_parserid-wordid_mapping.dat','r').readlines()
    prlen=len(parse)
except:
    flagparse=1
    log.write("H_parserid-wordid_mapping.dat not found\n")
list1=[]#Parse_ID
list2=[]#Word_ID
if(flagparse==0):
    for i in range(prlen):
        parse[i]=parse[i][:-2]
        parse[i]=parse[i][1:]
        res=re.split(r'\t',parse[i])
        res[1]=res[1].replace('P','')
        list1.append(res[1])
        list2.append(res[2])
    print(list1)
    print(list2)
    n=len(rows)
    print(n)
    for i in range(2,n):
        #print(rows[i])
        print(i)
        len1=len(rows[i])
        print(len1)
        for j in range(1,len1):
            #print(rows[i][j])
            if(rows[i][j]!='_'):
                id=re.split(r'\s+',rows[i][j])
                length=len(id)
                final=""
                try:
                    if(length>1):
                        for k in range(length):
                            #print(id[k])
                            id[k]=list2[list1.index(id[k])]
                            final=final+id[k]+' '
                        rows[i][j]=final
                        #print(id)
                        #print(final)

                    else:
                        print(rows[i][j])
                        rows[i][j]=list2[list1.index(rows[i][j])]
                except:
                    log.write("punctuation error \n")
                    break

        #print(rows[i])
    print(rows)
    filename1="H_alignment_wordid.csv"
    with open(filename1,'w') as csvfile:
        csvwriter=csv.writer(csvfile)
        csvwriter.writerows(rows)
log.close()
