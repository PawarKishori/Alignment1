import csv
import re
filename="debug_invert.csv"
rows=[]
with open(filename,'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)
lenr=len(rows)
list1=[]
for i in range(lenr):
    len2=len(rows[i])
    for j in range(len2):
        if(rows[i][0]=='"'):
            list1.append(rows[i])
        elif(len2==1):
            list1.append(rows[i])
        elif(len2>1):
            if('"' in rows[i][1]):
                list1.append(rows[i])
            if( "(" in rows[i][1]):
                list1.append(rows[i])
len1=len(list1)
print(list1)
list2=[]
for i in range(lenr):
    temp=0
    for j in range(len1):
        if(rows[i]==list1[j]):
            temp=1
            break
    if(temp==0):
        list2.append(rows[i])
list3=[]
for i in range(len(list2)):
    lenk=len(list2[i])
    if(lenk>1):
        list2[i].remove('"')
    lenk=len(list2[i])
    if(lenk>1):
        #print(list2[i])
        list3.append(list2[i])
len3=len(list3)
list4=[]
for i in range(len3):
    lenk=len(list3[i])
    #print(list3[i])
    for j in range(lenk):
        res=re.split(r'\s+',list3[i][j])
        #print(res)
        for k in range(len(res)):
            if res[k] != '':
                list3[i][j]=res[k]
    #print(list3[i])
lenf=len(list3)
print(list3)
with open('debug_csv.csv','w') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerows(list3)
