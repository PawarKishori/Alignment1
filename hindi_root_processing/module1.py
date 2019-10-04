def create_hindi_dataframe(parse):
    df= pd.read_csv(parse, sep='\t',names=['PID','WORD','1-','POS','2-','3-','PIDWITH','RELATION','4-','5-'])
    df.index = np.arange(1,len(df)+1)
    df1= df[['PID','WORD','POS','RELATION','PIDWITH']]
    pid = df1.PID.apply(lambda x : 'P'+str(x))
    pidwith = df1.PIDWITH.apply(lambda x : 'P'+str(x))
    relation_df =  pd.concat([pid, df1.WORD,df1.POS, df1.RELATION, pidwith], axis=1)
    return relation_df

def contained(candidate, container):
    temp = container[:]
    try:
        for v in candidate:
            temp.remove(v)
        return True
    except ValueError:
        return False

def check_vaa(pos):
    # Note: iterate with length-2, so can use i+1 and i+2 in the loop
    start_index=[]
    for i in range(len(pos)-2):
        if pos[i]=='VERB' and pos[i+1]=='AUX' and pos[i+2]=='AUX' and pos[i+3]!='AUX':
            start_index.append(i)
    return start_index

def check_va(pos):
    # Note: iterate with length-2, so can use i+1 and i+2 in the loop
    start_index=[]
    for i in range(len(pos)-2):
        if pos[i]=='VERB' and pos[i+1]=='AUX' and pos[i+2]!='AUX':
            start_index.append(i)
    return start_index

def check_vaaa(pos):
    # Note: iterate with length-2, so can use i+1 and i+2 in the loop
    start_index=[]
    for i in range(len(pos)-2):
        if pos[i]=='VERB' and pos[i+1]=='AUX' and pos[i+2]=='AUX' and pos[i+3] =='AUX' and pos[i+4]!='AUX':
            start_index.append(i)
    return start_index

def check_v(pos):
    # Note: iterate with length-2, so can use i+1 and i+2 in the loop
    start_index=[]
    for i in range(len(pos)-2):
        if pos[i]=='VERB' and pos[i+1]!='ADP'and pos[i+1]!='AUX' and pos[i+2]!='AUX':
            start_index.append(i)
    return start_index

'''def list123(desired, nums):
    #desired = [1, 2, 3]
    if str(desired)[1:-1] in str(nums):
        return True
    return False'''


def check(final):
    xxx=[];yyy=[]
    for entry in final:
        x=list(range(entry, entry+2))
        xx=[];yy=[]
        for i in x:
            xx.append(i)
            yy.append(all_dict['P'+str(i+1)][0])
            #print("=>",i)
        xxx.append(xx)
        yyy.append(yy)
    print(xxx)
    print(yyy)




def lwg(df):
    wid=list(df.iloc[:,0])
    word=list(df.iloc[:,1])
    pword=list(df.iloc[:,1])
    pos=list(df.iloc[:,2])
    relation=list(df.iloc[:,3])
    widwith =list(df.iloc[:,4])
    #print(pos)

    '''for i in range(0,len(pos)):
        print(i,word[i],pos[i])'''
    all_dict =OrderedDict()
    for i in range(0,len(pos)):
        all_dict[wid[i]]=[word[i],pos[i]]    
    #print(all_dict)
    vaaa = ['VERB', 'AUX', 'AUX', 'AUX']    
    vaa = ['VERB', 'AUX', 'AUX'] 
    va = ['VERB', 'AUX'] 
    v = ['VERB']
    a= ['AUX']
   
 
    if len(check_vaaa(pos)) > 0:
        print("vaaa")
        print(check_vaaa(pos))
        for entry in check_vaa(pos):
            print(range(entry, entry+3))

    if len(check_vaa(pos)) > 0:
        print("vaa")
        print(check_vaa(pos))
        for entry in check_vaa(pos):
            print(range(entry, entry+2))

    
    if len(check_va(pos)) > 0:
        print("va")
        final = check_va(pos)
        check(final)
        '''xxx=[];yyy=[]
        for entry in check_va(pos):
            x=list(range(entry, entry+2))
            xx=[];yy=[]
            for i in x:
                xx.append(i)
                yy.append(all_dict['P'+str(i+1)][0])
                #print("=>",i)
            xxx.append(xx)
            yyy.append(yy)
        print(xxx)
        print(yyy)'''

         

    if len(check_v(pos))>0:
        print("v")
        print(check_v(pos))

    #print(list123(a,pos))
    
    '''for i in range(0,len(pos)):
        try:
            vextra=[];nextra=[]
            if pos[i]=='VERB' and pos[i+1]=='AUX' and pos[i+2]=='AUX' and pos[i+3]=='AUX':
                #print("****VAAA****")
                v.extra.append(word[i])
                vextra.append(word[i+1])
                vextra.append(word[i+2])
                vextra.append(word[i+3])
                print("VAAA=>"," ".join(vextra))


            elif pos[i]=='VERB' and pos[i+1]=='AUX' and pos[i+2]=='AUX':
                #print("****VAA****")
                vextra.append(word[i])
                vextra.append(word[i+1])
                vextra.append(word[i+2])
                print("VAA=>"," ".join(vextra))
                #del vextra[:]


            elif pos[i]=='VERB' and pos[i+1]=='AUX' :
                #print("****VA****")
                vextra.append(word[i])
                vextra.append(word[i+1])
                #if wid[i]==widwith[i+1]:
                #    df=df[df.PID != wid[i+1]]
                print("VA=>"," ".join(vextra))
                #del vextra[:]
            
            elif pos[i]=='VERB' and pos[i+1]!='ADP':
                #print("****V****")
                vextra.append(word[i])
                print("V =>"," ".join(vextra))
            
            elif pos[i]=='AUX':
                #print("****A****")
                vextra.append(word[i])
                print("A=>"," ".join(vextra))

        except:
            print("Case not handled")'''


import sys
import pandas as pd
import numpy as np
from collections import OrderedDict 

parse_filepath = sys.argv[1] + '/hindi_parser_canonial.dat'
relation_df = create_hindi_dataframe(parse_filepath)
#print(relation_df)
wid=list(relation_df.iloc[:,0])
word=list(relation_df.iloc[:,1])
pword=list(relation_df.iloc[:,1])
pos=list(relation_df.iloc[:,2])
relation=list(relation_df.iloc[:,3])
widwith =list(relation_df.iloc[:,4])
#print(pos)

'''for i in range(0,len(pos)):
    print(i,word[i],pos[i])'''
all_dict =OrderedDict()
for i in range(0,len(pos)):
   all_dict[wid[i]]=[word[i],pos[i]]   


lwg(relation_df)


