import re
file=open('BUgol2.1E_table','r').readlines()
filelen=len(file)
g=open('BUgol2.1E_table2','w')
print(filelen)
f=open('H_parserid-wordid_mapping.dat','r').readlines()
flen=len(f)
print(flen)
for line in file:
    if(re.match('^<b>',line)):
        print(line)
        res=re.split(r'<FONT COLOR=purple>',line)#Splits Font_Color=Purple
        #print(res[1])
        res1=re.split(r'<FONT COLOR=brown>',res[1])#Splits Font_Color=Brown
        lenres1=len(res1)
        for j in range(1,lenres1):
            resk=res1[j].rstrip(".")
            res2=re.split(r'\s+',resk)
            res3=re.split(r'<b>',resk)
            res4=re.split(r'</b>',res3[1].replace("\t.",""))
            res5=res4[0].rstrip()
            res6=res5[1:]  #Contains the parserid which we want to replace
            #print(res6)
            length=len(res6)
            res111=re.split(r'\+?/?\s?',res6)
            #print(res111)
            lenplus=len(res111)
            for i in range(lenplus):
                for k in range(flen):
                    res11=f[k][1:]
                    res12=res11[:-2]
                    res13=re.split(r'\t',res12)
                    res14=res13[1]
                    res15=res14.replace('P','')
                    #print(res15)
                    if(res111[i]==res15):
                        res7=res13[2]
                #print(res7)
                line=line.replace(res111[i],res7)
        print(line)
        g.write(line)
    else:
        g.write(line)

g.close()

 
