from __future__ import print_function
import re
from wxconv import WXC
from anytree.importer import JsonImporter
from anytree import (RenderTree, ContRoundStyle)
from anytree.exporter import DotExporter 
from IPython.display import Image


#Function to form Word-ID to Word mappings
def wordid_word_mapping(path_des, relation_df):
    f = open(path_des+'/H_wordid-word_mapping.dat','w+')
    for i in relation_df.index:
        f.write("(H_wordid-word\t"+str(relation_df.PID[i])+"\t"+str(relation_df.WORD[i])+")\n")
    f.close()
    
#Function to form Parser-ID to Word-ID mappings   
def parserid_wordid_mapping(path_des, relation_df):
    f = open(path_des+'/H_parserid-wordid_mapping.dat','w+')
    for i in relation_df.index:
        f.write("(H_parserid-wordid\tP"+str(i)+"\t"+str(relation_df.PID[i])+")\n")
    f.close()
    
#Function to save punctuation information
def punct_info(path_des, relation_df, relation_old_df):
    f = open(path_des+'/H_sentence')
    input = f.readline()
    space_separate = re.split(r' ',input)
    space_separate[-1] = space_separate[-1].rstrip()
    
    f = open(path_des+'/H_punct_info.dat','w+')

    hindi_punct=['_','_',"'","!",'"',"#","$","%","&","'","(",")",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","|","}","~","'"]
    list5 = []
    n = len(space_separate)
    i = 0
    while i < n:
        if space_separate[i] in hindi_punct:
            list5.append(space_separate[i])
            space_separate.pop(i)
            n = n-1
        i = i+1
        
    for k in range(1, len(relation_old_df)+1):
        if relation_old_df.WORD[k] in list5:
            j = relation_old_df.PID[k-1]
            f.write("(H_punc-pos-ID\t"+relation_old_df.WORD[k]+"\t"+'M\t'+str(relation_df.PID[j])+"\t"+str(relation_df.PID[j]+1)+')\n')

    for i in range(1, len(relation_old_df)+1):
        if relation_old_df.POS[i] == "PUNCT" and relation_old_df.WORD[i] not in list5:
            word = relation_old_df.WORD[i] 
            j = relation_old_df.PID[i-1]
            if word == space_separate[relation_df.PID[j]-1][-1]:
                f.write("(H_punc-pos-ID\t"+relation_old_df.WORD[i]+"\t"+'R\t'+str(relation_df.PID[j])+')\n')
            else:
                f.write("(H_punc-pos-ID\t"+relation_old_df.WORD[i]+"\t"+'L\t'+str(relation_df.PID[j]+1)+'\n')  
                
    f.close()
    
#Function to find single-line-tree   
def form_final_json_tree(relation_df, node, sub_tree, clause):
        if node == 0:
            clause.append('{\n"name": "'+str(node)+'_root'+'",\n"children": [')
        else:
            for i in relation_df.index:
                if relation_df.PID[i] == node:
                    clause.append('{\n"name": "'+str(node)+'_'+relation_df.UTF_hindi[i]+'_'+relation_df.RELATION[i]+'",\n"children": [')
        if node in sub_tree:
            for i in sub_tree[node]:
                form_final_json_tree(relation_df, i, sub_tree, clause)
        clause.append(']\n}')
        return(clause)

def wx_utf_converter(relation_df):
    a = []
    con = WXC(order='wx2utf', lang = 'hin')
    for i in relation_df.index:
        a.append(con.convert(relation_df.WORD[i]))
    relation_df['UTF_hindi'] = a
    return(relation_df)


   
#Function to convert PID to WID and update corresponding Parent ID's    
def data_PID_PIDWITH_mod(relation_df, dflen):
    list1 = relation_df.PID
    k = 1

    for i in range(1, dflen):
        try:
            list1[i]
            relation_df.at[i,'PID'] = k
            k = k+1
        except:
            print("")
            
    for i in range(1, dflen):
        try:        
            list1[i]
            relation_df.PIDWITH[i] = relation_df.at[relation_df.PIDWITH[i], 'PID']
        except:
            print('')

#Function to create Dictionary    
def create_dict(relation_df):
    sub_tree1={}
    cid = relation_df['PID'].tolist()
    hid = relation_df['PIDWITH'].tolist()
    for h,c in zip(hid, cid):
        if h in sub_tree1:
            sub_tree1[h].append(c)
        else:
            sub_tree1[h] = [c]
    return(sub_tree1)

#Function to perform DFS traversal in the tree and retrun the string as a list
def DFS(node, sub_tree, relation_df, clause):
    if node == 0:
        clause.append('(root')
        clause.append('(')
    else:
        for j in relation_df.index:
            if relation_df.PID[j] == node:
                clause.append(relation_df.WORD[j])
                clause.append('(')
    if node in sub_tree:
        for i in sub_tree[node]:
            DFS(i, sub_tree, relation_df, clause)
    clause.append(')')
    return(clause)

def draw_tree(string1, path_des, file):
    from anytree import RenderTree
    importer = JsonImporter()    
    root = importer.import_(string1)
    # Render Tree
    print(RenderTree(root, style=ContRoundStyle()))
    # # Render graph tree
    DotExporter(root).to_picture(path_des+file)
    Image(filename=path_des+file)