def create_hindi_dataframe(parse):
    df= pd.read_csv(parse, sep='\t',names=['PID','WORD','1-','POS','2-','3-','PIDWITH','RELATION','4-','5-'],quotechar="~")
    df.index = np.arange(1,len(df)+1)
    df1= df[['PID','WORD','POS','RELATION','PIDWITH']]
    pid = df1.PID.apply(lambda x : 'P'+str(x))
    pidwith = df1.PIDWITH.apply(lambda x : 'P'+str(x))
    #print(df1)
    #print(df1.WORD)
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

# returns starting index of vaa verb phrase from hindi parse
def check_vaa(pos):
    # Note: iterate with length-2, so can use i+1 and i+2 in the loop
    start_index=[]
    for i in range(len(pos)-2):
        if pos[i]=='VERB' and pos[i+1]=='AUX' and pos[i+2]=='AUX' and pos[i+3]!='AUX':
            start_index.append(i)
    return start_index

# returns starting index of va verb phrase from hindi parse
def check_va(pos):
    # Note: iterate with length-2, so can use i+1 and i+2 in the loop
    start_index=[]
    for i in range(len(pos)-2):
        if pos[i]=='VERB' and pos[i+1]=='AUX' and pos[i+2]!='AUX':
            start_index.append(i)
    return start_index

# returns starting index of vaaa verb phrase from hindi parse
def check_vaaa(pos):
    # Note: iterate with length-2, so can use i+1 and i+2 in the loop
    start_index=[]
    for i in range(len(pos)-2):
        if pos[i]=='VERB' and pos[i+1]=='AUX' and pos[i+2]=='AUX' and pos[i+3] =='AUX' and pos[i+4]!='AUX':
            start_index.append(i)
    return start_index

# returns starting index of v verb phrase from hindi parse
def check_v(pos):
    # Note: iterate with length-2, so can use i+1
    start_index=[]
    for i in range(len(pos)-1):
        if pos[i]=='VERB' and pos[i+1]!='ADP'and pos[i+1]!='AUX':
            start_index.append(i)
    return start_index

def check_a(pos):
    # Note: iterate with length-1, so can use i+1 
    start_index=[]
    for i in range(len(pos)-1):
        #print("**",pos[i],pos[i-1],pos[i+1])
        if pos[i]=='AUX' and pos[i-1]!='VERB' and pos[i+1]!='AUX':
            start_index.append(i)
    return start_index

'''def list123(desired, nums):
    #desired = [1, 2, 3]
    if str(desired)[1:-1] in str(nums):
        return True
    return False'''


# returns a substring of words starting from 'final' index of length 'num'
def check(final,num):
    xxx=[];yyy=[]
    for entry in final:
        x=list(range(entry, entry+num))
        #print(x)
        xx=[];yy=[]
        for i in x:
            xx.append(i)
            yy.append(all_dict['P'+str(i+1)][0])
            #print("=>",i)
        xxx.append(xx)
        yyy.append(yy)

    #print(xxx)
    #print(yyy)
    return(" ".join(yy))

def lwg(df):
    '''wid=list(df.iloc[:,0])
    word=list(df.iloc[:,1])
    pword=list(df.iloc[:,1])
    pos=list(df.iloc[:,2])
    relation=list(df.iloc[:,3])
    widwith =list(df.iloc[:,4])
    #print(pos)

    all_dict =OrderedDict()

    for i in range(0,len(pos)):
        all_dict[wid[i]]=[word[i],pos[i]]    '''
    
    vaaa = ['VERB', 'AUX', 'AUX', 'AUX']; vaa = ['VERB', 'AUX', 'AUX']; va = ['VERB', 'AUX'] ; v = ['VERB']; a= ['AUX']
    
    indexes_covered_in_all_VPs_of_sentences = []
     
    if len(check_vaaa(pos)) > 0:
        #print("vaaa=>")
        #print(check_vaaa(pos))
        final = check_vaaa(pos)
        #print(final)
        expr_vaaa = check(final, 4)   
        print(expr_vaaa)

    if len(check_vaa(pos)) > 0:
        #print("vaa=>")
        #print(check_vaa(pos))
        final = check_vaa(pos)
        #print(final)
        #print(all_dict)
        expr_vaa=check(final, 3)
        print(expr_vaa)
       
    
    if len(check_va(pos)) > 0:
        #print("va=>")
        final = check_va(pos)
        expr_va= check(final, 2)
        print(expr_va)

    if len(check_v(pos))>0:
        #print("v=>")
        final = check_v(pos)
        expr_v = check(final,1)
        print(expr_v)
    if len(check_a(pos))>0:
        #print("a=>")
        final = check_a(pos)
        expr_a = check(final,1)
        print(expr_a)
    #print(list123(a,pos))

import sys
import pandas as pd
import numpy as np
from collections import OrderedDict 
import csv

parse_filepath = sys.argv[1] + '/hindi_parser_canonial.dat'
#parse_filepath = sys.argv[1] + '/hindi_dep_parser_original.dat'
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
#all_dict =OrderedDict()
all_dict={}
for i in range(0,len(pos)):
   #print(wid[i])
   #print(word[i])
   all_dict[wid[i]]=[word[i],pos[i]]   

lwg(relation_df)
